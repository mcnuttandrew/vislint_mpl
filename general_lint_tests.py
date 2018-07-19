"""
The tests for the vislint library
"""

import matplotlib.pyplot as plt
import numpy as np

from vislint import vislint

DEFAULT_CONFIGURATION = {}

def generic_scatterplot():
    """
    Generate a basic scatterplot object, returns an axes object and a figure object
    """
    # Data for plotting
    t_vals = np.arange(0.0, 2.0, 0.01)
    s_vals = 1 + np.sin(2 * np.pi * t_vals)

    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure() and then ax = fig.add_subplot(111)
    fig, axes = plt.subplots()
    axes.plot(t_vals, s_vals)
    return (axes, fig)

def test_simple_line_chart():
    """
    Test a line chart
    """
    (axes, fig) = generic_scatterplot()

    assert vislint(axes, fig, DEFAULT_CONFIGURATION) == [
        ("require-titles", 'Titles are required'),
        ("no-short-titles", 'Short titles are not allowed (must be greater than 1 word)'),
        ("require-axes", 'Axes must be labeled'),
        ("require-legend", 'A legend must be used')]

    axes.set(xlabel="time (s)", ylabel="voltage (mV)",
             title="About as simple as it gets, folks")

    assert vislint(axes, fig, DEFAULT_CONFIGURATION) == [
        ("require-legend", 'A legend must be used')
    ]

    axes.legend("Example legend")
    assert vislint(axes, fig, DEFAULT_CONFIGURATION) == []


def test_reading_level():
    """
    Test reading level functions
    """
    (axes, fig) = generic_scatterplot()

    reading_level_config = {
        "require-titles": True,
        "no-short-titles": True,
        "require-axes": False,
        "require-legend": False,
        "sentencify": True,
        "no-complex-titles": True
    }


    axes.set(title="About as simple as it gets, folks")
    assert vislint(axes, fig, reading_level_config) == []


    proust_block = """But I had seen first one and then another of the rooms in which I had slept during my life, and in the end I would revisit them all in the long course of my waking dream: rooms in winter, where on going to bed I would at once bury my head in a nest, built up out of the most diverse materials, the corner of my pillow, the top of my blankets, a piece of a shawl, the edge of my bed, and a copy of an evening paper, all of which things I would contrive, with the infinite patience of birds building their nests, to cement into one whole; rooms where, in a keen frost, I would feel the satisfaction of being shut in from the outer world (like the sea-swallow which builds at the end of a dark tunnel and is kept warm by the surrounding earth), and where, the fire keeping in all night, I would sleep wrapped up, as it were, in a great cloak of snug and savoury air, shot with the glow of the logs which would break out again in flame: in a sort of alcove without walls, a cave of warmth dug out of the heart of the room itself, a zone of heat whose boundaries were constantly shifting and altering in temperature as gusts of air ran across them to strike freshly upon my face, from the corners of the room, or from parts near the window or far from the fireplace which had therefore remained cold—or rooms in summer, where I would delight to feel myself a part of the warm evening, where the moonlight striking upon the half-opened shutters would throw down to the foot of my bed its enchanted ladder; where I would fall asleep, as it might be in the open air, like a titmouse which the breeze keeps poised in the focus of a sunbeam—or sometimes the Louis XVI room, so cheerful that I could never feel really unhappy, even on my first night in it: that room where the slender columns which lightly supported its ceiling would part, ever so gracefully, to indicate where the bed was and to keep it separate; sometimes again that little room with the high ceiling, hollowed in the form of a pyramid out of two separate storeys, and partly walled with mahogany, in which from the first moment my mind was drugged by the unfamiliar scent of flowering grasses, convinced of the hostility of the violet curtains and of the insolent indifference of a clock that chattered on at the top of its voice as though I were not there; while a strange and pitiless mirror with square feet, which stood across one corner of the room, cleared for itself a site I had not looked to find tenanted in the quiet surroundings of my normal field of vision: that room in which my mind, forcing itself for hours on end to leave its moorings, to elongate itself upwards so as to take on the exact shape of the room, and to reach to the summit of that monstrous funnel, had passed so many anxious nights while my body lay stretched out in bed, my eyes staring upwards, my ears straining, my nostrils sniffing uneasily, and my heart beating; until custom had changed the colour of the curtains, made the clock keep quiet, brought an expression of pity to the cruel, slanting face of the glass, disguised or even completely dispelled the scent of flowering grasses, and distinctly reduced the apparent loftiness of the ceiling."""# pylint: disable=line-too-long

    axes.set(title=proust_block)
    assert vislint(axes, fig, reading_level_config) == [
        ('no-complex-titles', 'Title should be easy to read')
    ]

