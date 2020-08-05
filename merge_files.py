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


def main():
    merge_files("transsmissions_data", "transsmissions_data3")
    # sort_file("transmissions_data_new")


if __name__ == "__main__":
    main()
