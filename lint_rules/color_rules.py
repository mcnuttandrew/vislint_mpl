from utils import get_count_patch_type_count

def count_uniques(colors):
    sum_colors = 0
    seen_colors = {}
    for color in colors:
        if not color in seen_colors:
            seen_colors[color] = True
            sum_colors += 1

    return sum_colors

def get_num_color_in_scatterplot(ax):
    colors = []
    for collection in ax.collections:
        [colors.append(str(color)) for color in collection.get_facecolors()]
    return count_uniques(colors)


def get_num_color_in_patches(ax, patchtype):
    colors = [str(patch.get_facecolor()) for patch in ax.patches if type(patch).__name__ == patchtype]
    return count_uniques(colors)

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
