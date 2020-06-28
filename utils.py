import re

from pattern3.en import pluralize, singularize

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
    with open('graphviz.svg','r') as file:
        for line in file:
            if line.startswith('<polygon fill="none" stroke="#000000" points=') and prev_line == '</g>\n':
                continue

            write_to_file.append(line)
            prev_line = line

    with open('graph.svg','w') as file:
        file.write("\n".join(write_to_file))


def main():
    remove_nodes_from_svg_file()


if __name__ == "__main__":
    main()