# vislint_mpl: a prototype visualization linter for matplotlib

vislint_mpl is an automated system for evaluating the effectiveness of visualization based on a collection of predefined rules. Visualization linting provides a robust mechanism to provide guidance to chart creators as the work through the steps of creating a visualization. The dream of this project is that users will be able to run vislint_mpl in a computational notebook setting, like jupyter, and have their visualizations evaluated on every code change, much like spell check or in the way that lint is accessed through code editors now.


This work is in the proof of concept stage of development, it is messy and there are limited number of rules implemented. Currently the rules that are implemented are:

- require-titles
- no-short-titles
- no-complex-titles
- sentencify
- require-axes
- require-legend
- no-pie
- maximum-pie-pieces
- maximum-histogram-bins
- no-radial
- representation-invariance
- max-colors
- no-indistinguishable-series
- require-annotation
- ledgible-text (not fully working)


Our organizational scheme follows that of Meeks's [viz-linting](https://github.com/emeeks/viz-linting), though another ordering, such as one analogous to the tagging system found on [VisGuides](https://visguides.dbvis.de/) or the taxonomical system found on the [Visualization Guidelines Repository](http://visguides.repo.dbvis.de/). The structure of this library is also heavily indebted to [write-good](https://github.com/btford/write-good) which we used as reference while creating it.

In the additional materials folder we provide a collection of additional lint rules and example notebooks of using vislint_mpl against charts sometimes found in the wild.

## API

This library consists of a single function that takes two mandatory arguments and an optional third

vislint_mpl(**axes**, **fig**, configuration={})

- **axes** - matplotlib [axes](https://matplotlib.org/api/axes_api.html) object

- **fig** - matplotlib [figure](https://matplotlib.org/api/figure_api.html) object

- **configuration** - the custom configuration map (see below)

It returns a list of tuples describing which of the tests failed, for example

```python
[
  ("require-titles", "Titles are required"),
  ("no-short-titles", "Short titles are not allowed (must be greater than 1 word)"),
  ("require-axes", "Axes must be labeled"),
  ("require-legend", "A legend must be used")
]
```

For usage examples, please refer to the test suite.

### Custom Configuration Map

The configuration map is the main way that user gets to opt into non-default rules, opt out of standard rules, provide alternative variables, or custom rules. With the exception of custom rules, rules manipulated by placing a key with that rules name in the configuration map and then a corresponding value. Here are the three designed use cases:

- **opt-out**: Provide a falsey value as the value to the key, ex ```"require-legend": False```.

- **opt-in**: Provide a truthy value as the value to the key, ex ```"no-complex-titles": True```.

- **change parameter**: Provide the configuration value you wish for your visualization be checked against, eg ```"maximum-histogram-bins": 100000```.


In addition to manipulating standard rules the user can also provide additional customizable rules through the "custom-rules" key, which expects a list of custom rules. A custom rule is tuple consisting of four values:

(**testName**, **testFunction**, **defaultTestValue**, **testFailureMsg**)

**testName** - string describing the test being run, for instance "no-scatterplots"

**testFunction** - the test function to be evaluated. It should take three arguments (axes, fig, config_value), which are respectively a matplotlib axes object, a matplotlib figure object, and the value to be checked against (though it is not necessary to set this), and return a boolean, True if the test passes, and Fail if the test fails.

**defaultTestValue** - The value to be passed into third argument of the test function, see above. This value does not have to be meaningful for all tests, for instance, no-radial does not accept any additional configuration value.

**testFailureMsg** - A string to present to the user when the test has fail, for instance "Radial charts are not allowed". This should be short and sweet and should follow the typical terse lint explanation style.


## Testing

This library is kept in check by running unit tests over the various lint rules. Our tests can be run via:

```sh
pytest -vv general_lint_tests.py
```


## Installing
### (Instruction for mac only)

Again we highlight that this is an extremely early stage prototype, so genuinely recommend that you do not try to use it for anything. That said, if you are really motivated to do so, we now provide installation instructions. We include a pretty wide variety of packages to proof of concept this work, so buyer beware. One such example is that we require that tesseract be installed (for OCR), this can be done on mac via:

```sh
brew install tesseract
```

Once done, clone this repository, cd into it then, boot up a python virtualenv by running

```sh
source bin/activate
```

Then install of the relevant packages.

```sh
pip install -r requirements.txt
```

Now you should be all set to go!



## Additional Materials

In the additional materials folder, we have included a speculative list of a wide variety of additional lint rules, along with notes as to how they might be created. As noted above in the additional materials section we present several notebooks of interest. In order to run these, first have jupyter installed, activate in the same fashion as noted above, and then run:

```sh
jupyter notebook
```

It may be necessary to also run ```ipython kernel install --user``` in order to get everything installe correctly.

Of particular note, we have provided the notebook used to produce the figure found in the paper associated with this work. That graphic is drawn from the sprawling github Jupyter notebook corpus found [here](https://library.ucsd.edu/dc/collection/bb6931851t). The figure used in the paper is drawn from a reconstruction of the original notebook (rebuild rebuild_of_nb_266110) which we present along side the original (nb_266110) for transparency.
