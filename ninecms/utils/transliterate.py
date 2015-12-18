""" Transliterate unicode characters """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.conf import settings


def transliterate(s, filename=False, to_lower=False):
    """ Transliterate unicode characters
    Currently supporting Greek, Serbian, Russian, Bulgarian
    Priority by order
    :param s: the string to transliterate
    :param filename: if true, different rule for punctuation is followed
    :param to_lower: convert to lowercase
    :return: the transliterated string
    """
    mapping = {
        'el': (
            'αβγδεζηικλμνξοπρστυφωΑΒΓΔΕΖΗΙΚΛΜΝΞΟΠΡΣΤΥΦΩάέίήύόώϊϋΐΰςΆΈΊΉΎΌΏ',
            'abgdeziiklmnxoprstyfoABGDEZIIKLMNXOPRSTYFOaeiiyooiyiysAEIIYOO',
        ),
        'rs': (
            'абвгдезијклмнопрстуфхцАБВГДЕЗИЈКЛМНОПРСТУФХЦ',
            'abvgdezijklmnoprstufhcABVGDEZIJKLMNOPRSTUFHC',
        ),
        'ru': (
            'абвгдезийклмнопрстуфхъыьАБВГДЕЗИЙКЛМНОПРСТУФХЪЫЬ',
            'abvgdezijklmnoprstufh_y_ABVGDEZIJKLMNOPRSTUFH_Y_',
        ),
        'bg': (
            'абвгдезийклмнопрстуфхАБВГДЕЗИЙКЛМНОПРСТУФХ',
            'abvgdeziyklmnoprstufhABVGDEZIYKLMNOPRSTUFH',
        ),
    }
    ext_mapping = {
        'el': (
            ('θ',  'χ',  'ψ',  'Θ',  'Χ',  'Ψ'),
            ('th', 'ch', 'ps', 'Th', 'Ch', 'Ps')
        ),
        'rs': (
            ('ђ',  'ж',  'љ',  'њ',  'ћ', 'ч',  'џ',  'ш',  'Ђ',  'Ж',  'Љ',  'Њ',  'Ћ', 'Ч',  'Џ',  'Ш'),
            ('dj', 'zh', 'lj', 'nj', 'c', 'ch', 'dz', 'sh', 'Dj', 'Zh', 'Lj', 'Nj', 'C', 'Ch', 'Dz', 'Sh'),
        ),
        'rs_latin': (
            ('đ',  'ž',  'ć', 'č',  'š',  'Đ',  'Ž',  'Ć', 'Č',  'Š'),
            ('dj', 'zh', 'c', 'ch', 'sh', 'Dj', 'Zh', 'C', 'Ch', 'Sh'),
        ),
        'ru': (
            ('ж',  'ц',  'ч',  'ш',  'щ',   'ю',  'я',  'Ж',  'Ц',  'Ч',  'Ш',  'Щ',   'Ю',  'Я'),
            ('zh', 'ts', 'ch', 'sh', 'sch', 'ju', 'ja', 'Zh', 'Ts', 'Ch', 'Sh', 'Sch', 'Ju', 'Ja'),
        ),
        'bg': (
            ('ж',  'ц',  'ч',  'ш',  'щ',   'ю',  'я',  'Ж',  'Ц',  'Ч',  'Ш',  'Щ',   'Ю',  'Я'),
            ('zh', 'ts', 'ch', 'sh', 'sht', 'yu', 'ya', 'Zh', 'Ts', 'Ch', 'Sh', 'Sht', 'Yu', 'Ya'),
        ),
    }
    for lang in mapping:
        s = s.translate(str.maketrans(mapping[lang][0], mapping[lang][1]))
    for lang in ext_mapping:
        for i, val in enumerate(ext_mapping[lang][0]):
            s = s.replace(ext_mapping[lang][0][i], ext_mapping[lang][1][i])
    # "'`,.-_:;|{[}]+=*&%^$#@!~()?<>/\
    remove = settings.TRANSLITERATE_REMOVE
    if filename:
        remove += '/\?%*:|"<>'
        s = s.replace(' ', '_')
    else:
        s = s.translate(str.maketrans(settings.TRANSLITERATE_REPLACE[0], settings.TRANSLITERATE_REPLACE[1]))
    s = s.translate({ord(i): None for i in remove})
    if to_lower:
        s = s.lower()
    return s


def upper_no_intonation(s):
    """ Convert a string to uppercase, removing any intonation
    :param s: the string to convert
    :return: the converted string
    """
    mapping = ('ΆΈΊΉΎΌΏ', 'ΑΕΙΗΥΟΩ')
    s = s.upper()
    s = s.translate(str.maketrans(mapping[0], mapping[1]))
    return s
