import re
import sys

dictionary = [word.lower().strip() for word in
    open('/usr/share/dict/words').readlines() if re.match(r'\w+', word)]


def neighbours(cands, w1):
    for cand in cands:
        if sum(l1 != l2 for l1, l2 in zip(cand, w1)) == 1:
            yield cand


def find_shortest_path(first_word, second_word):
    if len(first_word) != len(second_word):
        raise Exception("Words must be the same length.")

    candidates = [x for x in dictionary if len(x) == len(first_word)]
    print 'Using a dictionary with %d %d-letter words' % (len(candidates), len(candidates[0]))

    paths = [[first_word]]

    while True:
        print 'Found %d partial chains of %d words.' % (len(paths), len(paths[0]))
        new_paths = []
        for path in paths:
            for neighbour in neighbours(candidates, path[-1]):
                if neighbour == second_word:
                    path.append(neighbour)
                    return path
                candidates.remove(neighbour)
                new_paths.append(path + [neighbour])
        if not new_paths:
            return None
        paths = new_paths


if __name__ == "__main__":
    print '\n', find_shortest_path(sys.argv[1], sys.argv[2])
