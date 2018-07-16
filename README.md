# VisLint: a proto visualization linter for matplotlib

VisLint is an automated system for evaluating the effectiveness of visualization based on a collection of predefined rules. The dream of this project is that users will be able to run VisLint is a computational notebook setting, like jupyter, and have their visualizations evaluated on every code change, much like spell check or in the way that lint is accessed through code editors now.


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
- only-data-driven-visuals
- max-colors
- no-indistinguishable-series
- require-annotation
- ledgible-text


In the additional materials folder, we have included a speculative list of a wide variety of additional lint rules, along with notes as to how they might be created. Our organizational scheme follows that of Meeks's [viz-linting](https://github.com/emeeks/viz-linting), though another ordering, such as one analogous to the tagging system found on [VisGuides](https://visguides.dbvis.de/) or the taxonomical system found on the [Visualization Guidelines Repository](http://visguides.repo.dbvis.de/).


The work draws heavily on the ideas of Meeks and VisGuides.



The notebooks in example_nb/ are used to create the visualization found in the paper.


## Installing

We require that tesseract be installed (for OCR), this can be done on mac via:

```sh
brew install tesseract
```

Once done, boot up an python virtualenv by running

```sh
source bin/activate
```



## Testing

Our little library is kept in check by running unit tests over the various
