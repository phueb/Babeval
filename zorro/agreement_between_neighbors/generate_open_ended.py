

from zorro.agreement_between_neighbors import *

template = 'look at {}' + f' {configs.Data.mask_symbol} ' + '.'


def main():
    """
    example:
    "look at this [MASK]"
    """

    for pre_nominal in pre_nominals:
        yield template.format(pre_nominal)