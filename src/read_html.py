"""MIT License

Copyright (c) 2017 Paul Ross https://github.com/paulross

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__author__  = 'Paul Ross'
__date__    = '2017-01-01'
__version__ = '0.0.1'
__rights__  = 'Copyright (c) 2017 Paul Ross'

import collections
import os
import re
import pprint
import string

from bs4 import BeautifulSoup

HTML_PAGE_PATH = '/Users/paulross/Documents/pprune/concorde/original'
# Matches '423988-concorde-question-1.html' with two groups: ('423988', '1')
RE_FILENAME = re.compile(r'(\d+)\D+(\d+)\.html')
# Matches 'http://www.pprune.org/tech-log/423988-concorde-question.html#post5866333'
# Gives one group: ('5866333',)
RE_PERMALINK_TO_POST_NUMBER = re.compile(r'\S+post(\d+)')
PUNCTUATION_TABLE = str.maketrans({key: None for key in string.punctuation})
DIGITS_TABLE = str.maketrans({key: None for key in string.digits})

class Post:
    def __init__(self, date, permalink, user, td, pprune_sequence_num):
        self.date = date
        self.permalink = permalink
        self.user = user
        self.td = td
        self.pprune_sequence_num = pprune_sequence_num

    @property
    def text(self):
        return self.td.get_text()

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
    def __init__(self):
        # Ordered list of posts
        self.posts = []
        # Map of {permalink : post_ordinal, ...}
        self.post_map = {}

    def add_post(self, post):
        if post.permalink in self.post_map:
            raise ValueError('permalink already in post_map. Trying to add: {:s}'.format(post.permalink))
        self.post_map[post.permalink] = len(self.posts)
        self.posts.append(post)

    @property
    def all_users(self):
        return set([p.user for p in self.posts])

    def get_post(self, permalink):
        """Given a permalink this returns the Post object corresponding to that permalink.
        May raise KeyError or IndexError."""
        return self.posts[self.post_map[permalink]]

    def __len__(self):
        return len(self.posts)

def doc_to_posts(filename):
    # doctext = open('423988-concorde-question-1.html', errors='backslashreplace').read()
    with open(filename, errors='backslashreplace') as f:
        doc = BeautifulSoup(f.read(), 'html.parser')
        posts = doc.find(id='posts')
        post_entries = [c for c in posts.children if c.name == 'div']
        # Miss out the last one: <div id="lastpost"></div>
        return post_entries[:-1]


def post_text(post):
    # Every post contains a table with three rows:
    # The first row contains a timestamp as td[0]/text() and permalink as td[1]/b/a href=.
    # The second row contains the post.
    # The third row is not interesting.
    rows = [c for c in post.table.children if c.name == 'tr']
    # The first row contains two cells: a timestamp as td[0]/text() and permalink as td[1]/b/a href=.
    # >>> rows[0].find_all('td')[0].text.strip()
    # '13th Aug 2010, 04:32'
    date = rows[0].find_all('td')[0].text.strip()
    # pprunes post number
    pprune_sequence_num = int(rows[0].find_all('td')[1].a.strong.text)
    # >>> rows[0].find_all('td')[1].a['href']
    # Post link is 'http://www.pprune.org/5866333-post1.html'
    # postlink = rows[0].find_all('td')[1].a['href']
    # Permalink is: http://www.pprune.org/tech-log/423988-concorde-question.html#post5866333
    permalink = rows[0].find_all('td')[1].b.a['href']
    # print(permalink)
    # The second row contains two cells:
    # The first cell contains two <div> tags, the first contains the username.
    #   The second contains three <div> tags with join date, location, number of posts.
    # The second cell contains the text of the post
    tds = [t for t in rows[1].children if t.name == 'td']
    # Guest posters do not have a <a> link
    if tds[0].div.a is None:
        user = tds[0].div.get_text()
    else:
        user = tds[0].div.a.get_text()
    return Post(date, permalink, user, tds[1], pprune_sequence_num)

def read_common_words(filename, n):
    """Reads filename and returns the set of n words."""
    print('Reading words file: {}'.format(filename))
    l = []
    with open(filename) as f:
        for aline in f.readlines():
            if n <= 0:
                break
            l.append(aline.split()[0].lower())
            n -= 1
    return set(l)

def read_files(dirname):
    """Returns a dict of {ordinal : file_abspath, ...} of the files in a directory that match RE_FILENAME."""
    files = {}
    for aname in os.listdir(dirname):
        m = RE_FILENAME.match(aname)
        if m is not None:
            key = int(m.group(2))
            assert key not in files, 'Key %d already in %s' % (key, str(files.keys()))
            files[key] = os.path.abspath(os.path.join(dirname, aname))
            # else:
            #     print('Ignoring %s' % aname)
    return files

def read_whole_thread(html_path):
    thread = Thread()
    files = read_files(html_path)
    for filenum in sorted(files.keys()):
        post_count = 0
        for post in doc_to_posts(files[filenum]):
            # print('Post: %d' % i)
            thread.add_post(post_text(post))
            post_count += 1
        print('Read: {:s} posts: {:d}'.format(files[filenum], post_count))
    print('Read %d posts' % len(thread.posts))
    return thread
