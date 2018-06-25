def passes_require_titles(axes, fig, config_value):
    return len(axes.get_title()) != 0

def passes_no_short_titles(axes, fig, config_value):
    return len(axes.get_title().split(' ')) > config_value

def passes_sentencify(axes, fig, config_value):
    return sentence_count(axes.get_title()) >= 1

def passes_no_complex_titles(axes, fig, config_value):
    # print('???')
    # print_methods(textstat)
    # value = config_value if str(config_value).isdigit() else 69
    # return flesch_reading_ease(value) >= value
    return False

def passes_maximum_encoding(axes, fig, config_value):
    return False

def passes_require_axes(axes, fig, config_value):
    # TODO could add configuration for xy, x, y require axes
    xlabel = axes.get_xlabel()
    ylabel = axes.get_ylabel()
    return not len(xlabel) == 0 and not len (ylabel) == 0

def passes_require_legend(axes, fig, config_value):
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

def get_count_patch_type_count(patches, patch_type):
    count = 0
    for patch in patches:
        if type(patch).__name__ == patch_type:
            count += 1
    return count

def passes_no_pie(axes, fig, config_value):
    return get_count_patch_type_count(axes.patches, 'Wedge') == 0

def passes_maximum_pie_pieces(axes, fig, config_value):
    return get_count_patch_type_count(axes.patches, 'Wedge') < config_value

def passes_maximum_histogram_bins(axes, fig, config_value):
    # TODO how to differentiate between histogram and bar chart
    return get_count_patch_type_count(axes.patches, 'Rectangle') < config_value

def passes_no_radial(axes, fig, config_value):
    return get_count_patch_type_count(axes.patches, 'Wedge') == 0
