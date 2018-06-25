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
    "minimum-color-size": passes_minimum_color_size,

    ## Annotation
    "require-annotation": passes_require_annotation
}


BASE_CONFIGURATION = {
    # basic xy
    "require-titles": True,
    "no-short-titles": 1,
    "require-axes": True,
    "require-legend": True,
    "no-pie": True,
    "maximum-pie-pieces": 6,
    "maximum-histogram-bins": 50,
    "no-radial": True,

    # algebraic
    "value-ordering": 0.1

    # if it's no listed here then it's not written down
}

RULES_EXPLANATION = {
    "require-titles": "Titles are required",
    "no-short-titles": "Short titles are not allowed (must be greater than 1 word)",
    "require-axes": "Axes must be used",
    "require-legend": "A legend must be used",
    "no-pie": "Pie charts are not allowed",
    "maximum-pie-pieces": "This pie chart has more than the allowed number of wedges",
    "maximum-histogram-bins": "This histogram has more than the allowed number of bins",
    "no-radial": "Radial charts are not allowed",
    "value-ordering": "The order the of the points is not significant"
}



def reconcile_configurations(old_config, new_config):
    """
    Combine the default configuration and the users input configuration
    """
    rules_to_check = []
    for rule_name, value in old_config.items():
        if rule_name not in new_config and value:
            rules_to_check.append((rule_name, value))
        elif rule_name in new_config and new_config[rule_name]:
            rules_to_check.append((rule_name, new_config[rule_name]))
    return rules_to_check

def vis_lint(axes, fig, configuration):
    """
    Run lint on a matplotlib object, axes and fig are standard matplotlib objects
    configuration is a map with keys equals to rules and values equal to configurable values
    """

    rules_to_check = reconcile_configurations(BASE_CONFIGURATION, configuration)
    failed_checks = []
    for (rule, config_value) in rules_to_check:
        rule_to_eval = rule_to_function_map[rule]
        if not rule_to_eval(axes, fig, config_value):
            msg = RULES_EXPLANATION[rule]
            failed_checks.append((rule, msg))
    if 'custom_checks' in configuration:
        for (rule, rule_func, config_value, msg) in configuration['custom_checks']:
            if not rule_func(axes, fig, config_value):
                failed_checks.append((rule, msg))

    return failed_checks
