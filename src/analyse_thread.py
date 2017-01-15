import collections

def count_non_cap_words(thread, common_words, freq_gt):
    word_counter = collections.Counter()
    for post in thread.posts:
        trimmed_words = post.words_removed(common_words, True)
        word_counter.update(trimmed_words)
    all_users = thread.all_users
    wc = {w : c for w, c in word_counter.most_common() if c >= freq_gt and w.upper() != w and w.lower() not in common_words and w not in all_users}
    return wc

def count_phrases(thread, common_words, phrase_length):
    word_counter = collections.Counter()
    for post in thread.posts:
        trimmed_words = post.words_removed(common_words, True)
        phrases = []
        for i in range(len(trimmed_words) - (phrase_length - 1)):
            phrase = tuple(trimmed_words[i:i+phrase_length])
            if all([len(w) > 1 for w in phrase]):
                phrases.append(phrase)
        word_counter.update(phrases)
    return word_counter

def count_all_caps(thread, common_words):
    word_counter = collections.Counter()
    for post in thread.posts:
        trimmed_words = post.words_removed(common_words, False)
        words = [w for w in trimmed_words if w.upper() == w and len(w) > 1]
        word_counter.update(words)
    return word_counter


def match_words(post, common_words, freq_gt, word_map):
    """For a given post this strips the common_words and returns the set of word_map values
    that match any word that is in word_map."""
    trimmed_words = post.words_removed(common_words, True)
    return {word_map[w] for w in trimmed_words if w in word_map}

def match_phrases(post, common_words, phrase_length, phrase_map):
    """For a given post this strips the common_words and returns the phrase_map values
    that match for any phrases of length phrase_length."""
    result = set()
    trimmed_words = post.words_removed(common_words, True)
    for i in range(len(trimmed_words) - (phrase_length - 1)):
        phrase = tuple(trimmed_words[i:i+phrase_length])
        try:
            result.add(phrase_map[phrase])
        except KeyError:
            pass
    return result

def match_all_caps(post, common_words, caps_map):
    """For a given post this strips the common_words and returns the set of phrase_map values
    that match any upper case words that are in caps_map."""
    trimmed_words = post.words_removed(common_words, False)
    return {caps_map[w] for w in trimmed_words if w.upper() == w and len(w) > 1 and w in caps_map}
