import pytest
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from vis_lint import vis_lint

def test_simple_line_chart():
    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure() and then ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    ax.plot(t, s)

    assert vis_lint(ax, fig) == [
        "require-titles",
        "no-short-titles",
        "require-axes",
        "require-legend"
    ]

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')

    assert vis_lint(ax, fig) == [
        "require-legend"
    ]


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

    # add a 'best fit' line
    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
         np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
    ax.plot(bins, y, '--')
    ax.set_xlabel('Smarts')
    ax.set_ylabel('Probability density')
    ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

    assert vis_lint(ax, fig) == [
        'require-legend',
        "maximum-histogram-bins"
    ]

def test_no_py():
    # copied from https://matplotlib.org/examples/pie_and_polar_charts/pie_demo_features.html
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    assert vis_lint(ax1, fig1) == [
        "require-titles",
        "no-short-titles",
        "require-axes",
        "require-legend",
        "no-pie",
        "no-radial",
        "value-ordering"
    ]

# # algebraic smoke test?
def test_scatterplot():
    area = [100000, 100000]
    x = [0.5, -0.5]
    y = [0, 0]
    colors = [0, 1]

    fig, ax = plt.subplots()
    ax.scatter(x, y, s=area, c=colors)

    assert vis_lint(ax, fig) == [
        "require-titles",
        "no-short-titles",
        "require-axes",
        "require-legend",
        "value-ordering"
    ]
