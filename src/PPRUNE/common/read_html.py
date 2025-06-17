# MIT License
#
# Copyright (c) 2017 Paul Ross https://github.com/paulross
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
"""
__author__ = 'Paul Ross'
__date__ = '2017-01-01'
__version__ = '0.0.1'
__rights__ = 'Copyright (c) 2017 Paul Ross'

import argparse
import collections
import datetime
import logging
import os
import re
import pprint
import string
import sys
import time
import typing
from urllib.parse import urlparse, ParseResult

import bs4
import dateparser
import requests


logger = logging.getLogger(__file__)


HTML_PAGE_PATH = '/Users/paulross/Documents/pprune/concorde/original'
HTML_PAGE_PATH = '/Users/paulross/Documents/pprune/concorde/current'
# Matches '423988-concorde-question-2.html' with groups: ('423988', '-concorde-question-', '2')
# Special case '423988-concorde-question.html' corresponds to page 1.
RE_FILENAME = re.compile(r'(\d+)(\D+)(\d+)?\.html')
# Matches 'http://www.pprune.org/tech-log/423988-concorde-question.html#post5866333'
# Gives one group: ('5866333',)
RE_PERMALINK_TO_POST_NUMBER = re.compile(r'\S+post(\d+)')
PUNCTUATION_TABLE = str.maketrans({key: None for key in string.punctuation})
DIGITS_TABLE = str.maketrans({key: None for key in string.digits})


RE_USER_HREF_TO_USER_ID = re.compile(r'.+?/(\d+)-(\S+)')


class User(typing.NamedTuple):
    """Represents a user. Taken from a node such as:
    <a rel="nofollow" class="bigusername" href="https://www.pprune.org/members/219249-nicolai">nicolai</a>
    """
    href: str
    name: str

    @property
    def user_id(self) -> typing.Optional[str]:
        m = RE_USER_HREF_TO_USER_ID.match(self.href)
        if m:
            return f'{m.group(1)}-{m.group(2)}'


    @property
    def user_int(self) -> typing.Optional[int]:
        m = RE_USER_HREF_TO_USER_ID.match(self.href)
        if m:
            return int(m.group(1))


class Post:
    """Represents a single post in a thread."""
    def __init__(self, timestamp: datetime.datetime, permalink: str, user: User, node: bs4.element.Tag, sequence_num: int):
        self.timestamp = timestamp
        self.permalink = permalink
        self.user = user
        assert node is not None
        self.node = node
        self.sequence_num = sequence_num

    @property
    def post_message_attribute_id(self) -> str:
        """The id attribute of the post message node."""
        return f'post_message_{self.sequence_num}'

    @property
    def text(self):
        """The text in the node, this does not include the subject line.
        From:
        <div id="post_message_10994338">
        """
        text_node = self.node.find('div', **{'id' : self.post_message_attribute_id})
        return text_node.get_text()

    @property
    def text_stripped(self):
        """The text in the node with blank lines and excess whitespace removed."""
        ret = []
        for line in self.text.split('\n'):
            line = line.strip()
            if len(line):
                ret.append(line)
        return '\n'.join(ret)

    @property
    def words(self):
        txt = self.text.translate(PUNCTUATION_TABLE)
        # txt = txt.translate(DIGITS_TABLE)
        return [w for w in txt.strip().split() if not w.startswith('googletag')]
        # return [w for w in txt.lower().strip().split() if not w.startswith('googletag')]

    @property
    def post_number(self):
        m = RE_PERMALINK_TO_POST_NUMBER.match(self.permalink)
        if m is not None:
            return int(m.group(1))

    def words_removed(self, remove_these, lower_case):
        result = []
        for w in self.words:
            if lower_case and w.upper() != w:
                w = w.lower()
            if w not in remove_these:
                result.append(w)
        return result
        # return [w for w in self.words if w not in remove_these]


class Thread:
    """Represents a thread of ordered posts with some internal indexing."""
    def __init__(self):
        # Ordered list of posts
        self.posts: typing.List[Post] = []
        # Map of {permalink : post_ordinal, ...}
        self.post_map: typing.Dict[str, int] = {}
        # Map of {User : [post_ordinal, ...], ...}
        self.user_post_indexes: typing.Dict[User, typing.List[int]] = collections.defaultdict(list)

    def __len__(self) -> int:
        return len(self.posts)

    def __getitem__(self, item) -> Post:
        return self.posts[item]

    def add_post(self, post: Post):
        """Add a post."""
        if post.permalink in self.post_map:
            raise ValueError('permalink already in post_map. Trying to add: {:s}'.format(post.permalink))
        self.post_map[post.permalink] = len(self.posts)
        self.user_post_indexes[post.user].append(len(self.posts))
        self.posts.append(post)

    @property
    def all_users(self) -> typing.Set[User]:
        """All the users in this thread."""
        return set([p.user for p in self.posts])

    def get_post(self, permalink: str) -> Post:
        """Given a permalink this returns the Post object corresponding to that permalink.
        May raise KeyError or IndexError."""
        return self.posts[self.post_map[permalink]]

    def get_post_ordinals(self, user: User) -> typing.List[int]:
        """Given a user what posts have they made, by ordinal."""
        return self.user_post_indexes[user]


def get_url_text(url: str) -> str:
    """Gets a URL as text."""
    logger.info('Parsing URL %s', url)
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as err:  # pragma: no cover
        raise ValueError(f'URP request {url} raised: {err}')
    if response.status_code != 200:  # pragma: no cover
        raise ValueError(f'URP request {url} failed: {response.status_code}')
    logger.info('Parsed %d bytes from URL %s ', len(response.text), url)
    return response.text


def parse_url_to_beautiful_soup(url: str) -> bs4.BeautifulSoup:
    """Parses a URL."""
    response_text = get_url_text(url)
    return parse_str_to_beautiful_soup(response_text)


def parse_str_to_beautiful_soup(content: str) -> bs4.BeautifulSoup:
    """Parses a string as HTML."""
    parse_tree = bs4.BeautifulSoup(content, features='lxml')
    # parse_tree = bs4.BeautifulSoup(content, 'html.parser')
    return parse_tree


def get_post_nodes_from_file_path(file_path) -> typing.List[bs4.element.Tag]:
    # doctext = open('423988-concorde-question-1.html', errors='backslashreplace').read()
    with open(file_path, errors='backslashreplace') as f:
        return get_post_nodes_from_file(f)


def get_post_nodes_from_file(file: typing.TextIO) -> typing.List[bs4.element.Tag]:
    """Returns a list of posts as HTML nodes from a file object."""
    file.seek(0)
    doc = bs4.BeautifulSoup(file.read(), 'html.parser')
    return get_post_nodes_from_parsed_doc(doc)


def get_post_nodes_from_parsed_doc(doc: bs4.BeautifulSoup) -> typing.List[bs4.element.Tag]:
    posts = doc.find('div', id='posts')
    # Miss out the last one: <div id="lastpost"></div>
    ret = [c for c in posts.children if c.name == 'div' and c.attrs['id'] != 'lastpost']
    return ret


def get_post_objects_from_parsed_doc(doc: bs4.BeautifulSoup) -> typing.List[Post]:
    return [post_from_html_node(node) for node in get_post_nodes_from_parsed_doc(doc)]


def html_node_post_id(node: bs4.element.Tag) -> str:
    """The ID of the post. From:
    <div id="edit10994338">
    Would give 'edit10994338'
    """
    return node.attrs['id']


#: Matches 'edit10994338'
RE_POST_ID_TO_POST_NUMBER = re.compile(r'edit(\d+)')


def html_node_post_number(node: bs4.element.Tag) -> typing.Optional[int]:
    """The ID of the post. From:
    <div id="edit10994338">
    Would give 10994338
    """
    post_id = html_node_post_id(node)
    m = RE_POST_ID_TO_POST_NUMBER.match(post_id)
    if m:
        return int(m.group(1))


def html_node_date(node: bs4.element.Tag) -> datetime.datetime:
    """Returns the date from the node."""
    # Typically:
    # <div class="tcell" style="width:175px;">
    #     <!-- status icon and date -->
    #     <a name="post10994345">
    #         <img class="inlineimg" src="https://www.pprune.org/images/statusicon/post_old.gif" alt="Old"/>
    #     </a>
    #                         20th Feb 2021, 22:20
    #                         <!-- / status icon and date -->
    # </div>
    date_node = node.find('div', **{"class" : "tcell"})
    text = date_node.text
    ret = dateparser.parse(text.strip())
    return ret


def html_node_permalink(node: bs4.element.Tag) -> typing.Optional[str]:
    """Returns the permalink from the node."""
    # Looking for:
    # <a href="https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994345" title="Link to this Post">permalink</a>
    ret = node.find('a', title="Link to this Post")
    if ret is not None:
        return ret.attrs['href']


def html_node_user(node: bs4.element.Tag) -> typing.Optional[User]:
    """Returns the user from the node."""
    # Looking for:
    # <a rel="nofollow" class="bigusername" href="https://www.pprune.org/members/219249-nicolai">nicolai</a>
    user_node = node.find('a', **{"class" : "bigusername"})
    if user_node:
        return User(user_node.attrs['href'], user_node.text.strip())


def html_node_post_node(node: bs4.element.Tag) -> bs4.element.Tag:
    """Returns the node containing the post content from the post node."""
    # Looking for:
    # <div class="tcell alt1" id="td_post_10994338">
    post_id: int = html_node_post_number(node)
    user_node = node.find('div', **{"class" : "tcell alt1", "id" : f"td_post_{post_id}"})
    return user_node


def post_from_html_node(node: bs4.element.Tag) -> typing.Optional[Post]:
    """Returns a Post object from an HTML node."""
    timestamp = html_node_date(node)
    permalink = html_node_permalink(node)
    if permalink is None:
        logger.warning(f'No permalink extracted from node <{node.name} {node.attrs}>')
    user = html_node_user(node)
    if user is None:
        logger.warning(f'No user extracted from node <{node.name} {node.attrs}>')
    post_node = html_node_post_node(node)
    sequence_number = html_node_post_number(node)
    if sequence_number is not None:
        post = Post(timestamp, permalink, user, post_node, sequence_number)
        return post


def read_common_words(filename, n):
    """Reads file_path and returns the set of n words."""
    print('Reading words file: {}'.format(filename))
    l = []
    with open(filename) as f:
        for aline in f.readlines():
            if n <= 0:
                break
            l.append(aline.split()[0].lower())
            n -= 1
    return set(l)


def read_files(directory_name: str) -> typing.Dict[int, str]:
    """Returns a dict of {ordinal : file_abspath, ...} of the files in a directory that match RE_FILENAME."""
    files = {}
    for name in os.listdir(directory_name):
        m = RE_FILENAME.match(name)
        if m is not None:
            if m.group(3) is not None:
                key = int(m.group(3))
            else:
                key = 1
            assert key not in files, 'Key %d already in %s' % (key, str(files.keys()))
            files[key] = os.path.abspath(os.path.join(directory_name, name))
        else:
            logger.error('Can not regex "%s"', name)
    return files


def read_whole_thread(directory_name: str, count: int = -1) -> Thread:
    thread = Thread()
    files = read_files(directory_name)
    file_count = 0
    for file_number in sorted(files.keys()):
        if 0 <= count <= file_count:
            break
        post_count = 0
        for post_node in get_post_nodes_from_file_path(files[file_number]):
            # print('Post: %d' % i)
            post = post_from_html_node(post_node)
            if post is not None:
                thread.add_post(post)
                post_count += 1
            else:
                logger.warning('Can not read post from node <%s %s>', post_node.name, post_node.attrs)
        logger.info('Read: {:s} posts: {:d}'.format(files[file_number], post_count))
        file_count += 1
    logger.info('read_whole_thread(): Read %d posts' % len(thread.posts))
    return thread


def last_url_from_html_page(html_page: bs4.BeautifulSoup) -> str:
    node = html_page.find('a', **{'id': "mb_pagelast"})
    return node.attrs['href']

#: Matches https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-14.html
RE_HREF_TO_URL_NUMBER = re.compile(r'(.+?)-(\d+)\.html')


def all_page_urls_from_page(url: str, html_page: bs4.BeautifulSoup) -> typing.List[str]:
    """Get all the URLs for the thread from the first page.
    URLs
    First: https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html

    Subsequent: https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-2.html

    Last page <a id="mb_pagelast" ...
        <li>
            <a id="mb_pagelast" class="button primary hollow" href="https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-14.html" title="Last Page - Results 261 to 275 of 275">
                Last
                <i class="fas fa-angle-double-right"></i>
            </a>
        </li>

    If there is only a single page the anchor is:
        <a id="mb_pagelast" class="button primary hollow disabled" href="javascript:void(0)" title="Last Page - Results  to  of 1">
    """
    ret = [url]
    last_url = last_url_from_html_page(html_page)
    if last_url != "javascript:void(0)":
        m = RE_HREF_TO_URL_NUMBER.match(last_url)
        if m is not None:
            last_url_number = int(m.group(2))
            for i in range(2, last_url_number + 1):
                ret.append(f'{m.group(1)}-{i}.html')
    return ret


def all_page_urls_from_url(url: str) -> typing.List[str]:
    """Get all the URLs from the first page."""
    html_page = parse_url_to_beautiful_soup(url)
    return all_page_urls_from_page(url, html_page)


def get_first_page_and_subsequent_urls_from_url(url: str) -> typing.Tuple[bs4.BeautifulSoup, typing.List[str]]:
    """Get the first URL as a parsed HTML page and all the subsequent URLs."""
    html_doc = parse_url_to_beautiful_soup(url)
    return html_doc, all_page_urls_from_page(url, html_doc)[1:]


def read_whole_thread_from_url(url_first: str) -> Thread:
    """Take the first page URL and read all of the pages into a Thread object."""
    thread = Thread()
    html_doc, urls = get_first_page_and_subsequent_urls_from_url(url_first)
    for post in get_post_objects_from_parsed_doc(html_doc):
        thread.add_post(post)
    for url in urls:
        doc = parse_url_to_beautiful_soup(url)
        for post in get_post_objects_from_parsed_doc(doc):
            thread.add_post(post)
    return thread


def archive_thread_offline(url_first: str, offline_directory: str, page_count: int = -1) -> typing.Tuple[int, int]:
    """Given a URL of the first page of the thread archive all the pages limited by page_count.
    This returns the number of pages archived offline."""
    logger.info('Archiving thread from URL %s ', url_first)
    url_count = byte_count = 0
    os.makedirs(offline_directory, exist_ok=True)
    # NOTE: We read the first page twice, simplified code and all that.
    for url in all_page_urls_from_url(url_first):
        if page_count != -1 and url_count >= page_count:
            break
        text = get_url_text(url)
        parsed_url: ParseResult = urlparse(url)
        with open(os.path.join(offline_directory, os.path.basename(parsed_url.path)), 'w') as file:
            file.write(text)
        url_count += 1
        byte_count += len(text)
    logger.info('Read a total of %d bytes from URL %s ', byte_count, url_first)
    return url_count, byte_count



def main() -> int:  # pragma: no cover
    DEFAULT_OPT_LOG_FORMAT_VERBOSE = (
        '%(asctime)s - %(filename)24s#%(lineno)-4d - %(process)5d - (%(threadName)-10s) - %(levelname)-8s - %(message)s'
    )
    logging.basicConfig(level=logging.INFO, format=DEFAULT_OPT_LOG_FORMAT_VERBOSE, stream=sys.stdout)

    parser = argparse.ArgumentParser(description='Archive a thread to offline.')
    parser.add_argument('url', type=str, help='URL of the first page of the thread.')
    parser.add_argument('archive', type=str, help='Output path to save the thread pages to.')
    args = parser.parse_args()
    t_start = time.perf_counter()
    url_count, byte_count = archive_thread_offline(args.url, args.archive)
    t_elapsed = time.perf_counter() - t_start
    logger.info('Read %d URLs and %d bytes in %.3f (s) at %.3f (kb/s)', url_count, byte_count, t_elapsed, byte_count / t_elapsed / 1024)
    return 0


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
