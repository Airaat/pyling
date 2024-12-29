from nltk.grammar import CFG
from nltk.parse import ChartParser, ShiftReduceParser, RecursiveDescentParser
from nltk.tree import TreePrettyPrinter
from nltk.tokenize import word_tokenize


def sanitize(sentence: str) -> list[str]:
    """Removes punctuation and casts to lower case"""
    words = word_tokenize(sentence.lower())
    result = [word for word in words if word.isalpha()]
    return result


# Treasure Island. Robert Stevenson
dataset = {
    "Человек он был молчаливый.": """
    S -> NP VP
    NP -> N
    VP -> N V Adj
    N -> 'человек' | 'он'
    Adj -> 'молчаливый'
    V -> 'был'
""",
    "Целыми днями бродил по берегу бухты или взбирался на скалы с медной подзорной трубой.": """
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
    "Он не отвечал, если с ним заговаривали.": """
    S -> NP VP
    NP -> N Det V | P N V
    VP -> Conj NP
    N -> 'он' | 'ним'
    Det -> 'не'
    V -> 'отвечал' | 'заговаривали'
    P -> 'с'
    Conj -> 'если'
""",
    "По вечерам он сидел в общей комнате в самом углу, у огня, и пил ром, слегка разбавляя его водой.": None,
    "Только окинет свирепым взглядом и засвистит носом, как корабельная сирена в тумане.": None,
    "Вскоре мы и наши посетители научились оставлять его в покое.": None,
}

for sentence, schema in dataset.items():
    if not schema:
        continue

    grammar = CFG.fromstring(schema)
    parser = ChartParser(grammar)

    tokinized = sanitize(sentence)
    trees = parser.parse_all(tokinized)

    if len(trees) > 0:
        tpp = TreePrettyPrinter(trees[0])

        print(tpp.text())
