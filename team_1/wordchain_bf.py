import re
import argparse


def neighbours(cands, w1):
    return [cand for cand in cands if sum(l1 != l2 for l1, l2 in zip(cand, w1)) == 1]


def find_shortest_path(first_word, second_word, dict, DEBUG):
    # Load the dictionary, discarding words with apostrophes, accents or mixed case
    dictionary = [word[:-1].lower() for word in open(dict).readlines()
                   if re.match(r'([a-z]+|[A-Z]+)\n', word)]

    if len(first_word) != len(second_word):
        raise Exception("Words must be the same length.")

    candidates = [x for x in dictionary if len(x) == len(first_word)]
    print 'Using a dictionary with %d %d-letter words' % (len(candidates), len(candidates[0]))

    paths = [[first_word]]
    candidates.remove(first_word)
    solution = False

    while not solution:
        new_paths = []
        for path in paths:
            for neighbour in list(neighbours(candidates, path[-1])):
                candidates.remove(neighbour)
                new_paths.append(path + [neighbour])
                if neighbour == second_word:
                    solution = True
                    return path + [neighbour]
                if DEBUG:
                    print path + [neighbour]
        if not new_paths:
            return None
        paths = new_paths
        print 'Found %d partial chains of %d words.' % (len(paths), len(paths[0]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Wordchains!')
    parser.add_argument('-v', dest='DEBUG', action='store_true', help='display all intermediary chains found')
    parser.add_argument('-d', dest='dict', default='/usr/share/dict/words', help='dictionary to use')
    parser.add_argument('start', help='start word')
    parser.add_argument('end', help='destination word')
    args = parser.parse_args()
    path = find_shortest_path(args.start, args.end, args.dict, args.DEBUG)
    if path:
        print 'Solution in %d steps:' % (len(path) - 1), path
    else:
        print 'No solution'
