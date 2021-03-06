from typing import List, Tuple, Dict
from functools import partial

from zorro.grammatical import check_agreement_between_two_words
from zorro.agreement_between_neighbors.shared import templates, pre_nominals_plural, pre_nominals_singular
from zorro.agreement_between_neighbors.shared import nouns_singular, nouns_plural


prediction_categories = ('correct', )


def categorize_by_template(pairs: List[Tuple[List[str], List[str]]],
                           ) -> Dict[str, List[Tuple[List[str], List[str]]]]:

    template2pairs = {}

    for pair in pairs:
        s1, s2 = pair
        if s1[2] == 'must' and s2[2] == 'must':
            template2pairs.setdefault(templates[0], []).append(pair)
        elif s1[2] == 'can' and s2[2] == 'can':
            template2pairs.setdefault(templates[1], []).append(pair)
        else:
            raise ValueError(f'Failed to categorize {pair} to template.')
    return template2pairs


grammar_checker = partial(check_agreement_between_two_words,
                          pre_nominals_singular,
                          pre_nominals_plural,
                          nouns_singular,
                          nouns_plural,
                          )

