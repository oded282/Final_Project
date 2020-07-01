import re
from Final_Project.utils import sort_file

def generate_graphviz_data(file_name):
    edge_norm = 5
    pattern = re.compile(r'[a-z]+\s*[a-z]*')
    edges_weights = {}
    animals_dict = {}
    parag2link = {}

    with open(file_name, "r", encoding="utf8") as file:

        for line in file:

            data = line.split("|")
            animals_pair = data[0]
            matches = pattern.findall(animals_pair)
            animals = matches[0].replace(" ", "_") + "->" + matches[1].replace(" ", "_")

            link = data[2]
            paragraph = data[3]
            parag2link[animals + ' ' + paragraph] = link

            if animals not in animals_dict:

                edges_weights[animals] = 1
                link = "\n{}".format(link.strip('|').strip('\n'))
                label = "[taillabel=<<table> <tr><td href=\"{}\">link</td></tr> </table>>,label={},penwith={}]" \
                    .format(link.strip('|').strip('\n'), str(edges_weights[animals]),
                            edges_weights[animals] / edge_norm)

                animals_dict[animals] = animals + label


            else:
                edges_weights[animals] += 1
                link = "\n\t<tr><td href=\"{}\">link</td></tr>".format(link)
                index = animals_dict[animals].index('</table>>')
                animals_dict[animals] = (animals_dict.get(animals)[:index] + link + "</table>>,label=" +
                                         str(edges_weights[animals]) + ",penwidth=" +
                                         str((edges_weights[animals] / edge_norm) + 2) + "]")

    with open("data/transmission_graph", "w") as file:
        file.write("digraph prof {\n" + "\tratio = fill;\n" + "\tnode [style=filled, fillcolor=lightblue];\n")
        for val in animals_dict.values():
            file.write("\t" + val + "\n")
        file.write("}")

    return parag2link

def main():
    sort_file("transsmissions_data3")
    parag2link = generate_graphviz_data("sorted_file")




    #TODO 1. Generate transmission_data and filter it
    # 2. build sort function (sort by animal poair)
    # 3. build generate_graphviz (current impl doesn't fit the transmissions graph)
    # 4. create svg file
    # 5. bind between paragraph2link
    # 6. bind between link2id (from svg file)
    # 7. Insert to SVG the info icons
    # 8. Create all the div paragraphs
    # 9. Create javascript code to add events to pop up paragraph.
if __name__ == "__main__":
    main()