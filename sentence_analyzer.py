#!/usr/bin/env python3
from nltk.grammar import CFG, DependencyGrammar
from nltk.parse import ChartParser, ProjectiveDependencyParser
from nltk.tree import TreePrettyPrinter
from nltk.tokenize import word_tokenize


def sanitize(sentence: str) -> list[str]:
    """Removes punctuation and casts to lower case"""
    words = word_tokenize(sentence.lower())
    result = [word for word in words if word.isalpha()]
    return result


def display_cfg_tree(data: dict[str, str]) -> None:
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


def display_dg_tree(data: dict[str, str]) -> None:
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


# Treasure Island. Robert Stevenson
DATASET = {
    "Человек он был молчаливый.": {
        "CFG": """
            S -> NP VP
            NP -> N
            VP -> N V Adj
            N -> 'человек' | 'он'
            Adj -> 'молчаливый'
            V -> 'был'
        """,
        "DG": """
            'был' -> 'молчаливый' | 'он'
            'он' -> 'человек'
        """,
    },
    "Целыми днями бродил по берегу бухты или взбирался на скалы с медной подзорной трубой.": {
        "CFG": """
            S -> VP Conj VP
            VP -> AP V NP | V PP AP
            Conj -> 'или'
            AP -> Adj N | P Adj Adj N
            NP -> PP N | PP AP N
            PP -> P N
            V -> 'бродил' | 'взбирался'
            N -> 'днями' | 'берегу' | 'бухты' | 'скалы' | 'трубой'
            P -> 'по' | 'на' | 'с'
            Adj -> 'целыми' | 'медной' | 'подзорной'
        """,
        "DG": """
            'или' -> 'взбирался' | 'бродил'
            'бродил' -> 'по' | 'днями'
            'днями' -> 'целыми'
            'по' -> 'берегу'
            'берегу' -> 'бухты'
            'взбирался' -> 'на'
            'на' -> 'скалы'
            'скалы' -> 'с'
            'с' -> 'трубой'
            'трубой' -> 'медной' | 'подзорной'
        """,
    },
    "Он не отвечал, если с ним заговаривали.": {
        "CFG": """
            S -> NP VP
            NP -> N Det V | P N V
            VP -> Conj NP
            N -> 'он' | 'ним'
            Det -> 'не'
            V -> 'отвечал' | 'заговаривали'
            P -> 'с'
            Conj -> 'если'
        """,
        "DG": """
            'отвечал' -> 'он' | 'не' | 'если'
            'если' -> 'заговаривали'
            'заговаривали' -> 'с'
            'с' -> 'ним'
        """,
    },
    "Только окинет свирепым взглядом и засвистит носом, как корабельная сирена в тумане.": {
        "CFG": """
            S -> VP NP
            NP -> Conj AdjP PP
            VP -> AdvP AdjP Conj V N
            AdvP -> Adv V
            AdjP -> Adj N
            PP -> P N
            P -> 'в'
            Adv -> 'только'
            Conj -> 'и' | 'как'
            V -> 'окинет' | 'засвистит'
            Adj -> 'свирепым' | 'корабельная'
            N -> 'взглядом' | 'носом' | 'сирена' | 'тумане'
        """,
        "DG": """
            'и' -> 'окинет' | 'засвистит'
            'окинет' -> 'только' | 'взглядом'
            'взглядом' -> 'свирепым'
            'засвистит' -> 'носом' | 'как'
            'как' -> 'сирена'
            'сирена' -> 'корабельная' | 'в'
            'в' -> 'тумане'
        """,
    },
    "По вечерам он сидел в общей комнате в самом углу, у огня, и пил ром, слегка разбавляя его водой.": {
        "CFG": """
            S -> PP NP AdjP AdjP PP VP AdvP

            NP -> N V
            VP -> Conj V N
            AdvP -> Adv Adv N N
            PP -> P N
            AdjP -> P Adj N

            Conj -> 'и'
            P -> 'по' | 'в' | 'у'
            N -> 'вечерам' | 'он' | 'комнате' | 'углу' | 'огня' | 'ром' | 'его' | 'водой'
            V -> 'сидел' | 'пил'
            Adj -> 'общей' | 'самом'
            Adv -> 'разбавляя' | 'слегка'
        """,
        "DG": """
            'сидел' -> 'он' | 'в' | 'по' | 'у' | 'и'
            'по' -> 'вечерам'
            'в' -> 'комнате' | 'углу'
            'комнате' -> 'общей'
            'углу' -> 'самом'
            'у' -> 'огня'
            'и' -> 'пил'
            'пил' -> 'ром' | 'разбавляя'
            'разбавляя' -> 'слегка' | 'его'
            'его' -> 'водой'
        """,
    },
    "Вскоре мы и наши посетители научились оставлять его в покое.": {
        "CFG": """
            S -> NP VP
            NP -> AdvP Conj AdjP
            AdvP -> Adv N
            AdjP -> Adj N
            VP -> V V N PP
            PP -> P N
            Adv -> 'вскоре'
            N -> 'мы' | 'посетители' | 'его' | 'покое'
            V -> 'научились' | 'оставлять'
            Adj -> 'наши'
            P -> 'в'
            Conj -> 'и'
        """,
        "DG": """
            'научились' -> 'вскоре' | 'и' | 'оставлять'
            'и' -> 'мы' | 'посетители'
            'посетители' -> 'наши'
            'оставлять' -> 'его' | 'в'
            'в' -> 'покое'
        """,
    },
}

if __name__ == "__main__":
    display_cfg_tree(DATASET)
