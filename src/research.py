import collections
import pprint
import sys

import read_html
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
    print('print_phrases() [{:d}]: most_common({:d})'.format(phrase_length, print_count))
    word_counter = analyse_thread.count_phrases(thread, common_words, phrase_length)
    pprint.pprint(word_counter.most_common(print_count))
    print('print_phrases() [{:d}]: most_common({:d}) sorted'.format(phrase_length, print_count))
    pprint.pprint(sorted(word_counter.most_common(print_count)))

def print_all_caps(thread, common_words, print_count):
    print('print_all_caps(): most_common({:d})'.format(print_count))
    word_counter = analyse_thread.count_all_caps(thread, common_words)
    pprint.pprint(word_counter.most_common(print_count))
    print('print_all_caps(): most_common({:d}) sorted'.format(print_count))
    pprint.pprint(sorted(word_counter.most_common(print_count)))

def print_research(thread, common_words):
    print_non_cap_words(thread, common_words)
    # print_all_caps(thread, common_words, 200)
    # print_phrases(thread, common_words, 2, 400)

def main():
    thread = read_html.read_whole_thread(sys.argv[1])
    word_count = 0
    for post in thread.posts:
        word_count += len(post.words)
    print('Number of words: {:d}'.format(word_count))
    common_words = read_html.read_common_words(sys.argv[2], 10000)
    print_research(thread, common_words)

if __name__ == '__main__':
    main()
