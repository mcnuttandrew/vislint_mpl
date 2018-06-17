import sys

sys.path.append('./lint_rules')
from algebraic_rules import *
from annotation_rules import *
from color_rules import *
from general_rules import *
from hierarchical_rules import *
from network_rules import *
from xy_rules import *

def print_methods(input_obj):
    print('\n'.join([x for x in dir(input_obj)]))

rule_to_function_map = {
    ## Algebraic rules
    "value-ordering": passes_value_ordering,
    # TODO

    ## VisGuide rules?
    # TODO tuftian rules, like data-ink-ratio

    ## General
    "require-titles": passes_require_titles,
    "no-short-titles": passes_no_short_titles,
    # not sure how to implement this
    # "sentencify": passes_sentencify,
    "maximum-encoding": passes_maximum_encoding,
    "require-axes": passes_require_axes,
    "require-legend": passes_require_legend,
    "no-pie": passes_no_pie,
    "maximum-pie-pieces": passes_maximum_pie_pieces,
    "maximum-histogram-bins": passes_maximum_histogram_bins,
    "no-radial": passes_no_radial,
    # possible additional rules: require labels, no-explode, no-shadow

    ## XY
    "collision-handling": passes_collision_handling,
    "fitts-law-handling": passes_fitts_law_handling,
    "uncertainty-encoding": passes_uncertainty_encoding,
    "error-encoding": passes_error_encoding,
    "mind-the-gap": passes_mind_the_gap,

    ## Hierarchical
    "no-hierarchical-small-multiples": passes_no_hierarchical_small_multiples,
    "atomic-circle-pack": passes_atomic_circle_pack,
    "minimum-treemap-leaf-edge": passes_minimum_treemap_leaf_edge,

    ## Network
    "orphanage-n": passes_orphanage_n,

    ## Color
    "no-color-ramps": passes_no_color_ramps,
    "ten-color-max": passes_ten_color_max,
    "noticeably-different-colors": passes_noticeably_different_colors,
    "colorblind-distinct": passes_colorblind_distinct,
    # "thoughtful-background": passes_thoughtful_background,
    # actually can not be executed
    "minimum-color-size": passes_minimum_color_size,

    ## Annotation
    "require-annotation": passes_require_annotation
}

def vis_lint(axes, fig):
    rules_to_check = [
        "require-titles",
        "no-short-titles",
        # "sentencify",
        # "maximum-encoding",
        "require-axes",
        "require-legend",
        "no-pie",
        "maximum-pie-pieces",
        "maximum-histogram-bins",
        "no-radial",

        # algebraic
        "value-ordering"
    ]

    failed_checks = [
        rule for rule in rules_to_check if not rule_to_function_map[rule](axes, fig)
    ]

    return failed_checks
    # how does eslint work whitelist/blacklist?
    # rules?
    # i guess let's just do whitelist for now
