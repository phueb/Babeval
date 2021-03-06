from typing import List, Tuple, Dict
from functools import partial

from zorro.grammatical import check_agreement_between_two_words
from zorro.agreement_across_RC.shared import templates, copulas_plural, copulas_singular
from zorro.agreement_across_RC.shared import nouns_singular, nouns_plural


prediction_categories = ('correct', )


def categorize_by_template(pairs: List[Tuple[List[str], List[str]]],
                           ) -> Dict[str, List[Tuple[List[str], List[str]]]]:

    template2pairs = {}

    for pair in pairs:
        s1, s2 = pair
        if s1[4].startswith('like') and s2[4].startswith('like'):
            template2pairs.setdefault(templates[0], []).append(pair)
        elif s1[4] == 'there' and s2[4] == 'there':
            template2pairs.setdefault(templates[1], []).append(pair)
        else:
            raise ValueError(f'Failed to categorize {pair} to template.')
    return template2pairs


grammar_checker = partial(check_agreement_between_two_words,
                          nouns_singular,
                          nouns_plural,
                          copulas_singular,
                          copulas_plural,
                          )
