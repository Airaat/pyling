import re
# TODO: 
# оформить в виде модуля
# скомпилировать регулярки в константах
# решить баг с "вами" -> "в"

class RePorterStemmer:
    VOWEL = '[аёеиоуыэюя]' 
    CONSONANT = '[^аёеиоуыэюя]' 

    PERFECTIVE_GERUNDS = '((?<=[ая])(вшись|вши|в)|(ившись|ывшись|ивши|ывши|ив|ыв))$'
    PARTICIPLE = '(?<=[ая])(ем|нн|вш|ющ|щ)|(ивш|ывш|ующ)'
    VERB = '((?<=[ая])(ете|йте|ешь|нно|ла|на|ли|ем|ло|но|ет|ют|ны|ть|й|л|н)|(ейте|уйте|ила|ыла|ена|ите|или|ыли|ило|ыло|ено|ует|уют|ены|ить|ыть|ишь|ей|уй|ил|ыл|им|ым|ен|ят|ит|ыт|ую|ю))$'

    ADJECTIVE = '(ими|ыми|его|ого|ему|ому|ее|ие|ые|ое|ей|ий|ый|ой|ем|им|ым|ом|их|ых|ую|юю|ая|яя|ою|ею)$'
    NOUN = '(иями|ями|ами|ией|иям|ием|иях|ев|ов|ие|ье|ьё|еи|ии|ей|ой|ий|ям|ем|ам|ом|ах|ях|ию|ью|ия|ья|а|е|и|й|о|у|ы|ь|ю|я)$'

    REFLEXIVES = '(с[яь])$'
    SUPERLATIVE = '(ейше|ейш)$'
    DERIVATIONAL = '(ость|ост)$'

    @classmethod
    def __find_region(cls, pattern: str, word: str) -> int:
        match = re.search(pattern, word)
        return match.end() if match else None

    @classmethod
    def __cut(cls, pattern, string) -> str:
        return re.sub(pattern, '', string, 1)

    @classmethod
    def stem(cls, word: str) -> str:
        if not word:
            raise ValueError("Строка не должна быть пустой")
        
        word = word.lower()
        rv = cls.__find_region(cls.VOWEL, word)
        r1 = cls.__find_region(cls.VOWEL + cls.CONSONANT, word)
        r2 = cls.__find_region(cls.VOWEL + cls.CONSONANT, word[r1:])
        r2 = (r2 + r1) if r2 else None

        if not rv:
            return word

        # Step 1
        if re.search(cls.PERFECTIVE_GERUNDS, word[rv:]):
            word = cls.__cut(cls.PERFECTIVE_GERUNDS, word)
        else:
            word = cls.__cut(cls.REFLEXIVES, word)
            if re.search(cls.PARTICIPLE, word[rv:]) or re.search(cls.ADJECTIVE, word[rv:]):
                word = cls.__cut(cls.PARTICIPLE, word)
                word = cls.__cut(cls.ADJECTIVE, word)
            elif re.search(cls.VERB, word[rv:]):
                word = cls.__cut(cls.VERB, word)
            elif re.search(cls.NOUN, word[rv:]):
                word = cls.__cut(cls.NOUN, word)

        # Step 2
        if word.endswith('и'):
            word = word[:-1]

        # Step 3
        if re.search(cls.DERIVATIONAL, word[r2:]):
            word = cls.__cut(cls.DERIVATIONAL, word)
        
        # Step 4
        if word.endswith('нн'):
            word = word[:-1]
        elif re.search(cls.SUPERLATIVE, word[rv:]):
            word = cls.__cut(cls.SUPERLATIVE, word)
            if word.endswith('нн'):
                word = word[:-1]
        elif word.endswith('ь'):
            word = word[:-1]

        return word

# FIX: отрезаем match, а не заново ищем
if __name__ == '__main__':
    problem_words = [
        'вами', # вам
    ]

    example = RePorterStemmer.stem('вами')

    