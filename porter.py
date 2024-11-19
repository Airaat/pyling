import re

VOWEL = '[аёеиоуыэюя]'
CONSONANT = '[^аёеиоуыэюя]'

PERFECTIVE_GERUNDS = '((?<=[ая])(вшись|вши|в)|(ившись|ывшись|ивши|ывши|ив|ыв))$'
ADJECTIVAL = '(?:(?<=[ая])(ем|нн|вш|ющ|щ)|(ивш|ывш|ующ))?(ими|ыми|его|ого|ему|ому|ее|ие|ые|ое|ей|ий|ый|ой|ем|им|ым|ом|их|ых|ую|юю|ая|яя|ою|ею)$'

VERB = '((?<=[ая])(ете|йте|ешь|нно|ла|на|ли|ем|ло|но|ет|ют|ны|ть|й|л|н)|(ейте|уйте|ила|ыла|ена|ите|или|ыли|ило|ыло|ено|ует|уют|ены|ить|ыть|ишь|ей|уй|ил|ыл|им|ым|ен|ят|ит|ыт|ую|ю))$'
NOUN = '(иями|ями|ами|ией|иям|ием|иях|ев|ов|ие|ье|ьё|еи|ии|ей|ой|ий|ям|ем|ам|ом|ах|ях|ию|ью|ия|ья|а|е|и|й|о|у|ы|ь|ю|я)$'

REFLEXIVES = '(с[яь])$'
SUPERLATIVE = '(ейше|ейш)$'
DERIVATIONAL = '(ость|ост)$'


def cut(pattern: str, word: str) -> str:
    return re.sub(pattern, '', word, 1)

def find_region(pattern: str, word: str) -> int:
    match = re.search(pattern, word)
    return match.end() if match else None

def find_regions(word: str) -> tuple[int, int]:
    word = word.lower()
    rv = find_region(VOWEL, word)
    r1 = find_region(VOWEL + CONSONANT, word)
    r2 = find_region(VOWEL + CONSONANT, word[r1:])
    r2 = (r2 + r1) if r2 else None

    return rv, r2

def cut_first(word: str, rv: int, *patterns) -> str:
    for pattern in patterns:
        match = re.search(pattern, word[rv:])
        if match:
            word = cut(match.group() + "$", word)
            break

    return word

def stem(word: str) -> str:
    if not word:
        raise ValueError("Строка не должна быть пустой")

    rv, r2 = find_regions(word)
    if not rv:
        return word

    # Step 1
    if re.search(PERFECTIVE_GERUNDS, word[rv:]):
        word = cut(PERFECTIVE_GERUNDS, word)
    else:
        word = cut(REFLEXIVES, word)
        word = cut_first(word, rv, ADJECTIVAL, VERB, NOUN)

    # Step 2
    if word.endswith('и'):
        word = word[:-1]

    # Step 3
    if re.search(DERIVATIONAL, word[r2:]):
        word = cut(DERIVATIONAL, word)

    # Step 4
    if word.endswith('нн'):
        word = word[:-1]
    elif re.search(SUPERLATIVE, word[rv:]):
        word = cut(SUPERLATIVE, word)
        if word.endswith('нн'):
            word = word[:-1]
    elif word.endswith('ь'):
        word = word[:-1]

    return word


if __name__ == '__main__':
    problem_words = [
        'вами',  # вам
    ]

    example = stem('вами')