def test_histogram():
    """
    Test for testing histogram type charts
    Example drawn from https://matplotlib.org/gallery/statistics/histogram_features.html
    """
    np.random.seed(19680801)

    # example data
    mu_val = 100  # mean of distribution
    sigma = 15  # standard deviation of distribution
    x_val = mu_val + sigma * np.random.randn(437)

    num_bins = 50

    fig, axes = plt.subplots()

    # the histogram of the data
    n_bins, bins, patches = axes.hist(x_val, num_bins, density=1)# pylint: disable=unused-variable

    # add a "best fit" line
    y_val = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
             np.exp(-0.5 * (1 / sigma * (bins - mu_val))**2))
    axes.plot(bins, y_val, "--")
    axes.set_xlabel("Smarts")
    axes.set_ylabel("Probability density")
    axes.set_title(r"Histogram of IQ: $\mu=100$, $\sigma=15$")

    assert vislint(axes, fig, DEFAULT_CONFIGURATION) == [
        ("require-legend", 'A legend must be used'),
        ("maximum-histogram-bins", 'This histogram has more than the allowed number of bins')
    ]

def test_no_pie():
    """
    tests for pie chart
    copied from https://matplotlib.org/examples/pie_and_polar_charts/pie_demo_features.html
    Pie chart, where the slices will be ordered and plotted counter-clockwise:
    """
    labels = "Frgs", "Hgs", "Dgs", "Lgs", "Frgs", "Hgs", "Dgs", "Lgs", "Dgs", "Lgs", "Lgs"
    sizes = [15, 30, 45, 10, 15, 30, 45, 10, 12, 9, 9]
    explode = (0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. "Hogs")

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%",
            shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    assert vislint(ax1, fig1, {
        "maximum-pie-pieces": 12,
        "max-colors": 10
    }) == [
        ("require-titles", 'Titles are required'),
        ("no-short-titles", 'Short titles are not allowed (must be greater than 1 word)'),
        ("require-axes", 'Axes must be labeled'),
        ("require-legend", 'A legend must be used'),
        ("no-pie", 'Pie charts are not allowed'),
        ("no-radial", 'Radial charts are not allowed'),
        # logically this should fail this test, however we can"t verify that from the library
        # level i think
        # ("representation-invariance", 'The order the of the points is not significant')
    ]

    alt_configuration = {
        "require-axes": False,
        "no-pie": False,
        "no-radial": False,
        "maximum-pie-pieces": 3,
        "require-annotation": True
    }

    assert vislint(ax1, fig1, alt_configuration) == [
        ("require-titles", 'Titles are required'),
        ("no-short-titles", 'Short titles are not allowed (must be greater than 1 word)'),
        ("require-legend", 'A legend must be used'),
        ("maximum-pie-pieces", 'This pie chart has more than the allowed number of wedges'),
        ('max-colors', 'Too many colors'),
        ("require-annotation", "annotations must be used")
    ]

# # algebraic smoke test?
def test_small_scatterplot():
    """
    Test focusing on algebraic scatterplot
    """
    area = [100000, 100000]
    x_points = [0.5, -0.5]
    y_points = [0, 0]
    colors = [0, 1]

    fig, axes = plt.subplots()
    axes.scatter(x_points, y_points, s=area, c=colors)

    assert vislint(axes, fig, DEFAULT_CONFIGURATION) == [
        ("require-titles", 'Titles are required'),
        ("no-short-titles", 'Short titles are not allowed (must be greater than 1 word)'),
        ("require-axes", 'Axes must be labeled'),
        ("require-legend", 'A legend must be used'),
        ("representation-invariance", 'The order the of the points is not significant')
    ]

def test_colors():
    """
    color tests
    copied from the docs again
    """
    np.random.seed(19680801)

    n_rows = 50
    x_vals = np.random.rand(n_rows)
    y_vals = np.random.rand(n_rows)
    colors = np.random.rand(n_rows)
    area = (30 * np.random.rand(n_rows))**2  # 0 to 15 point radii
    fig, axes = plt.subplots()
    axes.scatter(x_vals, y_vals, s=area, c=colors, alpha=0.5)
    axes.set(
        title="my big scatterplot",
        xlabel="x label",
        ylabel="y label"
    )
    axes.legend(" ex legend ")

    assert vislint(axes, fig, DEFAULT_CONFIGURATION) == [
        ("max-colors", 'Too many colors')
    ]
    # remove the previous scatterplot
    axes.collections[0].remove()

    colors = [idx % 5 for idx in range(n_rows)]
    axes.scatter(x_vals, y_vals, s=area, c=colors, alpha=0.5)
    assert vislint(axes, fig, DEFAULT_CONFIGURATION) == []

