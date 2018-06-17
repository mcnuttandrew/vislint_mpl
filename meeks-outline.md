# viz-linting

meeks makes notes about a difference between unit-testing and linting

## General
* require-titles
* no-short-titles
* sentencify
* maximum-encoding
* require-axes
* require-legend
* maximum-pie-pieces
* maximum-histogram-bins
* no-radial
* value ordering

## XY
* collision-handling
    * prefer-hexbin
    * minimum-spacing
    * no-data-overlap
* fitts-law-handling
    an element should be of a certain size to be interacted with
* uncertainty-encoding
    be aware that uncertainty exists
* error-encoding
* mind-the-gap
    line chart gaps

## Hierarchical
* no-hierarchical-small-multiples
    strict-small-multiples
* atomic-circle-pack
* minimum-treemap-leaf-edge
* unique-leaves
*

## Network
* orphanage-n
    have a way to address singletons or disconnected components
* network-diagram-density
* maximum-edge-conflict

## Color
* no-color-ramps
* ten-color-max
* noticeably-different-colors
* colorblind-distinct
* thoughtful-background
    mindfulness??? unsure how this would be
* minimum-color-size
    might be this paper http://delivery.acm.org/10.1145/3030000/3026041/p1364-bartram.pdf?ip=128.135.98.176&id=3026041&acc=ACTIVE%20SERVICE&key=06A6A3A8AFB87403%2E37E789C11FBE2C91%2E4D4702B0C3E38B35%2E4D4702B0C3E38B35&__acm__=1529285357_2095e5233976899625a7d7955c2b6a94
* no-color-logging

## Annotation
* require-annotation
* no-label-overlap
