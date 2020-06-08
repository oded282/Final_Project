import matplotlib.pyplot as plt
import numpy as np

# This function plot the bars graph
def simple_bar_graph(animals_names, all_animals):

    N = len(all_animals)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.2  # the width of the bars
    fig = plt.figure(figsize=(8, 6), edgecolor='red')
    ax = fig.add_subplot(111)

    yvals = all_animals
    rects1 = ax.bar(ind, yvals, width, edgecolor="black", linewidth=0.6, color='paleturquoise')

    ax.set_ylabel('Animal frequency')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(tuple(animals_names))

    autolabel(rects1, ax)

    plt.show()


def autolabel(rects, ax):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.00 * h, '%d' % int(h),
                ha='center', va='bottom')


# This function plot the two bars graph.
def complex_bar_graph(animals_names, count_overall_animals, count_corona_related = None):

    N = 3
    ind = np.arange(N)  # the x locations for the groups
    width = 0.3  # the width of the bars

    fig = plt.figure(figsize=(8, 6), edgecolor='red')
    ax = fig.add_subplot(111)

    yvals = count_overall_animals
    rects1 = ax.bar(ind, yvals, width, edgecolor="black", linewidth=0.6, color='paleturquoise')
    zvals = count_corona_related
    rects2 = ax.bar(ind, zvals, width, edgecolor="black", linewidth=0.6, color='cadetblue', alpha=.7)

    ax.set_ylabel('Scores')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(tuple(animals_names))
    ax.legend((rects1[0], rects2[0]), ('y', 'z'))

    autolabel(rects1, ax)
    autolabel(rects2, ax)

    plt.show()
