import numpy as np
import re
from enum import Enum
import argparse

separators_regex = r'[\s\.\-]+'


class Operation(Enum):
    EQUAL = 1
    INSERTION = 2
    DELETION = 3


def compare(s, t, case_sensitive=True):
    if case_sensitive:
        return s == t
    else:
        return s.lower() == t.lower()


def dist(s, t, split_words=True, case_sensitive=True, deletion_cost=1, insertion_cost=1, substitution_cost=1):
    if split_words:
        s = re.split(separators_regex, s)
        t = re.split(separators_regex, t)

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
            if compare(s[j-1], t[i-1], case_sensitive):
                sub = 0
            else:
                sub = substitution_cost

            d[i, j] = min(
                d[i-1, j] + insertion_cost,
                d[i, j-1] + deletion_cost,
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
                md_s += f'{value}' + separator
                md_t += f'{value}' + separator
        elif op == Operation.INSERTION:
                md_t += f'<{value}>' + separator
        elif op == Operation.DELETION:
                md_s += f'<{value}>' + separator

    with open('out.md', 'w+') as outfile:
        outfile.write(f'{md_s}\n\n')
        outfile.write(f'{md_t}\n\n')

    print(md_s)
    print(md_t)

    return d[m-1, n-1]


def main(s, t, split_words, case_sensitive):
    result = dist(s, t, split_words, case_sensitive, 1, 1, 1)
    print(f'Minimum edit distance: {result}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Compare two strings')
    parser.add_argument('string1', help='The first string to compare')
    parser.add_argument('string2', help='The second string to compare')
    parser.add_argument("-w", "--word", help="Perform comparison on whole words, " +
        "as opposed to on individual characters.", action='store_true')
    parser.add_argument("-i", "--ignore-case", help="Whether ignore case " +
        "when performing comparisons.", action='store_true')
    args = parser.parse_args()

    main(args.string1, args.string2, args.word, not args.ignore_case)