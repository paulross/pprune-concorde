import collections
import logging
import pprint
import sys
import typing

import spacy

from src.PPRUNE import read_html

logger = logging.getLogger(__file__)


def print_filtered_entity_label_map():
    pass


def process_thread(thread: read_html.Thread):
    logger.info('process_thread(): %s', thread)
    # Load English tokenizer, tagger, parser and NER
    nlp = spacy.load("en_core_web_sm")
    # {label : value : [post_ordinals, ...], ...}, ...}
    entity_lable_map: typing.Dict[str, typing.Dict[str, typing.List[int]]] = {}
    nouns = set()
    for p, post in enumerate(thread.posts):
        logger.info('Post %d/%d', p, len(thread))
        doc = nlp(post.text_stripped)
        # Analyze syntax
        # print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
        nouns |= set(chunk.text for chunk in doc.noun_chunks)
        # print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
        # Find named entities, phrases and concepts
        for entity in doc.ents:
            # print(entity.text, entity.label_)
            if entity.label_ not in entity_lable_map:
                entity_lable_map[entity.label_] = collections.defaultdict(list)
            entity_lable_map[entity.label_][entity.text].append(p)
        # print()
    # print(entity_lable_map)
    # Prune entity_lable_map
    for entity in entity_lable_map:
        to_del = []
        for key in entity_lable_map[entity]:
            if len(entity_lable_map[entity][key]) < 5:
                to_del.append(key)
        for key in to_del:
            del entity_lable_map[entity][key]
    print('entity_lable_map')
    # pprint.pprint(entity_lable_map)

    max_count = 0
    for entity in entity_lable_map:
        for subject in entity_lable_map[entity]:
            max_count = max(max_count, len(entity_lable_map[entity][subject]))

    factor = max_count // 80
    for entity in sorted(entity_lable_map.keys()):
        print(f' {entity} '.center(75, '='))
        for subject in sorted(entity_lable_map[entity].keys()):
            print(f'    {subject:16} [{len(entity_lable_map[entity][subject]):6d}]: {"*" * (len(entity_lable_map[entity][subject]) // factor)}')
        print(f' {entity}...DONE '.center(75, '='))
    print('nouns')
    pprint.pprint(nouns)


def main() -> int:  # pragma: no cover
    DEFAULT_OPT_LOG_FORMAT_VERBOSE = (
        '%(asctime)s - %(filename)24s#%(lineno)-4d - %(process)5d - (%(threadName)-10s) - %(levelname)-8s - %(message)s'
    )
    logging.basicConfig(level=logging.INFO, format=DEFAULT_OPT_LOG_FORMAT_VERBOSE, stream=sys.stdout)
    thread = read_html.read_whole_thread(read_html.HTML_PAGE_PATH)#, 40)
    process_thread(thread)

    return 0


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
