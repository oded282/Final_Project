import re
from py.utils import create_divs, create_id2para, bind_ids, remove_nodes_from_svg_file


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


def add_icon_to_svg(r_file_name, w_file_name):
    pattern1 = re.compile(r'a_edge\d+_\d+')
    pattern2 = re.compile(r'x="-*\d+\.\d+"')
    pattern3 = re.compile(r'y="-*\d+\.\d+"')
    all_ids = []

    with open(r_file_name, "r", encoding="utf8") as r_file, open(w_file_name, "w") as w_file:
        line = r_file.readline()

        while line:

            if "xlink:href" in line:
                id = pattern1.findall(line)[0]
                all_ids.append(id)
                w_file.write(line)  # write the xlink line
                line = r_file.readline()
                w_file.write(line)  # write line
                line = r_file.readline()
                w_file.write(line)

                x = float(pattern2.findall(line)[0][3:-1])
                y = float(pattern3.findall(line)[0][3:-1])

                w_file.write("<g id=\"icon_{}\" class=\"icon\" pointer-events=\"all\">"
                             "<circle cx=\"{}\" cy=\"{}\" r=\"8\" fill=\"none\" stroke=\"gold\" "
                             "stroke-width=\"1.5\"/>"
                             "<circle cx=\"{}\" cy=\"{}\" r=\"0.75\" fill=\"gold\"/>"
                             "<rect x=\"{}\" y=\"{}\" width=\"1\" height=\"6\" fill=\"gold\"/></g>"
                             .format(id, x + 38.052, y - 3.0676, x + 38.052, y - 7.0676, x + 37.552, y - 5.0676))
            else:
                w_file.write(line)

            line = r_file.readline()
    return all_ids


def main():
    remove_nodes_from_svg_file()
    ids = add_icon_to_svg("Graph/graph_img.svg", "data/graphviz2.svg")
    id2paragraph = create_id2para("sorted_file")
    id2paragraph = bind_ids(id2paragraph, ids)
    create_divs(id2paragraph)


if __name__ == "__main__":
    main()
