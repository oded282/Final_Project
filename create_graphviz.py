import re

def main():

    pattern = re.compile(r'[a-z]+')
    results = ""
    pairs = {}
    dict = {}

    with open("transsmission_between_animals", "r", encoding="utf8") as file:
        line = file.readline()
        is_link = False
        while line:

            if is_link:
                label = "[label=<<table> <tr><td href={}>link</td></tr> </table>>]"\
                    .format(line.strip('|').strip('\n')) + '\n'
                dict[animals] += label
                is_link = False
            else:
                animals_pair = line.split('|')[1]
                matches = pattern.findall(animals_pair)
                animals = matches[0] + "->" + matches[1]

                if animals in dict:
                    link = file.readline()
                    link = "<tr><td href={}>link</td></tr>".format(link.strip('|'.strip('\n')))
                    temp = dict[animals][-11:]
                    dict[animals] = (dict.get(animals)[:-11] + link + temp)
                    line = file.readline()
                    continue

                dict[animals] = animals
                is_link = True

            line = file.readline()



if __name__ == "__main__":
    main()