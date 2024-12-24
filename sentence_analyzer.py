from nltk.grammar import CFG
from nltk.parse import ChartParser, ShiftReduceParser, RecursiveDescentParser
from nltk.tree import TreePrettyPrinter

# Treasure Island. Robert Stevenson
dataset = [
    "человек он был молчаливый",
    "Целыми днями бродил по берегу бухты или взбирался на скалы с медной подзорной трубой.",
    "По вечерам он сидел в общей комнате в самом углу, у огня, и пил ром, слегка разбавляя его водой.",
    "Он не отвечал, если с ним заговаривали.",
    "Только окинет свирепым взглядом и засвистит носом, как корабельная сирена в тумане.",
    "Вскоре мы и наши посетители научились оставлять его в покое."
]

grammar = CFG.fromstring("""
    S -> NP VP
    NP -> N NP | 'он'
    VP -> V Adj
    N -> 'человек'
    Adj -> 'молчаливый'
    V -> 'был'
""")


sent = dataset[0].split()
parser = ChartParser(grammar)

trees = parser.parse_all(sent)
tpp = TreePrettyPrinter(trees[0])

print(tpp.text())