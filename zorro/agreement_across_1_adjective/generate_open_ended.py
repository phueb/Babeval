
from zorro import configs
from zorro.agreement_across_1_adjective.shared import task_name, pre_nominals_singular, pre_nominals_plural
from zorro.task_words import get_task_word_combo

NUM_ADJECTIVES = 100

template1 = 'look at {} {}' + f' {configs.Data.mask_symbol} ' + '.'
template2 = '{} {}' + f' {configs.Data.mask_symbol} ' + 'went there .'


def main():
    """
    example:
    "look at this green <mask> .
    "these green <mask> went there .
    """

    for pre_nominal in pre_nominals_singular + pre_nominals_plural:

        for adj, in get_task_word_combo(task_name,
                                        [('JJ', 0, NUM_ADJECTIVES),
                                         ]):
            yield template1.format(pre_nominal, adj)
            yield template2.format(pre_nominal, adj)


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n:>12,}', s)
