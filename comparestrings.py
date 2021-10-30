import numpy as np
from enum import Enum
import argparse


class Operation(Enum):
    EQUAL = 1
    INSERTION = 2
    DELETION = 3


def dist(s, t, split_words=True, deletion_cost=1, insertion_cost=1, substitution_cost=1):
    if split_words:
        s = s.split(' ')
        t = t.split(' ')

    m = len(t) + 1
    n = len(s) + 1
    d = np.zeros((m, n), np.int32)

    # Prefixes can be transformed into empty string by dropping all chars.
    for i in range(1, n):
        d[0, i] = i

    for i in range(1, m):
        d[i, 0] = i

    for j in range(1, n):
        for i in range(1, m):
            if s[j-1] == t[i-1]:
                sub = 0
            else:
                sub = substitution_cost

            d[i, j] = min(
                d[i-1, j] + 1,
                d[i, j-1] + 1,
                d[i-1, j-1] + sub
            )

    # Print matrix
    # print(d)

    # Reconstruction
    stack = []
    x, y = (m-1, n-1)
    while x > 0 and y > 0:
        if x == 0:
            ops = [(Operation.DELETION, s[y-1])]
            y -= 1
            continue
        elif y == 0:
            ops = [(Operation.INSERTION, t[x-1])]
            x -= 1
        else:
            minimum = min(d[x-1, y-1], d[x-1, y], d[x, y-1])
            if d[x-1, y-1] == minimum:
                if d[x-1, y-1] == d[x, y]:
                    ops = [(Operation.EQUAL, s[y-1])]
                else:
                    ops = [(Operation.DELETION, s[y-1]), (Operation.INSERTION, t[x-1])]
                x, y = (x-1, y-1)
            elif d[x-1, y] == minimum:
                ops = [(Operation.INSERTION, t[x-1])]
                x -= 1
            elif d[x, y-1] == minimum:
                ops = [(Operation.DELETION, s[y-1])]
                y -= 1
        stack.extend(ops)

    # If we're splitting the strings by words, we need to separate them when outputting
    if split_words:
        separator = ' '
    else:
        separator = ''

    md_s = ''
    md_t = ''
    while stack:
        op, value = stack.pop()
        if op == Operation.EQUAL:
                md_s += f'{value.lower()}' + separator
                md_t += f'{value.lower()}' + separator
        elif op == Operation.INSERTION:
                md_t += f'{value.upper()}' + separator
        elif op == Operation.DELETION:
                md_s += f'{value.upper()}' + separator

    with open('out.md', 'w+') as outfile:
        outfile.write(f'{md_s}\n\n')
        outfile.write(f'{md_t}\n\n')

    return d[m-1, n-1]


def main(s, t, split_words):
    print(f'{s} {t}')
    result = dist(s, t, split_words, 1, 1, 1)
    print(f'Minimum edit distance: {result}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Compare two strings')
    parser.add_argument('string1', help='The first string to compare')
    parser.add_argument('string2', help='The second string to compare')
    parser.add_argument("-w", "--word", help="Perform comparison on whole words, " +
        "as opposed to on individual characters.", action='store_true')
    args = parser.parse_args()
    print(args.word)

    main(args.string1, args.string2, args.word)