def test_multi_series_plot_test():
    """
    test distinguishable series
    """
    def build_chart(data):
        """
        chart builder!
        """
        fig, axes = plt.subplots(figsize=(6, 6))
        marks = ['o', '^', 's']
        colors = [
            (0.8941176470588236, 0.10196078431372549, 0.10980392156862745),
            (0.21568627450980393, 0.49411764705882355, 0.7215686274509804)
        ]

        for i in range(len(data)):
            group = data[i]
            axes.plot(group['left'], group['right'],
                      marker=marks[i % len(marks)],
                      color=colors[i % len(colors)],
                      linestyle='',
                      ms=5.5,
                      alpha=0.74,
                      label=group['maker'],
                      markeredgecolor='k',
                      markeredgewidth=0.25)
        plt.legend(ncol=2, numpoints=1, bbox_to_anchor=(1., 1.), fontsize=11, frameon=True)
        plt.xlabel('WOAOOAO')
        plt.ylabel('MAGIC')
        plt.title('wacky pizzaz')
        return (axes, fig)

    data = [
        {"left": [1, 2, 3], "right": [4, 5, 6], "maker": 'dogs'},
        {"left": [1, 2, 3], "right": [4, 5, 6], "maker": 'cats'},
        {"left": [1, 2, 3], "right": [4, 5, 6], "maker": 'squids'},
        {"left": [1, 2, 3], "right": [4, 5, 6], "maker": 'sushis'},
    ]

    axes, fig = build_chart(data)
    assert vislint(axes, fig, {"representation-invariance": 0.01}) == []

    data.append({"left": [1, 2, 3], "right": [4, 5, 6], "maker": 'seadogs'})
    data.append({"left": [1, 2, 3], "right": [4, 5, 6], "maker": 'giraffes'})
    data.append({"left": [1, 2, 3], "right": [4, 5, 6], "maker": 'octopus'})

    axes, fig = build_chart(data)
    assert vislint(axes, fig, {"representation-invariance": 0.01}) == [
        ('no-indistinguishable-series', 'Series must be distinguishable')
    ]

    dup_data = [
        {"left": [1, 2, 3], "right": [4, 5, 6], "maker": 'seadogs'},
        {"left": [1, 2, 3], "right": [4, 5, 6], "maker": 'seadogs'},
    ]
    axes, fig = build_chart(dup_data)
    assert vislint(axes, fig, {"representation-invariance": 0.01}) == [
        ('no-indistinguishable-series', 'Series must be distinguishable')
    ]



# THIS TEST IS BUSTED BC ledgible-text DOESNT REALLY WORK
# def test_scatterplot_annotate():
#     np.random.seed(19680801)
#
#     N = 3
#     x = np.random.rand(N)
#     y = np.random.rand(N)
#     colors = np.random.rand(N)
#     area = (30 * np.random.rand(N))**2  # 0 to 15 point radii
#     labels = ['dog', 'squid', 'octopus']
#     fig, ax = plt.subplots()
#     ax.scatter(x, y, s=30, c=colors, alpha=0.5)
#     ax.set(
#         title="my big scatterplot",
#         xlabel="x label",
#         ylabel="y label"
#     )
#     ax.legend(" ex legend ")
#     for idx in range(len(labels)):
#         ax.annotate(labels[idx], (x[idx] + 0.001, y[idx] + 0.001), fontsize=20)
#     # does very very poorly
#     assert vislint(ax, fig, {
#         "ledgible-text": True,
#         "require-annotation": True
#     }) == []


def passes_only_data_driven_visuals(axes, fig, config_value):
    """
    Example custom test function
    """
    return axes.get_title() == 'big bird'

# example custom test
EXAMPLE_CUSTOM_TEST = (
    "big-bird-title",
    passes_only_data_driven_visuals,
    False,
    "Title must be equal to big bird"
)

def test_custom_rule():
    """
    custom test test
    """
    (axes, fig) = generic_scatterplot()

    custom_config = {"custom_checks": [EXAMPLE_CUSTOM_TEST]}
    assert vislint(axes, fig, custom_config) == [
        ("require-titles", 'Titles are required'),
        ("no-short-titles", 'Short titles are not allowed (must be greater than 1 word)'),
        ("require-axes", 'Axes must be labeled'),
        ("require-legend", 'A legend must be used'),
        (EXAMPLE_CUSTOM_TEST[0], EXAMPLE_CUSTOM_TEST[3])]

    axes.set(xlabel="X", ylabel="Y", title="big bird")

    assert vislint(axes, fig, custom_config) == [('require-legend', 'A legend must be used')]
