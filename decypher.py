import copy

# template = """123 456267 8290 5 7ABC0
# 8C6 D1E6F BGCF0 C2 H741
# 58 C6843C GCD I107
# F680E 8H3C4J"""

template = """012 3240125 67 2805292AB C6D2 0EF4B"""


def read_doc(path):
    with open(path, 'r') as doc:
        dictionary = {}
        [dictionary.setdefault(len(w[:-1]), []).append(w[:-1]) for w in doc.readlines()]
        return dictionary


def print_result(r, t, forbidden_letters):
    for k, v in r.items():
        t = t.replace(k, v)
    print(''.join([l if (l in forbidden_letters or l == ' ') else '_' for l in t]))


def translate(w, d):
    return ''.join([d[l] if l in d else '_' for l in w])


def create_dictionary():
    pass


def all_letters_translated(w, d):
    for l in w:
        if l not in d:
            return False
    return True


def create_find_word(w, dictionary):
    f_w = ''
    duplicate_letters = []
    for l in w:
        if l in dictionary:
            f_w += dictionary[l]
        else:
            if w.count(l) > 1:
                duplicate_letters = [pos for pos, char in enumerate(w) if char == l]
            f_w += '_'
    forbidden_letters = [v for v in dictionary.values()]
    return f_w, duplicate_letters, forbidden_letters

def find_viable_words(eng_words, find_word, duplicate_letters, forbidden_letters):
    indices = list(range(len(eng_words[len(find_word)])))
    for l_i, l in enumerate(find_word):
        if l != '_':
            viable_indices = []
            for i in indices:
                if eng_words[len(find_word)][i][l_i] == find_word[l_i]:
                    viable_indices.append(i)
            indices = viable_indices
        else:
            viable_indices = []
            for i in indices:
                if eng_words[len(find_word)][i][l_i] not in forbidden_letters:
                    viable_indices.append(i)
            indices = viable_indices


    res = []
    for i in indices:
        if duplicate_letters and eng_words[len(find_word)][i][duplicate_letters[0]] != eng_words[len(find_word)][i][duplicate_letters[1]]:

            continue

        res.append(eng_words[len(find_word)][i])

    return res


def expand_dictionary(word, applied_word, dictionary):
    for f_l, a_l in zip(word, applied_word):
        if f_l not in dictionary:
            dictionary[f_l] = a_l
    return dictionary


def num_words_in_dict(template_words_enc, eng_words, dictionary):
    num = 0
    for word in template_words_enc:
        t_w = translate(word, dictionary)
        if t_w in eng_words[len(t_w)]:
            num += 1
    return num


def fill_dictionary(encoded_word_id, dictionary, depth=0, parent_w=''):
    if len(template_words_enc) == encoded_word_id:
        print_result(dictionary, template, 'abcdefghijklmnopqrstuvwxyz')
        return

    find_word, duplicate_letters, forbidden_letters = create_find_word(template_words_enc[encoded_word_id], dictionary)
    viable_words = find_viable_words(eng_words, find_word, duplicate_letters, forbidden_letters)

    for viable_word in viable_words:
        new_dictionary = copy.deepcopy(dictionary)
        expanded_dictionary = expand_dictionary(template_words_enc[encoded_word_id], viable_word, new_dictionary)
        fill_dictionary(encoded_word_id + 1, expanded_dictionary, depth=depth+1, parent_w=viable_word)


template_words_enc = sorted(template.split(), key=lambda x: len(x), reverse=True)
# eng_words = read_doc('words_alpha.txt')
eng_words = read_doc('data/google-10000-english-no-swears.txt')
fill_dictionary(0, {})
