"""
Root of the vislint_mpl library, imports all of the relevant rules
and provides to main api
"""

from collections import namedtuple

import lint_rules.algebraic_rules as algebraic_rules
import lint_rules.annotation_rules as annotation_rules
import lint_rules.color_rules as color_rules
import lint_rules.computational_rules as computational_rules
import lint_rules.general_rules as general_rules

Rule = namedtuple('Rule', 'title default explanation rule_eval')

RULES_CONFIGS = [
    # basic xy
    Rule(
        "require-titles",
        True,
        "Titles are required",
        general_rules.passes_require_titles
    ),
    Rule(
        "no-short-titles",
        1,
        "Short titles are not allowed (must be greater than 1 word)",
        general_rules.passes_no_short_titles
    ),
    Rule(
        "sentencify",
        False,
        "Title should be in complete sentences",
        general_rules.passes_sentencify
    ),
    Rule(
        "require-axes",
        True,
        "Axes must be labeled",
        general_rules.passes_require_axes
    ),
    Rule(
        "no-complex-titles",
        False,
        "Title should be easy to read",
        general_rules.passes_no_complex_titles
    ),
    Rule(
        "require-legend",
        True,
        "A legend must be used",
        general_rules.passes_require_legend
    ),
    Rule(
        "no-indistinguishable-series",
        True,
        "Series must be distinguishable",
        general_rules.passes_no_indistinguishable_series
    ),
    Rule(
        "no-pie",
        True,
        "Pie charts are not allowed",
        general_rules.passes_no_pie
    ),
    Rule(
        "maximum-pie-pieces",
        6,
        "This pie chart has more than the allowed number of wedges",
        general_rules.passes_maximum_pie_pieces
    ),
    Rule(
        "maximum-histogram-bins",
        50,
        "This histogram has more than the allowed number of bins",
        general_rules.passes_maximum_histogram_bins
    ),
    Rule(
        "no-radial",
        True,
        "Radial charts are not allowed",
        general_rules.passes_no_radial
    ),

    # algebraic
    Rule(
        "representation-invariance",
        0.1,
        "The order the of the points is not significant",
        algebraic_rules.passes_only_data_driven_visuals
    ),

    # color
    Rule(
        "max-colors",
        6,
        "Too many colors",
        color_rules.passes_max_colors
    ),
    Rule(
        "printable-colors",
        True,
        "Colors must be printable",
        color_rules.passes_printable_colors
    ),

    # computational
    Rule(
        "ledgible-text",
        False,
        "text must be ledgible",
        computational_rules.passes_ledgible_text
    ),

    # other
    Rule(
        "require-annotation",
        False,
        "annotations must be used",
        annotation_rules.passes_require_annotation
    )
]

DEFAULT_CONFIGURATION = {}
RULES_EXPLANATION = {}
RULE_TO_FUNCTION_MAP = {}
for title, default, explanation, rule_eval in RULES_CONFIGS:
    DEFAULT_CONFIGURATION[title] = default
    RULES_EXPLANATION[title] = explanation
    RULE_TO_FUNCTION_MAP[title] = rule_eval


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

def vislint(axes, fig, configuration=None):
    """
    Run lint on a matplotlib object, axes and fig are standard matplotlib objects
    configuration is a map with keys equals to rules and values equal to configurable values
    """
    if configuration is None:
        configuration = {}
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
