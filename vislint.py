"""
Root of the vislint_mpl library, imports all of the relevant rules
and provides to main api
"""

import lint_rules.algebraic_rules as algebraic_rules
import lint_rules.annotation_rules as annotation_rules
import lint_rules.color_rules as color_rules
import lint_rules.computational_rules as computational_rules
import lint_rules.general_rules as general_rules

RULE_TO_FUNCTION_MAP = {
    ## Algebraic rules
    "representation-invariance": algebraic_rules.passes_only_data_driven_visuals,

    ## Annotation
    "require-annotation": annotation_rules.passes_require_annotation,

    ## computational
    "ledgible-text": computational_rules.passes_ledgible_text,

    ## Color
    "max-colors": color_rules.passes_max_colors,

    ## General
    "require-titles": general_rules.passes_require_titles,
    "no-short-titles": general_rules.passes_no_short_titles,
    "sentencify": general_rules.passes_sentencify,
    "no-complex-titles": general_rules.passes_no_complex_titles,
    "require-axes": general_rules.passes_require_axes,
    "require-legend": general_rules.passes_require_legend,
    "no-indistinguishable-series": general_rules.passes_no_indistinguishable_series,
    "no-pie": general_rules.passes_no_pie,
    "maximum-pie-pieces": general_rules.passes_maximum_pie_pieces,
    "maximum-histogram-bins": general_rules.passes_maximum_histogram_bins,
    "no-radial": general_rules.passes_no_radial
}

# if it's no listed here then it's not written down
DEFAULT_CONFIGURATION = {
    # basic xy
    "require-titles": True,
    "no-short-titles": 1,
    "require-axes": True,
    "require-legend": True,
    "no-indistinguishable-series": True,
    "no-complex-titles": False,
    "sentencify": False,
    "no-pie": True,
    "maximum-pie-pieces": 6,
    "maximum-histogram-bins": 50,
    "no-radial": True,

    # algebraic
    "representation-invariance": 0.1,

    # color
    "max-colors": 6,

    # ml rules
    "ledgible-text": False,

    "require-annotation": False
}

RULES_EXPLANATION = {
    "require-titles": "Titles are required",
    "no-short-titles": "Short titles are not allowed (must be greater than 1 word)",
    "no-complex-titles": "Title should be easy to read",
    "sentencify": "Title should be in complete sentences",
    "require-axes": "Axes must be labeled",
    "require-legend": "A legend must be used",
    "no-pie": "Pie charts are not allowed",
    "maximum-pie-pieces": "This pie chart has more than the allowed number of wedges",
    "maximum-histogram-bins": "This histogram has more than the allowed number of bins",
    "no-radial": "Radial charts are not allowed",
    "representation-invariance": "The order the of the points is not significant",
    "max-colors": "Too many colors",
    "no-indistinguishable-series": "Series must be distinguishable",
    "require-annotation": "annotations must be used",
    "ledgible-text": "text must be ledgible"
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

def vislint(axes, fig, configuration):
    """
    Run lint on a matplotlib object, axes and fig are standard matplotlib objects
    configuration is a map with keys equals to rules and values equal to configurable values
    """

    rules_to_check = reconcile_configurations(DEFAULT_CONFIGURATION, configuration)
    failed_checks = []
    for (rule, config_value) in rules_to_check:
        rule_to_eval = RULE_TO_FUNCTION_MAP[rule]
        if not rule_to_eval(axes, fig, config_value):
            msg = RULES_EXPLANATION[rule]
            failed_checks.append((rule, msg))
    if 'custom_checks' in configuration:
        for (rule, rule_func, config_value, msg) in configuration['custom_checks']:
            if not rule_func(axes, fig, config_value):
                failed_checks.append((rule, msg))

    return failed_checks
