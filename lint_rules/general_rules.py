

def passes_require_titles(axes, fig):
    return len(axes.get_title()) != 0

def passes_no_short_titles(axes, fig):
    title = axes.get_title().split(' ')
    return len(title) > 1

# def passes_sentencify(axes, fig):
#
#     return False


def passes_maximum_encoding(axes, fig):
    return False

def passes_require_axes(axes, fig):
    xlabel = axes.get_xlabel()
    ylabel = axes.get_ylabel()
    return not len(xlabel) == 0 and not len (ylabel) == 0

def passes_require_legend(axes, fig):
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

def passes_no_pie(axes, fig):
    return get_count_patch_type_count(axes.patches, 'Wedge') == 0

# arbitrarilly set to 6? figure out post configuraiton later
def passes_maximum_pie_pieces(axes, fig):
    return get_count_patch_type_count(axes.patches, 'Wedge') < 6

# arbitrarilly set to 40
def passes_maximum_histogram_bins(axes, fig):
    # how to differentiate between histogram and bar chart
    return get_count_patch_type_count(axes.patches, 'Rectangle') < 6

def passes_no_radial(axes, fig):
    return get_count_patch_type_count(axes.patches, 'Wedge') == 0
