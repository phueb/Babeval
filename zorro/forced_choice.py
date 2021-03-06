from typing import List, Tuple, Dict, Callable

from zorro import configs
from zorro.agreement_across_1_adjective.score_forced_choice import prediction_categories


def categorize_choices(pairs: List[Tuple[List[str], List[str]]],
                       grammatical_scores: List[Tuple[bool, bool]],
                       s2cross_entropies: Dict[Tuple[str], float],
                       ) -> Dict[str, float]:
    """
    for each sentence pair in the original, ordered file of test sentences,
     1) the cross entropy assigned to each by a model is retrieved
     2) some syntactic phenomenon (e.g. agreement = True or agreement = False) is evaluated
    When the cross-entropy assigned to the correct choice is higher,
     a value representing "correct" is incremented by one.

    """
    res = {k: 0 for k in prediction_categories}

    # loop over all possible sentence pairs with all possible templates
    num_skipped = 0
    num_false = 0
    for (s1, s2), (is_grammatical1, is_grammatical2) in zip(pairs, grammatical_scores):

        # get cross-entropies
        try:
            xe1 = s2cross_entropies[tuple(s1)]
            xe2 = s2cross_entropies[tuple(s2)]
        except KeyError:  # happens when original test sentences are different than what model was tested with
            # try sentences without punctuation (if model was probed with sentences stripped of punctuation)
            try:
                xe1 = s2cross_entropies[tuple(s1[:-1])]
                xe2 = s2cross_entropies[tuple(s2[:-1])]
            except KeyError:
                num_skipped += 1
                continue

        is_correct1 = is_grammatical1 and xe1 < xe2
        is_correct2 = is_grammatical2 and xe1 > xe2
        if is_correct1 or is_correct2:  # two ways to be correct
            res["correct"] += 1
        else:
            num_false += 1

    num_scored = res["correct"] + num_false
    num_expected_scores = len(pairs)

    if num_scored != num_expected_scores:
        raise RuntimeError(f'Expected {num_expected_scores:,} but got {num_scored:,} scores')

    print(f'correct={res["correct"]:>9,}')
    print(f'false  ={num_false:>9,}')
    print(f'total  ={num_scored :>9,}')
    print(f'skipped={num_skipped :>9,}')
    print()

    return res


def check_pairs_for_grammar(pairs: List[Tuple[List[str], List[str]]],
                            grammar_checker: Callable,
                            ) -> List[Tuple[bool, bool]]:
    nas = (configs.Dirs.external_words / "nouns_ambiguous_number.txt").open().read().split()

    res = []

    for s1, s2 in pairs:
        is_grammatical1 = grammar_checker(s1)
        is_grammatical2 = grammar_checker(s2)

        if len({is_grammatical1, is_grammatical2}) != 2:  # check that only 1 but not both are True
            for na in nas:
                if na in s1:  # a noun with an ambiguous number can cause s1 and s2 to be identical
                    raise RuntimeError('Detected noun with ambiguous number')
            else:
                print(s1, is_grammatical1)
                print(s2, is_grammatical2)
                raise ValueError('Only one sentence per pair can be correct/agree in number.')

        res.append((is_grammatical1, is_grammatical2))

    return res