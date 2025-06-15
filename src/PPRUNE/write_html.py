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
from contextlib import contextmanager
import os
import pprint
import shutil
import string
import sys

import analyse_thread
import concorde_pub_map
import styles

PUNCTUATION_TABLE = str.maketrans({key: '-' for key in string.punctuation})
POSTS_PER_PAGE = 20
# +/- Links to other pages
PAGE_LINK_COUNT = 10

# Google analytics script
GOOGLE_ANALYTICS_SCRIPT = """<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-90397128-1', 'auto');
  ga('send', 'pageview');

</script>
"""

def get_out_path():
    return os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir, 'docs'))

@contextmanager
def element(_stream, _name, **attributes):
    _stream.write('<{}'.format(_name))
    # Sort attributes: {true_name : attribute key, ...}
    attr_dict = {}
    for k in attributes.keys():
        if k.startswith('_'):
            assert k[1:] not in attr_dict
            attr_dict[k[1:]] = k
        else:
            attr_dict[k] = k
    if len(attributes):
        for a in sorted(attr_dict.keys()):
            _stream.write(' {}={}'.format(a, attributes[attr_dict[a]]))
    _stream.write('>')
    yield
    _stream.write('</{}>\n'.format(_name))

def pass_one(thread, common_words):
    """Works through every post in the thread and returns a tuple of maps:
    (
        {subject : [post_ordinals, ...], ...}
        {post_ordinals : set([subject, ...]), ...}
    )
    """
    subject_post_map = collections.defaultdict(list)
    post_subject_map = {}
    user_subject_map = collections.defaultdict(set)
    for i, post in enumerate(thread.posts):
        subjects = analyse_thread.match_words(post, common_words, 10, concorde_pub_map.WORDS_MAP)
        subjects |= analyse_thread.match_all_caps(post, common_words, concorde_pub_map.CAPS_WORDS)
        subjects |= analyse_thread.match_phrases(post, common_words, 2, concorde_pub_map.PHRASES_2_MAP)
        if post.pprune_sequence_num in concorde_pub_map.SPECIFIC_POSTS_MAP:
            subjects.add(concorde_pub_map.SPECIFIC_POSTS_MAP[post.pprune_sequence_num])
        for subject in subjects:
            subject_post_map[subject].append(i)
        post_subject_map[post.pprune_sequence_num] = subjects
        user_subject_map[post.user.strip()] |= subjects
        # print('Post {:3d} subjects [{:3d}]: {}'.format(i, len(subjects), subjects))
    # pprint.pprint(subject_map, width=200)
    return subject_post_map, post_subject_map, user_subject_map

def _subject_page_name(subject, page_num):
    result = subject.translate(PUNCTUATION_TABLE) + '{:d}.html'.format(page_num)
    result = result.replace(' ', '_')
    # print(subject, '->' , result)
    return result

def write_index_page(thread, subject_map, user_subject_map, out_path):
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    styles.writeCssToDir(out_path)
    with open(os.path.join(out_path, 'index.html'), 'w') as index:
        index.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
        with element(index, 'html', xmlns="http://www.w3.org/1999/xhtml", dir="ltr", lang="en"):
            with element(index, 'head'):
                with element(index, 'meta', name='keywords', content='Concord'):
                    pass
                with element(index, 'link', rel="stylesheet", type="text/css", href=styles.CSS_FILE):
                    pass
                index.write(GOOGLE_ANALYTICS_SCRIPT)
            with element(index, 'body'):
                # with element(index, 'table', border="0", width="96%", cellpadding="0", cellspacing="0", bgcolor="#FFFFFF", align="center"):
                with element(index, 'h1'):
                    index.write('Concorde Re-mixed')
                with element(index, 'p'):
                    index.write('There is a great ')
                    with element(index, 'a', href='http://www.pprune.org/tech-log/423988-concorde-question.html'):
                        index.write('thread on pprune')
                    index.write(' that contains a fascinating discussion from experts about Concorde.')
                    index.write(' The thread has nearly 2000 posts and around 100 pages.')
                    index.write(' Naturally enough it is ordered in time of each post but since it covers so many subjects it is a little hard to follow a particular subject.')
                with element(index, 'p'):
                    index.write('Here I have reorganised the original thread by subject semi-automatically using Python.')
                    index.write(' Any post that refers to a subject is included in a page in the original order of the posts.')
                    index.write(' Posts that mention multiple subjects are duplicated appropriately.')
                    index.write(' I have not changed the content of any post and this includes links and images.')
                    index.write(' Each post is linked to the original so that you can check ;-)')
                with element(index, 'p'):
                    index.write('Here are all {:d} subjects I have identified with the number of posts for each subject:'.format(len(subject_map)))
                with element(index, 'table', _class="indextable"):
                    COLUMNS = 4
                    subjects = sorted(subject_map.keys())
                    rows = [subjects[i:i+COLUMNS] for i in range(0, len(subjects), COLUMNS)]
                    subject_index = 0
                    for row in rows:
                        with element(index, 'tr'):
                            for _cell in row:
                                subject = subjects[subject_index]
                                with element(index, 'td', _class='indextable'):
                                    with element(index, 'a',
                                                 href=_subject_page_name(subject, 0)):
                                        index.write('{:s} [{:d}]'.format(subject,
                                                                         len(subject_map[subject])))
                                # print(subject, subject_map[subject])
                                subject_index += 1
                # Posts by user, including the subjects they covered
                with element(index, 'h1'):
                    index.write('Hall of Fame')
                MOST_COMMON_COUNT = 20
                user_count = collections.Counter([p.user.strip() for p in thread.posts])
                # print(user_count)
                with element(index, 'p'):
                    index.write('The most prolific {:d} posters in the original thread:'.format(MOST_COMMON_COUNT))
                with element(index, 'table', _class="indextable"):
                    with element(index, 'tr'):
                        with element(index, 'th', _class='indextable'):
                            index.write('User Name')
                        with element(index, 'th', _class='indextable'):
                            index.write('Number of Posts')
                        with element(index, 'th', _class='indextable'):
                            index.write('Subjects')
                    for k, v in user_count.most_common(MOST_COMMON_COUNT):
                        with element(index, 'tr'):
                            # User name
                            with element(index, 'td', _class='indextable'):
                                index.write(k)
                            # Count of posts
                            with element(index, 'td', _class='indextable'):
                                index.write('{:d}'.format(v))
                            # Comma separated list of subjects that they are identified with 
                            with element(index, 'td', _class='indextable'):
                                subjects = sorted(user_subject_map[k])
                                for subject in subjects:
                                    with element(index, 'a',
                                                 href=_subject_page_name(subject, 0)):
                                        index.write(subject)
                                    index.write('&nbsp; ')

