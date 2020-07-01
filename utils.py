import re


# from pattern3 import pluralize, singularize


# This function used to create to files from the animal dictionary we find in the internet.
# The dictionary contains an animal common name, and the scientific name related to the common one.
# We separated the names into two files, common names file and scientific names file.
def create_animals_files(all_animals_file, common_names_file, scientific_names_file):
    with open(all_animals_file) as ofd:
        with open(common_names_file, 'w') as rfd:
            with open(scientific_names_file, 'w') as sfd:
                line = ofd.readline()
                regular_name = True
                dict = []
                while line:
                    line = line.strip('\n')
                    match = re.fullmatch('[A-Z]top', line)

                    if "(unidentified)" in line:
                        line = line.split(' ')[0]

                    if ',' in line:
                        names = line.split(',')
                        line = (names[0])

                    if line != '' and match is None and line not in dict:
                        if regular_name:
                            line = line.split(' ')[-1]
                            rfd.write(line.lstrip().rstrip() + '|')
                            regular_name = False
                        else:
                            sfd.write(line.lstrip().rstrip() + '|')
                            regular_name = True

                        dict.append(line)

                    line = ofd.readline()


def arrange_animals_list(animals):
    all_animal_set = set()
    plural_animal_name = ''
    special_animals_dic = {'cow': 'cows', 'silvestris': 'silvestrium'}

    for animal in animals:

        if animal in special_animals_dic.keys():
            plural_animal_name = special_animals_dic[animal]

        elif animal in all_animal_set:
            continue

        elif singularize(animal) == animal:
            plural_animal_name = pluralize(animal.lower())
        else:
            temp = animal.lower()
            plural_animal_name = animal.lower()
            animal = singularize(temp).lower()

        all_animal_set.add(plural_animal_name.lower())
        all_animal_set.add(animal.lower())

    all_animal_set.remove('')
    all_animal_set.remove('s')

    return all_animal_set


def remove_nodes_from_svg_file():
    write_to_file = []
    prev_line = ""
    with open('graphviz.svg', 'r') as file:
        for line in file:
            if line.startswith('<polygon fill="none" stroke="#000000" points=') and prev_line == '</g>\n':
                continue

            write_to_file.append(line)
            prev_line = line

    with open('graph.svg', 'w') as file:
        file.write("\n".join(write_to_file))


def sort_file(file_name):
    data = []
    with open(file_name, "r", encoding="utf8") as file:
        for line in file:
            data.append("|".join(line.split("|")[:]))

    data.sort()
    with open("sorted_file", "w", encoding="utf8") as file:
        file.write("".join(data))


def create_divs(id2paragraph):
    divs_list = []

    for id, parg in id2paragraph.items():
        div_string = "<div id=\"info_" + id + "\">\n<h3>paragraph source</h3>\n<p>" + parg + "</p>\n</div>"
        divs_list.append(div_string)

    with open("div_file", "w", encoding="utf8") as file:
        file.write("\n\n".join(divs_list))


def create_id2para(file_name):
    id2paragraph = {}

    with open(file_name, "r", encoding="utf8")as file:
        old_pairs = []
        pair_counter = 0
        for index, line in enumerate(file):
            temp = line.split("|")
            pair = temp[0]
            paragraph = temp[3]
            if pair not in old_pairs:
                pair_counter += 1
                old_pairs.append(pair)
            id2paragraph.update({"a_edge" + str(pair_counter) + "_" + str(index): paragraph})

    return id2paragraph


def bind_ids(id2paragraph, ids):
    keys = id2paragraph.keys()
    new_dic = {}
    pass_list = []
    for key in id2paragraph.keys():

        if key in pass_list:
            continue

        pattern1 = re.compile(r'a_edge\d+_')
        result1 = [i for i in ids if i.startswith(pattern1.findall(key)[0])]
        result2 = [i for i in id2paragraph.keys() if i.startswith(pattern1.findall(key)[0])]
        for id_bad, id_good in zip(result2, result1):
            new_dic.update({id_good: id2paragraph[id_bad]})
            pass_list.append(id_bad)

    return new_dic


def main():
    # id2paragraph = {
    #     "a_edge1_0": "jsdhfjdnjxn;cvjnzxjccxbjmb xnmchnjcn mxcnnnnnnnnnnnnnnnnnnnnnnnnmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmxcjhkxhc jhxchxjchxjcnxcjn",
    #     "a_edge1_1": "ssssssssssssssssssssssssssssssssssssssssssssssssss sssssssssssssss dk                   kdddddddddddd kddddddddddddddddddddddddddddddddddddddddddddd",
    #     "a_edge1_2": "jsdhfjdnjxn;cvjnzxjccxbjmb xnmchnjcn mxcnnnnnnnnnnnnnnnnnnnnnnnnmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmxcjhkxhc jhxchxjchxjcnxcjn",
    #     "a_edge1_3": "ssssssssssssssssssssssssssssssssssssssssssssssssss sssssssssssssss dk                   kdddddddddddd kddddddddddddddddddddddddddddddddddddddddddddd",
    #     "a_edge2_4": "jsdhfjdnjxn;cvjnzxjccxbjmb xnmchnjcn mxcnnnnnnnnnnnnnnnnnnnnnnnnmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmxcjhkxhc jhxchxjchxjcnxcjn",
    #     "a_edge2_5": "ssssssssssssssssssssssssssssssssssssssssssssssssss sssssssssssssss dk                   kdddddddddddd kddddddddddddddddddddddddddddddddddddddddddddd",
    #     "a_edge2_6": "jsdhfjdnjxn;cvjnzxjccxbjmb xnmchnjcn mxcnnnnnnnnnnnnnnnnnnnnnnnnmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmxcjhkxhc jhxchxjchxjcnxcjn",
    #     "a_edge2_7": "ssssssssssssssssssssssssssssssssssssssssssssssssss sssssssssssssss dk                   kdddddddddddd kddddddddddddddddddddddddddddddddddddddddddddd",
    # }
    # create_divs(id2paragraph)
    id2paragraph = create_id2para("sorted_file")
    #bind_ids(id2paragraph, id2paragraph.keys())


if __name__ == "__main__":
    main()
