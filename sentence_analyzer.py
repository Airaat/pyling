#!/usr/bin/env python3
import json
from collections import defaultdict

import pymorphy3
from nltk.grammar import CFG, DependencyGrammar
from nltk.parse import ChartParser, ProjectiveDependencyParser
from nltk.tree import TreePrettyPrinter
from nltk.tokenize import word_tokenize


def sanitize(sentence: str) -> list[str]:
    """Removes punctuation and casts to lower case"""
    words = word_tokenize(sentence.lower())
    result = [word for word in words if word.isalpha()]
    return result


def display_cfg_tree(data: dict) -> None:
    """Display Context Free Grammar trees"""
    for sentence, schema in data.items():
        if not schema["CFG"]:
            continue

        grammar = CFG.fromstring(schema["CFG"])
        parser = ChartParser(grammar)

        tokinized = sanitize(sentence)
        trees = parser.parse_all(tokinized)

        if len(trees) > 0:
            tpp = TreePrettyPrinter(trees[0])

            print(tpp.text())


def display_dg_tree(data: dict) -> None:
    """Display Dependency Grammar trees"""
    for sentence, schema in data.items():
        if not schema["DG"]:
            continue

        grammar = DependencyGrammar.fromstring(schema["DG"])
        parser = ProjectiveDependencyParser(grammar)

        try:
            tokenized = sanitize(sentence)
            trees = list(parser.parse(tokenized))

            if len(trees) > 0:
                trees[0].pretty_print()
        except ValueError as e:
            print(f'Error parsing sentence: "{sentence}"')
            print(str(e))


def div_by_pos(sentence: str, lang: str = 'ru') -> dict:
    """
    Divides words in a sentence by part of speech using pymorphy3.
    """

    result = defaultdict(list)
    morph = pymorphy3.MorphAnalyzer(lang=lang)

    for token in sanitize(sentence):
        parsed = morph.parse(token)[0]
        part_of_speech = parsed.tag.POS or 'unknown'
        result[part_of_speech].append(parsed.word)

    return {pos: sorted(words) for pos, words in result.items()}


if __name__ == "__main__":

    with open("dataset.json", "r", encoding='utf8') as json_file:
        DATASET = json.load(json_file)

    # display_cfg_tree(DATASET)

    for sentence in DATASET:
        parsed = div_by_pos(sentence)
        print(parsed)