def _write_page_links(subject, page_num, page_count, f):
    with element(f, 'p', _class='page_links'):
        f.write('Page Links:&nbsp;')
        if page_count > 1:
            with element(f, 'a', href=_subject_page_name(subject, 0)):
                f.write('First')
            if page_num > 0:
                f.write('&nbsp;')
                with element(f, 'a', href=_subject_page_name(subject, page_num - 1)):
                    f.write('Previous')
            page_start = max(0, page_num - PAGE_LINK_COUNT)
            page_end = min(page_count - 1, page_num + PAGE_LINK_COUNT)
            for p in range(page_start, page_end + 1):
                f.write('&nbsp;')
                with element(f, 'a', href=_subject_page_name(subject, p)):
                    if p == page_num:
                        with element(f, 'b'):
                            f.write('{:d}'.format(p + 1))
                    else:
                        f.write('{:d}'.format(p + 1))
            if page_num < page_count - 1:
                f.write('&nbsp;')
                with element(f, 'a', href=_subject_page_name(subject, page_num + 1)):
                    f.write('Next')
            f.write('&nbsp;')
            with element(f, 'a', href=_subject_page_name(subject, page_count - 1)):
                f.write('Last')
            f.write('&nbsp;')
        with element(f, 'a', href='index.html'):
            f.write('Index Page')

def write_subject_page(thread, subject_map, subject, out_path):
    _posts = subject_map[subject]
    pages = [_posts[i:i+POSTS_PER_PAGE] for i in range(0, len(_posts), POSTS_PER_PAGE)]
    for p, page in enumerate(pages):
        with open(os.path.join(out_path, _subject_page_name(subject, p)), 'w') as f:
            f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
            with element(f, 'html', xmlns="http://www.w3.org/1999/xhtml", dir="ltr", lang="en"):
                with element(f, 'head'):
                    with element(f, 'meta', name='keywords', content='Concord {:s}'.format(subject)):
                        pass
                    with element(f, 'link', rel="stylesheet", type="text/css", href=styles.CSS_FILE):
                        pass
                    f.write(GOOGLE_ANALYTICS_SCRIPT)
                with element(f, 'body'):
                    with element(f, 'h1'):
                        f.write('Posts about: "{:s}" [Posts: {:d} Pages: {:d}]'.format(subject, len(_posts), len(pages)))
                    _write_page_links(subject, p, len(pages), f)
                    # with element(f, 'table', border="0", width="96%", cellpadding="0", cellspacing="0", bgcolor="#FFFFFF", align="center"):
                    with element(f, 'table', _class='posts'):
                        for post_index in page:
                            post = thread.posts[post_index]
                            with element(f, 'tr', valign="top"):
                                # with element(f, 'td', _class="alt2", style="border: 1px solid #000063; border-top: 0px; border-bottom: 0px"):
                                with element(f, 'td', _class="post"):
                                    f.write(post.user)
                                    f.write('<br/>{:s}'.format(post.date))
                                    with element(f, 'a', href=post.permalink):
                                        f.write('<br/>permalink')
                                    f.write(' Post: {:d}'.format(post.pprune_sequence_num))
                                f.write(post.td.prettify())
                    _write_page_links(subject, p, len(pages), f)

def write_whole_thread(thread, common_words):
    out_path = get_out_path()
    print('Output path: {}'.format(out_path))
    shutil.rmtree(out_path, ignore_errors=True)
    subject_map, post_map, user_subject_map = pass_one(thread, common_words)
#     pprint.pprint(user_subject_map)
    print('Writing: {:s}'.format('index.html'))
    write_index_page(thread, subject_map, user_subject_map, out_path)
    for subject in sorted(subject_map.keys()):
        print('Writing: "{:s}" [{:d}]'.format(subject, len(subject_map[subject])))
        write_subject_page(thread, subject_map, subject, out_path)
#     pprint.pprint(post_map)
