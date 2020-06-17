import re

def main():

    edge_norm = 2
    pattern = re.compile(r'[a-z]+\s*[a-z]*')
    weight_counter = {}
    dict = {}

    with open("transsmissions_data", "r", encoding="utf8") as file:
        line = file.readline()
        is_link = False
        while line:

            if is_link:
                label = "[taillabel=<<table> <tr><td href=\"{}\">link</td></tr> </table>>,label={},penwith={}]"\
                    .format(line.strip('|').strip('\n'), str(weight_counter[animals]),
                            weight_counter[animals] / edge_norm)
                dict[animals] += label
                is_link = False
            else:
                animals_pair = line.split('|')[1]
                matches = pattern.findall(animals_pair)
                animals = matches[0].replace(" ", "_") + "->" + matches[1].replace(" ", "_")

                if animals in dict:
                    link = file.readline()
                    link = "\n\t<tr><td href=\"{}\">link</td></tr>".format(link.strip('|').strip('\n'))
                    weight_counter[animals] += 1
                    index = dict[animals].index('</table>>')
                    dict[animals] = (dict.get(animals)[:index] + link + "</table>>,label=" + str(weight_counter[animals])
                                     + ",penwidth=" + str(weight_counter[animals] / edge_norm) + "]")
                    line = file.readline()
                    continue

                weight_counter[animals] = 1
                dict[animals] = animals
                is_link = True

            line = file.readline()

        with open("data/transmission_graph", "w") as file:
            file.write("digraph prof {\n" + "\tratio = fill;\n" + "\tnode [style=filled, fillcolor=lightblue];\n")
            for val in dict.values():
                file.write("\t"+val + "\n")
            file.write("}")


if __name__ == "__main__":
    main()