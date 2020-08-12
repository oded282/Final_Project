from py.utils import arrange_animals_list
from data.animal_dictionary import animals_list
from pattern3.en import singularize
import re


def check_animal_in_sentence(animals_set, data, per_animals_list, sentence, complex_sentence_list, link, paragraph):
    animals_in_sentence_set = set()

    for word in sentence.split(" "):
        if word in animals_set:

            singular_animal = singularize(word)

            if singular_animal in animals_set:
                animals_in_sentence_set.add(singular_animal)
            else:
                animals_in_sentence_set.add(word)

    if len(animals_in_sentence_set) < 2:
        return False, False
    if len(animals_in_sentence_set) == 2:
        per_animals_list.append((animals_in_sentence_set.pop(), animals_in_sentence_set.pop()))
        data.append(sentence + "|" + link + "|" + paragraph)
        return True, True

    complex_sentence_list.append((animals_in_sentence_set, sentence + "|" + link + "|" + paragraph))
    return True, False


def filter_1_result_query(file_name, animals_set):
    data = [[]]
    per_animals_list = []
    complex_sentence_list = []
    link_to_articl = []
    link_to_articl_complex_sentence = []
    prev_sent = ""
    with open(file_name, "r", encoding="utf8") as file:
        next(file)
        # data_fix = file.read()
        # data.replace("", "\"")
        for line in file:

            line = line.lower()
            temp = line.split("\t")
            if len(temp) < 17:
                continue

            link = temp[4]
            paragraph = temp[17]
            sentence = temp[16]
            # remove dups results.
            if prev_sent == sentence:
                continue

            check_animal_in_sentence(animals_set, data, per_animals_list, sentence,
                                     complex_sentence_list, link, paragraph)

            prev_sent = sentence
    data.pop(0)
    return data, per_animals_list, complex_sentence_list


def filter_2_result_query(data, per_animals_list):
    results = []
    bed_result = []
    for sentence, pair in zip(data, per_animals_list):

        if re.search(pair[1] + "[^...]*" + "to" + "[^...]*" + pair[0], sentence) or re.search(
                pair[0] + "[^...]*" + "to" + "[^...]*" + pair[1], sentence):
            results.append((pair, sentence))
        else:
            bed_result.append((pair, sentence))

    return results


def write_to_file(result, complex_sentence_list):
    with open("transsmissions_data3", "w", encoding="utf8") as file:
        for index, line in enumerate(result):
            file.write(str(index) + "|" + str(line[0]) + "|" + str(line[1]))

        file.write("\n----------------complex sentence--------------------------\n\n")

        for index, line in enumerate(complex_sentence_list):
            animals_in_sentence, sentence = line[0], line[1]
            file.write(str(index) + "|(" + ",".join(animals_in_sentence) + ")|" + sentence)


def filter_transmit_query():
    animals_set = arrange_animals_list(animals_list)
    result_after_filter_1, per_animals_list_1, complex_sentence_list = filter_1_result_query(
        "data/transmit_query_results3.tsv", animals_set)
    print(result_after_filter_1)
    print(per_animals_list_1)
    result = filter_2_result_query(result_after_filter_1, per_animals_list_1)

    write_to_file(result, complex_sentence_list)


def main():
    print(len(animals_list))
    filter_transmit_query()


if __name__ == "__main__":
    main()
