"""
Lint rules for the ambigious general category
"""

from textstat.textstat import textstat

from lint_rules.utils import get_count_patch_type_count

def passes_require_titles(axes, fig, config_value):
    """
    lint rule for require-titles
    """
    return len(axes.get_title()) != 0

def passes_no_short_titles(axes, fig, config_value):
    """
    lint rule for no-short-titles
    """
    return len(axes.get_title().split(' ')) > config_value

def passes_sentencify(axes, fig, config_value):
    """
    lint rule for sentencify
    """
    return textstat.sentence_count(axes.get_title()) >= 1

def passes_no_complex_titles(axes, fig, config_value):
    """
    lint rule for no-complex-titles
    """
    value = config_value if str(config_value).isdigit() else 69
    return textstat.flesch_reading_ease(axes.get_title()) >= value

def passes_require_axes(axes, fig, config_value):
    """
    lint rule for require-axes
    """
    # could add configuration for xy, x, y require axes
    xlabel = axes.get_xlabel()
    ylabel = axes.get_ylabel()
    return not len(xlabel) == 0 and not len(ylabel) == 0

def passes_require_legend(axes, fig, config_value):
    """
    lint rule for require-legend
    """
    # notes on a later idealized rule
    # if there are multiple series or plot object require a legend
    # if there are colors require a legend
    # if there is size variation require a legend

    legend = axes.get_legend()
    if not legend:
        return False

    # notes on a stronger rule
    # text_length = 0
    # [text_length += len(text.get_text()) for text in legend.texts]

    return True

# only checks multiple artist groups
def passes_no_indistinguishable_series(axes, fig, config_value): # pylint: disable=invalid-name
    """
    lint rule for no-indistinguishable-series
    """
    if len(axes.collections) >= 1:
        return True

    if axes.get_legend():
        seen_texts = {}
        for text in list(axes.get_legend().get_texts()):
            to_hash = text.get_text()
            if to_hash in seen_texts:
                return False
            seen_texts[to_hash] = True

    seen_mark_types = {}
    children_to_check = [child for child in axes.get_children() if type(child).__name__ == 'Line2D']
    if not len(children_to_check):
        return True

    for child in children_to_check:
        mark_and_color = (child.get_marker(), child.get_color())
        if mark_and_color in seen_mark_types:
            return False
        seen_mark_types[mark_and_color] = True
    return True


def passes_no_pie(axes, fig, config_value):
    """
    lint rule for no-pie
    """
    return get_count_patch_type_count(axes.patches, 'Wedge') == 0

def passes_maximum_pie_pieces(axes, fig, config_value):
    """
    lint rule for maximum-pie-pieces
    """
    return get_count_patch_type_count(axes.patches, 'Wedge') < config_value

def passes_maximum_histogram_bins(axes, fig, config_value):
    """
    lint rule for maximum-histogram-bins
    """
    # prototype note: how to differentiate between histogram and bar chart?
    return get_count_patch_type_count(axes.patches, 'Rectangle') < config_value

def passes_no_radial(axes, fig, config_value):
    """
    lint rule for no-radial
    """
    return get_count_patch_type_count(axes.patches, 'Wedge') == 0
