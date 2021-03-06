from typing import Tuple, List


def check_agreement_between_two_words(
        words_left_s: List[str],  # possible words for left word position, singular
        words_left_p: List[str],  # possible words for left word position, plural
        words_right_s: List[str],  # possible words for right word position, singular
        words_right_p: List[str],  # possible words for right word position, plural
        sentence: List[str],
) -> bool:
    """
    find two words in sentence which must agree (e.g. "this" and "dog") in a single 'for' loop.

    warning: word_left must occur before word_right in sentence

    how it works:
    of the three temporary objects in each iteration, only 2 are defined, while the other are of NoneType.
    in theory, this prevents need to search through right words and left words again, to determine their number.
    """
    wls = None  # left singular
    wlp = None  # left plural
    wrs = None  # right singular
    wrp = None  # right plural
    for wr, wl in zip(sentence, reversed(sentence)):
        if wls is None and wlp is None and wr in words_left_s:
            wls = wr
        elif wls is None and wlp is None and wr in words_left_p:
            wlp = wr
        if wrs is None and wrp is None and wl in words_right_s:
            wrs = wl
        elif wrs is None and wrp is None and wl in words_right_p:
            wrp = wl

    return True if (wls and wrs) or (wlp and wrp) else False