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
    with open('Graph/graph_img.svg', 'r', encoding="utf8") as file:
        for line in file:
            if line.startswith('<polygon fill="none" stroke="#000000" points=') and prev_line == '</g>\n':
                continue

            write_to_file.append(line)
            prev_line = line

    with open('Graph/graph_img.svg', 'w', encoding="utf8") as file:
        file.write(" ".join(write_to_file))


def sort_file(file_name):
    data = []
    with open(file_name, "r", encoding="utf8") as file:
        for line in file:
            data.append("|".join(line.split("|")[:]))

    data.sort()
    with open("sorted_file", "w", encoding="utf8") as file:
        file.write("".join(data))


def remove_unnecessary_space(str):
    temp = str
    count = 0
    open_apostrophe = True
    for index, char in enumerate(temp):
        if (
                char == ',' or char == '.' or char == ')' or char == ";" or char == ']' or char == '%' or char == '’' or char == ':' or char == '-') and \
                temp[index - 1] == ' ':
            str = str[:index - 1 - count] + str[index - count:]
            count += 1

        if (char == '(' or char == '[' or char == '-') and temp[index + 1] == ' ':
            str = str[:index + 1 - count] + str[index - count + 2:]
            count += 1
            open_apostrophe = True

        if char == '\'' and not open_apostrophe and temp[index - 1] == ' ':
            str = str[:index - 1 - count] + str[index - count:]
            count += 1
            open_apostrophe = True

        elif char == '\'' and open_apostrophe and temp[index + 1] == ' ':
            str = str[:index + 1 - count] + str[index - count + 2:]
            count += 1
            open_apostrophe = False

    return str


def create_divs(id2paragraph):
    divs_list = []

    for id, parg in id2paragraph.items():
        temp = parg.split("|")
        parg = temp[0]
        sentence = temp[1]

        parg = remove_unnecessary_space(parg)
        sentence = remove_unnecessary_space(sentence)

        try:
            start_index = parg.index(sentence)
        except:
            print(parg + '\n')
            print(sentence)
            print("---------------------------------------------------")
            continue
        parg = parg[:start_index] + "<b>" + sentence + "</b>" + parg[start_index + len(sentence):]

        div_string = "<div id=\"info_" + id + "\" class= \"paragraph\">\n<h3>paragraph source</h3>\n<p>" + parg + "</p>\n</div>"
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
            sentence = temp[1]
            paragraph = temp[3]
            if pair not in old_pairs:
                pair_counter += 1
                old_pairs.append(pair)
            id2paragraph.update({"a_edge" + str(pair_counter) + "_" + str(index): paragraph + "|" + sentence})

    return id2paragraph


def bind_ids(id2paragraph, ids):
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


def design_graph(file_name):
    pattern1 = re.compile(r'cx="-*\d+\.\d+"')
    pattern2 = re.compile(r' x="-*\d+\.\d+"')
    pattern3 = re.compile(r'a_edge\d+_\d+')
    pattern4 = re.compile(r'cy="-*\d+\.\d+"')
    pattern5 = re.compile(r' y="-*\d+\.\d+"')
    # pattern5 = re.compile(r'fill="#[A-Z0-9]+"')
    new_file = []

    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if "<polygon fill=\"none\" stroke=\"#000000\"" in line:
                continue

            if "link to article" in line:
                fill_index = line.index("fill")
                new_line = line[:6] + "text-decoration=\"underline\" " + line[6:fill_index + 7] + "0BF5D7" \
                           + line[fill_index + 13:]
                new_file.append(new_line)
                continue

            if "class=\"icon\"" in line:
                cxpoints = [float(cx[4:-1]) for cx in pattern1.findall(line)]
                xpoint = float(pattern2.findall(line)[0][4:-1])
                id = pattern3.findall(line)[0]
                cypoints = [float(cy[4:-1]) for cy in pattern4.findall(line)]
                ypoint = float(pattern5.findall(line)[0][4:-1])

                new_line = "<g id=\"icon_{}\" class=\"icon\" pointer-events=\"all\">" \
                           "<circle cx=\"{}\" cy=\"{}\" r=\"8\" fill=\"none\" stroke=\"gold\" " \
                           "stroke-width=\"1.5\"/>" \
                           "<circle cx=\"{}\" cy=\"{}\" r=\"0.75\" fill=\"gold\"/>" \
                           "<rect x=\"{}\" y=\"{}\" width=\"1\" height=\"6\" fill=\"gold\"/></g></a>" \
                    .format(id, cxpoints[0] + 48.0, cypoints[0], cxpoints[1] + 48.0, cypoints[1], xpoint + 48.0, ypoint)

                new_file.append(new_line)
                continue

            new_file.append(line)

        with open("new_graph.html", "w", encoding="utf-8") as f:
            f.write("\n".join(new_file))


def merge_files(old_file_name, current_file_name):
    new_file_data = []
    isfind = False
    with open(old_file_name, "r", encoding="utf8") as old_file:

        for line in old_file:
            isfind = False
            temp = line.split("|")
            sentence = temp[2]

            with open(current_file_name, "r", encoding="utf8") as current_file:

                for index, current_line in enumerate(current_file):
                    current_temp = current_line.split("|")
                    current_sentence = current_temp[2]

                    if current_sentence == sentence:
                        new_file_data.append(line.replace("\n", "") + "|" + current_temp[4].replace("\n", ""))
                        isfind = True
                        break

            print(isfind)

    with open("transmissions_data_new", "w", encoding="utf8") as new_file:
        new_file.write("\n".join(new_file_data))


def sort_file(file_name):
    data = []
    with open(file_name, "r", encoding="utf8") as file:
        for line in file:
            data.append("|".join(line.split("|")[1:]))

    data.sort()
    with open("sorted_file", "w", encoding="utf8") as file:
        file.write("".join(data))

def LDA_coherency_graph():
    import matplotlib.pyplot as plt

    # x axis values
    topcis = [20, 50, 150, 200, 300, 400]
    # corresponding y axis values
    coherency = [0.5743, 0.5989,0.6028,0.607,0.5979,0.597]

    # plotting the points
    plt.plot(topcis, coherency, color='green', linestyle='dashed', linewidth=3,
             marker='o', markerfacecolor='blue', markersize=12)


    # naming the x axis
    plt.xlabel('Topics')
    # naming the y axis
    plt.ylabel('Coherency')

    # giving a title to my graph
    plt.title('LDA Model Evaluation')

    plt.savefig("lda_eval.png")

    # function to show the plot
    # plt.show()


def main():
    LDA_coherency_graph()

if __name__ == '__main__':
    main()