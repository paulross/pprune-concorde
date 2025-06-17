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
import pprint
import sys

from PPRUNE.common import read_html
import analyse_thread

def print_non_cap_words(thread, common_words):
    print('print_words():')
    word_counter = analyse_thread.count_non_cap_words(thread, common_words, 10)
    print(sum(word_counter.values()))
    # pprint.pprint(word_counter.most_common(400))
    pprint.pprint(word_counter)
    # print('print_words(): sorted')
    pprint.pprint(sorted(word_counter))
    # pprint.pprint(sorted(word_counter.most_common(400)))

def print_phrases(thread, common_words, phrase_length, print_count):
    print(' print_phrases(): most_common({:d}) '.format(print_count).center(75, '-'))
    word_counter = analyse_thread.count_phrases(thread, common_words, phrase_length)
    # pprint.pprint(word_counter.most_common(print_count))
    for words, count in word_counter.most_common(print_count):
        print(f'{" ".join(words):32} : {count:4d}')
    print(' print_phrases(): most_common({:d}) DONE '.format(print_count).center(75, '-'))
    print(' print_phrases(): most_common({:d}) sorted '.format(print_count).center(75, '-'))
    # pprint.pprint(sorted(word_counter.most_common(print_count)))
    for words, count in sorted(word_counter.most_common(print_count)):
        print(f'{" ".join(words):32} : {count:4d}')
    print(' print_phrases(): most_common({:d}) sorted DONE '.format(print_count).center(75, '-'))

def print_all_caps(thread, common_words, print_count):
    print(' print_all_caps(): most_common({:d}) '.format(print_count).center(75, '-'))
    word_counter = analyse_thread.count_all_caps(thread, common_words)
    pprint.pprint(word_counter.most_common(print_count))
    print(' print_all_caps(): most_common({:d}) DONE '.format(print_count).center(75, '-'))
    print(' print_all_caps(): most_common({:d}) sorted '.format(print_count).center(75, '-'))
    pprint.pprint(sorted(word_counter.most_common(print_count)))
    print(' print_all_caps(): most_common({:d}) sorted DONE '.format(print_count).center(75, '-'))

def print_authors(thread: read_html.Thread, print_count: int):
    user_count = collections.Counter()
    for user in thread.all_users:
        for _post_ordinal in thread.get_post_ordinals(user):
            user_count.update([user.name])
    print(' print_authors(): most_common({:d}) '.format(print_count).center(75, '-'))
    # pprint.pprint(user_count.most_common(print_count))
    total = 0
    for user_name, count in user_count.most_common(print_count):
        print(f'{user_name:32} : {count:4d}')
        total += count
    print(f'TOTAL: {total:4d}')
    print(' print_authors(): most_common({:d}) DONE '.format(print_count).center(75, '-'))
    print(' print_authors(): most_common({:d}) sorted '.format(print_count).center(75, '-'))
    # pprint.pprint(user_count.most_common(print_count))
    for user_name, count in sorted(user_count.most_common(print_count)):
        print(f'{user_name:32} : {count:4d}')
    print(' print_authors(): most_common({:d}) sorted DONE '.format(print_count).center(75, '-'))



def print_research(thread, common_words):
    # print_non_cap_words(thread, common_words)
    # print_all_caps(thread, common_words, 200)
    print_phrases(thread, common_words, 2, 1000)
    # print_authors(thread, 100)

def main():
    thread = read_html.read_whole_thread(sys.argv[1])
    print(f'Number of posts: {thread.__len__()}')
    word_count = 0
    for post in thread.posts:
        word_count += len(post.words)
    print('Number of words: {:d}'.format(word_count))
    common_words = read_html.read_common_words(sys.argv[2], 1000)
    print_research(thread, common_words)

if __name__ == '__main__':
    main()
