import re
# TODO: 
# - вынести константы в отдельный enum
# - оформить решение в виде класса

VOWEL = '[аёеиоуыэюя]' 
CONSONANT = '[^аёеиоуыэюя]' 

PERFECTIVE_GERUNDS = '([ая](вшись|вши|в)|(ившись|ывшись|ивши|ывши|ив|ыв))$'
PARTICIPLE = '[ая](ем|нн|вш|ющ|щ)|(ивш|ывш|ующ)'
VERB = '([ая](ете|йте|ешь|нно|ла|на|ли|ем|ло|но|ет|ют|ны|ть|й|л|н)|(ейте|уйте|ила|ыла|ена|ите|или|ыли|ило|ыло|ено|ует|уют|ены|ить|ыть|ишь|ей|уй|ил|ыл|им|ым|ен|ят|ит|ыт|ую|ю))$'

ADJECTIVE = '(ими|ыми|его|ого|ему|ому|ее|ие|ые|ое|ей|ий|ый|ой|ем|им|ым|ом|их|ых|ую|юю|ая|яя|ою|ею)$'
NOUN = '(иями|ями|ами|ией|иям|ием|иях|ев|ов|ие|ье|ьё|еи|ии|ей|ой|ий|ям|ем|ам|ом|ах|ях|ию|ью|ия|ья|а|е|и|й|о|у|ы|ь|ю|я)$'

REFLEXIVES = '(с[яь])$'
SUPERLATIVE = '(ейше|ейш)$'
DERIVATIONAL = '(ость|ост)$'

def find_region(pattern: str, word: str, is_rv: bool = False) -> str:
    match = re.search(pattern, word)
    if not match:
        return ''
    ind = match.end()
    if is_rv and word[ind-1] in "ая":
        ind -= 1
    
    return word[ind:]
    
def get_word_base(word: str) -> str:
    if not word:
        raise ValueError("Строка не должна быть пустой")
    
    word = word.lower()
    rv = find_region(VOWEL, word, is_rv=True)
    r1 = find_region(VOWEL + CONSONANT, word)
    r2 = find_region(VOWEL + CONSONANT, r1)

    # Step 1: 
    # - Если есть perfective_gerund удалить и перейти к Step 2
    # - Если нет, то удалить reflexive с конца слова, 
    # затем adjectival, VERB, NOUN - как только одно из них найденно, шаг завершается
    if re.search(PERFECTIVE_GERUNDS, rv):
        word = re.sub(PERFECTIVE_GERUNDS, '', word)
    else:
        word = re.sub(REFLEXIVES, '', word)
        if re.search(PARTICIPLE, rv) or re.search(ADJECTIVE, rv):
            word = re.sub(PARTICIPLE, '', word)
            word = re.sub(ADJECTIVE, '', word)
        elif re.search(VERB, rv):
            word = re.sub(VERB, '', word)
        elif re.search(NOUN, rv):
            word = re.sub(NOUN, '', word)

    # Step 2: если слово оканчивается на И, удаляем
    if word.endswith('и'):
        word = word[:-1]

    # Step 3: если в r2 найдется DERIVATIONAL, удаляем
    if re.search(DERIVATIONAL, r2):
        word = re.sub(DERIVATIONAL, '', word)
    
    # Step 4: 
    # - Если слово оканчивается на НН удаляем последнюю букву
    # - Если слово оканчивается на SUPERLATIVE удаляем его и повторяем удаление последней буквы Н при НН
    # - Если слово оканчивается на Ь удаляем его 
    if word.endswith('нн'):
        word = word[:-1]
    elif re.search(SUPERLATIVE, word):
        word = re.sub(SUPERLATIVE, '', word)
        if word.endswith('нн'):
            word = word[:-1]
    elif word.endswith('ь'):
        word = word[:-1]

    return word
    
def norm(word: str) -> str:
    word_list = word.split('|')
    word_list.sort(key=len, reverse=True)

    return '|'.join(word_list)



if __name__ == '__main__':
    words = ['гналась', 'противоестесвтенном', 'выживший', 'забегавшись', 'неотвратимость']
    bases = []
    for word in words:
        base = get_word_base(word)
        bases.append(base)
    
    print(' | '.join(bases))