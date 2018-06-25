

def passes_require_titles(axes, fig, config_value):
    return len(axes.get_title()) != 0

def passes_no_short_titles(axes, fig, config_value):
    title = axes.get_title().split(' ')
    return len(title) > config_value

# def passes_sentencify(axes, fig, config_value):
#
#     return False


def passes_maximum_encoding(axes, fig, config_value):
    return False

def passes_require_axes(axes, fig, config_value):
    xlabel = axes.get_xlabel()
    ylabel = axes.get_ylabel()
    return not len(xlabel) == 0 and not len (ylabel) == 0

def passes_require_legend(axes, fig, config_value):
    # if there are multiple series or plot object require a legend
    # if there are colors require a legend
    # if there is size variation require a legend
    return False

def get_count_patch_type_count(patches, patch_type):
    count = 0
    for patch in patches:
        if type(patch).__name__ == patch_type:
            count += 1
    return count

def passes_no_pie(axes, fig, config_value):
    return get_count_patch_type_count(axes.patches, 'Wedge') == 0

# arbitrarilly set to 6? figure out post configuraiton later
def passes_maximum_pie_pieces(axes, fig, config_value):
    return get_count_patch_type_count(axes.patches, 'Wedge') < config_value

# arbitrarilly set to 40
def passes_maximum_histogram_bins(axes, fig, config_value):
    # how to differentiate between histogram and bar chart
    return get_count_patch_type_count(axes.patches, 'Rectangle') < config_value

def passes_no_radial(axes, fig, config_value):
    return get_count_patch_type_count(axes.patches, 'Wedge') == 0
