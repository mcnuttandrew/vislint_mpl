from utils import get_count_patch_type_count

def get_num_color_in_scatterplot(ax):
    # thats just a count of all of the colors, not the unique colors
    sum_colors = 0
    seen_colors = {}
    for collection in ax.collections:
        for color in collection.get_facecolors():
            str_color = str(color)
            if not str_color in seen_colors:
                seen_colors[str_color] = True
                sum_colors += 1

    return sum_colors


def get_num_color_in_patches(ax, patchtype):
    # thats just a count of all of the colors, not the unique colors
    sum_colors = 0
    seen_colors = {}
    for patch in ax.patches:
        if not type(patch).__name__ == patchtype:
            continue
        str_color = str(patch.get_facecolor())
        if not str_color in seen_colors:
            seen_colors[str_color] = True
            sum_colors += 1

    return sum_colors

def passes_no_color_ramps(axes, fig, config_value):
    return False

# reconfigurable please
def passes_ten_color_max(axes, fig, config_value):
    if len(axes.collections) >= 1:
        # scatterplot
        return get_num_color_in_scatterplot(axes) <= 10
    elif get_count_patch_type_count(axes.patches, 'Wedge') >= 1:
        # radial
        return get_num_color_in_patches(axes, 'Wedge') <= 10
    elif get_count_patch_type_count(axes.patches, 'Rect') >= 1:
        # rect
        return get_num_color_in_patches(axes, 'Rect') <= 10
    else:
        return True

def passes_noticeably_different_colors(axes, fig, config_value):
    return False

def passes_colorblind_distinct(axes, fig, config_value):
    return False

def passes_minimum_color_size(axes, fig, config_value):
    return False
