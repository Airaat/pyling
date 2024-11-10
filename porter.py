class PorterStemmer:
    """
    Стеммер Портера - алгоритм нахождения основы заданного слова,
    путем последовательного отсечения окончаний и суффиксов
    """

    VOWELS = 'аёеиоуыэюя'

    PERFECTIVE_GERUNDS = ('вшись', 'вши', 'в', 'ившись', 'ывшись', 'ивши', 'ывши', 'ив', 'ыв')
    AYA_PERFECTIVE_GERUNDS = ('вшись', 'вши', 'в')

    REFLEXIVES = ('ся', 'сь')

    ADJECTIVAL = (
        'ившими', 'ившыми', 'ившего', 'ившого', 'ившему', 'ившому', 'ывшими', 'ывшыми', 'ывшего', 'ывшого', 'ывшему',
        'ывшому', 'ующими', 'ующыми', 'ующего', 'ующого', 'ующему', 'ующому', 'емими', 'емыми', 'емего', 'емого',
        'емему', 'емому', 'нними', 'нными', 'ннего', 'нного', 'ннему', 'нному', 'вшими', 'вшыми', 'вшего', 'вшого',
        'вшему', 'вшому', 'ющими', 'ющыми', 'ющего', 'ющого', 'ющему', 'ющому', 'ившее', 'ившие', 'ившые', 'ившое',
        'ившей', 'ивший', 'ившый', 'ившой', 'ившем', 'ившим', 'ившым', 'ившом', 'ивших', 'ившых', 'ившую', 'ившюю',
        'ившая', 'ившяя', 'ившою', 'ившею', 'ывшее', 'ывшие', 'ывшые', 'ывшое', 'ывшей', 'ывший', 'ывшый', 'ывшой',
        'ывшем', 'ывшим', 'ывшым', 'ывшом', 'ывших', 'ывшых', 'ывшую', 'ывшюю', 'ывшая', 'ывшяя', 'ывшою', 'ывшею',
        'ующее', 'ующие', 'ующые', 'ующое', 'ующей', 'ующий', 'ующый', 'ующой', 'ующем', 'ующим', 'ующым', 'ующом',
        'ующих', 'ующых', 'ующую', 'ующюю', 'ующая', 'ующяя', 'ующою', 'ующею', 'емее', 'емие', 'емые', 'емое', 'емей',
        'емий', 'емый', 'емой', 'емем', 'емим', 'емым', 'емом', 'емих', 'емых', 'емую', 'емюю', 'емая', 'емяя', 'емою',
        'емею', 'ннее', 'нние', 'нные', 'нное', 'нней', 'нний', 'нный', 'нной', 'ннем', 'нним', 'нным', 'нном', 'нних',
        'нных', 'нную', 'ннюю', 'нная', 'нняя', 'нною', 'ннею', 'вшее', 'вшие', 'вшые', 'вшое', 'вшей', 'вший', 'вшый',
        'вшой', 'вшем', 'вшим', 'вшым', 'вшом', 'вших', 'вшых', 'вшую', 'вшюю', 'вшая', 'вшяя', 'вшою', 'вшею', 'ющее',
        'ющие', 'ющые', 'ющое', 'ющей', 'ющий', 'ющый', 'ющой', 'ющем', 'ющим', 'ющым', 'ющом', 'ющих', 'ющых', 'ющую',
        'ющюю', 'ющая', 'ющяя', 'ющою', 'ющею', 'щими', 'щыми', 'щего', 'щого', 'щему', 'щому', 'щее', 'щие', 'щые',
        'щое', 'щей', 'щий', 'щый', 'щой', 'щем', 'щим', 'щым', 'щом', 'щих', 'щых', 'щую', 'щюю', 'щая', 'щяя', 'щою',
        'щею', 'ими', 'ыми', 'его', 'ого', 'ему', 'ому', 'ее', 'ие', 'ые', 'ое', 'ей', 'ий', 'ый', 'ой', 'ем', 'им',
        'ым', 'ом', 'их', 'ых', 'ую', 'юю', 'ая', 'яя', 'ою', 'ею'
    )

    VERBS = (
        'ете', 'йте', 'ешь', 'нно', 'ла', 'на', 'ли', 'ем', 'ло', 'но', 'ет', 'ют', 'ны', 'ть', 'й', 'л', 'н', 'ейте',
        'уйте', 'ила', 'ыла', 'ена', 'ите', 'или', 'ыли', 'ило', 'ыло', 'ено', 'ует', 'уют', 'ены', 'ить', 'ыть', 'ишь',
        'ей', 'уй', 'ил', 'ыл', 'им', 'ым', 'ен', 'ят', 'ит', 'ыт', 'ую', 'ю'
    )

    AYA_VERBS = ('ете', 'йте', 'ешь', 'нно', 'ла', 'на', 'ли', 'ем', 'ло', 'но', 'ет', 'ют', 'ны', 'ть', 'й', 'л', 'н')

    NOUNS = (
        'иями', 'ями', 'ами', 'ией', 'иям', 'ием', 'иях', 'ев', 'ов', 'ие', 'ье', 'ьё', 'еи', 'ии', 'ей', 'ой', 'ий',
        'ям', 'ем', 'ам', 'ом', 'ах', 'ях', 'ию', 'ью', 'ия', 'ья', 'а', 'е', 'и', 'й', 'о', 'у', 'ы', 'ь', 'ю', 'я'
    )

    DERIVATIONALS = ('ость', 'ост')
    SUPERLATIVES = ('ейше', 'ейш')

    @staticmethod
    def stem(word: str) -> str:
        """
        Возвращает основу исходного слова, отсекая все суффиксы и окончания
        """
        if not word:
            raise ValueError("Строка не должна быть пустой")

        word = word.lower()
        rv, r2 = PorterStemmer.__find_regions(word)

        word, rv, r2 = PorterStemmer.__step_1(word, rv, r2)
        word, rv, r2 = PorterStemmer.__step_2(word, rv, r2)
        word, r2 = PorterStemmer.__step_3(word, r2)
        word = PorterStemmer.__step_4(word)

        return word

    @staticmethod
    def __find_regions(word: str) -> tuple[str, str]:
        """
        Нахождение регионов `rv`, `r2` в слове `word`
        """
        rv, r1, r2 = '', '', ''

        for i in range(1, len(word)):
            if word[i - 1] in PorterStemmer.VOWELS and word[i] not in PorterStemmer.VOWELS:
                r1 = word[i + 1:]
                break

        for i in range(1, len(r1)):
            if r1[i - 1] in PorterStemmer.VOWELS and r1[i] not in PorterStemmer.VOWELS:
                r2 = r1[i + 1:]
                break

        for i in range(len(word)):
            if word[i] in PorterStemmer.VOWELS:
                rv = word[i + 1:]
                break

        return rv, r2

    @staticmethod
    def __step_1(word: str, rv: str, r2: str) -> tuple[str, str, str]:
        """
        Step 1: 
        - Если есть perfective_gerund удалить и перейти к Step 2
        - Если нет, то удалить reflexive с конца слова, 
        затем adjectival, verb, noun - как только одно из них найденно, шаг завершается
        """

        step1_success = False
        adjectival_removed = False
        verb_removed = False

        for suffix in PorterStemmer.PERFECTIVE_GERUNDS:
            if rv.endswith(suffix):
                len_suffix = len(suffix)
                if suffix in PorterStemmer.AYA_PERFECTIVE_GERUNDS:
                    if rv[-len_suffix - 1: -len_suffix] in ('а', 'я'):
                        word = word[: -len_suffix]
                        r2 = r2[: -len_suffix]
                        rv = rv[: -len_suffix]
                        step1_success = True
                        break
                else:
                    word = word[: -len_suffix]
                    r2 = r2[: -len_suffix]
                    rv = rv[: -len_suffix]
                    step1_success = True
                    break

        if not step1_success:
            for suffix in PorterStemmer.REFLEXIVES:
                if rv.endswith(suffix):
                    len_suffix = len(suffix)
                    word = word[: -len_suffix]
                    r2 = r2[: -len_suffix]
                    rv = rv[: -len_suffix]
                    break

            for suffix in PorterStemmer.ADJECTIVAL:
                if rv.endswith(suffix):
                    len_suffix = len(suffix)
                    if (suffix[0] == 'щ' or suffix[:2] in ('ем', 'нн', 'вш', 'ющ')):
                        if rv[-len_suffix - 1: -len_suffix] in ('а', 'я'):
                            word = word[: -len_suffix]
                            r2 = r2[: -len_suffix]
                            rv = rv[: -len_suffix]
                            adjectival_removed = True
                            break
                    else:
                        word = word[: -len_suffix]
                        r2 = r2[: -len_suffix]
                        rv = rv[: -len_suffix]
                        adjectival_removed = True
                        break

            if not adjectival_removed:
                for suffix in PorterStemmer.VERBS:
                    if rv.endswith(suffix):
                        len_suffix = len(suffix)
                        if suffix in PorterStemmer.AYA_VERBS:
                            if rv[-len_suffix - 1: -len_suffix] in ('а', 'я'):
                                word = word[: -len_suffix]
                                r2 = r2[: -len_suffix]
                                rv = rv[: -len_suffix]
                                verb_removed = True
                                break

                        else:
                            word = word[: -len_suffix]
                            r2 = r2[: -len_suffix]
                            rv = rv[: -len_suffix]
                            verb_removed = True
                            break

            if not adjectival_removed and not verb_removed:
                for suffix in PorterStemmer.NOUNS:
                    if rv.endswith(suffix):
                        len_suffix = len(suffix)
                        word = word[: -len_suffix]
                        r2 = r2[: -len_suffix]
                        rv = rv[: -len_suffix]

        return word, rv, r2

    @staticmethod
    def __step_2(word: str, rv: str, r2: str) -> tuple[str, str, str]:
        """
        Step 2: если слово оканчивается на И, удаляем
        """
        if rv.endswith('и'):
            word = word[:-1]
            r2 = r2[:-1]

        return word, rv, r2

    @staticmethod
    def __step_3(word: str, r2: str) -> tuple[str, str]:
        """
        Step 3: если в r2 найдется DERIVATIONAL, удаляем
        """
        for suffix in PorterStemmer.DERIVATIONALS:
            if r2.endswith(suffix):
                word = word[: -len(suffix)]
                break

        return word, r2

    @staticmethod
    def __step_4(word: str) -> str:
        """
        Step 4: 
        - Если слово оканчивается на НН удаляем последнюю букву
        - Если слово оканчивается на SUPERLATIVE удаляем его и повторяем удаление последней буквы Н при НН
        - Если слово оканчивается на Ь удаляем его 
        """
        undouble_success = False
        superlative_removed = False

        if word.endswith('нн'):
            word = word[:-1]
            undouble_success = True

        if not undouble_success:
            for suffix in PorterStemmer.SUPERLATIVES:
                if word.endswith(suffix):
                    word = word[: -len(suffix)]
                    superlative_removed = True
                    break
            if word.endswith('нн'):
                word = word[:-1]

        if not undouble_success and not superlative_removed:
            if word.endswith('ь'):
                word = word[:-1]

        return word
