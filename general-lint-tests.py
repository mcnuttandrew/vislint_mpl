import pytest
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from vis_lint import vis_lint

DEFAULT_CONFIGURATION = {}

def test_simple_line_chart():
    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure() and then ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    ax.plot(t, s)

    assert vis_lint(ax, fig, DEFAULT_CONFIGURATION) == [
        ("require-titles", 'Titles are required'),
        ("no-short-titles", 'Short titles are not allowed (must be greater than 1 word)'),
        ("require-axes", 'Axes must be used'),
        ("require-legend", 'A legend must be used')]

    ax.set(xlabel="time (s)", ylabel="voltage (mV)",
           title="About as simple as it gets, folks")

    assert vis_lint(ax, fig, DEFAULT_CONFIGURATION) == [
        ("require-legend", 'A legend must be used')
    ]

    ax.legend("Example legend")
    assert vis_lint(ax, fig, DEFAULT_CONFIGURATION) == []

# this test should mostly be done, however i rage quit when textstat didn't do what it advertised
# def test_reading_level():
#     t = np.arange(0.0, 2.0, 0.01)
#     s = 1 + np.sin(2 * np.pi * t)
#     fig, ax = plt.subplots()
#     ax.plot(t, s)
#
#     reading_level_config = {
#         "require-titles": True,
#         "no-short-titles": True,
#         "require-axes": False,
#         "require-legend": False,
#         "sentencify": True
#     }
#
#     ax.set(title="About as simple as it gets, folks")
#
#     assert vis_lint(ax, fig, reading_level_config) == [
#         ("sentencify", 'should find that not complete sentences are still sentences')
#     ]

# https://matplotlib.org/gallery/statistics/histogram_features.html
def test_histogram():
    np.random.seed(19680801)

    # example data
    mu = 100  # mean of distribution
    sigma = 15  # standard deviation of distribution
    x = mu + sigma * np.random.randn(437)

    num_bins = 50

    fig, ax = plt.subplots()

    # the histogram of the data
    n, bins, patches = ax.hist(x, num_bins, density=1)

    # add a "best fit" line
    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
         np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
    ax.plot(bins, y, "--")
    ax.set_xlabel("Smarts")
    ax.set_ylabel("Probability density")
    ax.set_title(r"Histogram of IQ: $\mu=100$, $\sigma=15$")

    assert vis_lint(ax, fig, DEFAULT_CONFIGURATION) == [
        ("require-legend", 'A legend must be used'),
        ("maximum-histogram-bins", 'This histogram has more than the allowed number of bins')
    ]

def test_no_pie():
    # copied from https://matplotlib.org/examples/pie_and_polar_charts/pie_demo_features.html
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = "Frogs", "Hogs", "Dogs", "Logs", "Frogs", "Hogs", "Dogs", "Logs", "Dogs", "Logs", "Logs"
    sizes = [15, 30, 45, 10, 15, 30, 45, 10, 12, 9, 9]
    explode = (0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. "Hogs")

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%",
            shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    assert vis_lint(ax1, fig1, {
        "maximum-pie-pieces": 12
    }) == [
        ("require-titles", 'Titles are required'),
        ("no-short-titles", 'Short titles are not allowed (must be greater than 1 word)'),
        ("require-axes", 'Axes must be used'),
        ("require-legend", 'A legend must be used'),
        ("no-pie", 'Pie charts are not allowed'),
        ("no-radial", 'Radial charts are not allowed'),
        # logically this should fail this test, however we can"t verify that from the library
        # level i think
        # ("value-ordering", 'The order the of the points is not significant')
    ]

    alt_configuration = {
        "require-axes": False,
        "no-pie": False,
        "no-radial": False,
        "maximum-pie-pieces": 3
    }

    assert vis_lint(ax1, fig1, alt_configuration) == [
        ("require-titles", 'Titles are required'),
        ("no-short-titles", 'Short titles are not allowed (must be greater than 1 word)'),
        ("require-legend", 'A legend must be used'),
        ("maximum-pie-pieces", 'This pie chart has more than the allowed number of wedges')
    ]

# # algebraic smoke test?
def test_small_scatterplot():
    area = [100000, 100000]
    x = [0.5, -0.5]
    y = [0, 0]
    colors = [0, 1]

    fig, ax = plt.subplots()
    ax.scatter(x, y, s=area, c=colors)

    assert vis_lint(ax, fig, DEFAULT_CONFIGURATION) == [
        ("require-titles", 'Titles are required'),
        ("no-short-titles", 'Short titles are not allowed (must be greater than 1 word)'),
        ("require-axes", 'Axes must be used'),
        ("require-legend", 'A legend must be used'),
        ("value-ordering", 'The order the of the points is not significant')
    ]

# coped from the docs again
def test_scatterplot():
    np.random.seed(19680801)

    N = 50
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)
    area = (30 * np.random.rand(N))**2  # 0 to 15 point radii
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=area, c=colors, alpha=0.5)
    ax.set(
        title="my big scatterplot",
        xlabel="x label",
        ylabel="y label"
    )
    ax.legend(" ex legend ")

    assert vis_lint(ax, fig, DEFAULT_CONFIGURATION) == [
        ("ten-color-max", 'Should have a maximum of ten colors')
    ]
    # remove the previous scatterplot
    ax.collections[0].remove()

    colors = [i % 5 for i in range(N)]
    ax.scatter(x, y, s=area, c=colors, alpha=0.5)
    assert vis_lint(ax, fig, DEFAULT_CONFIGURATION) == []
