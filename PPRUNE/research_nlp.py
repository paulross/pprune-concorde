import collections
import logging
import pprint
import sys

import spacy

from PPRUNE.common import read_html

logger = logging.getLogger(__file__)


def process_thread(thread: read_html.Thread):
    print(thread)
    # Load English tokenizer, tagger, parser and NER
    nlp = spacy.load("en_core_web_sm")
    entity_lable_map = collections.defaultdict(set)
    nouns = set()
    for post in thread.posts:
        doc = nlp(post.text_stripped)
        # Analyze syntax
        # print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
        nouns |= set(chunk.text for chunk in doc.noun_chunks)
        # print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
        # Find named entities, phrases and concepts
        for entity in doc.ents:
            # print(entity.text, entity.label_)
            entity_lable_map[entity.label_].add(entity.text)
        # print()
    # print(entity_lable_map)
    print('entity_lable_map')
    pprint.pprint(entity_lable_map)
    print('nouns')
    pprint.pprint(nouns)


def main() -> int:  # pragma: no cover
    DEFAULT_OPT_LOG_FORMAT_VERBOSE = (
        '%(asctime)s - %(filename)24s#%(lineno)-4d - %(process)5d - (%(threadName)-10s) - %(levelname)-8s - %(message)s'
    )
    logging.basicConfig(level=logging.INFO, format=DEFAULT_OPT_LOG_FORMAT_VERBOSE, stream=sys.stdout)
    thread = read_html.read_whole_thread(read_html.HTML_PAGE_PATH)
    process_thread(thread)

    return 0


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
