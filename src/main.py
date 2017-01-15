import os
import sys

import read_html
import write_html


def common_words_file():
    return os.path.normpath(os.path.join(os.path.dirname(__file__), 'count_1w.txt'))


def main():
    thread = read_html.read_whole_thread(sys.argv[1])
    word_count = 0
    for post in thread.posts:
        word_count += len(post.words)
    print('Number of words: {:d}'.format(word_count))
    common_words = read_html.read_common_words(common_words_file(), 1000)
    # write_html.pass_one(thread, common_words)
    write_html.write_whole_thread(thread, common_words)
    print('Bye, bye!')

if __name__ == '__main__':
    main()