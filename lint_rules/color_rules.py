"""
Lint rules for color based rules
"""

from lint_rules.utils import get_count_patch_type_count, has_method

def count_uniques(colors):
    """
    count the number of uniques in a set of color tuples
    """
    sum_colors = 0
    seen_colors = {}
    for color in colors:
        if not color in seen_colors:
            seen_colors[color] = True
            sum_colors += 1

    return sum_colors

def get_num_color_in_scatterplot(axes):
    """
    extract the number of colors in a scatterplot
    """
    colors = []
    for collection in axes.collections:
        for color in collection.get_facecolors():
            colors.append(str(color))
    return count_uniques(colors)

DATA_COLOR_OBJECTS = {
    "Rectangle": True,
    "Spine": True,
    "Line2D": True
}

def get_num_color_in_children(axes):
    """
    get number of colors in an axes children
    """
    return count_uniques([
        (child.get_color() if has_method(child, 'get_color') else child.get_facecolor())
        for child in axes.get_children()
        if type(child).__name__ in DATA_COLOR_OBJECTS])


def get_num_color_in_patches(axes, patchtype):
    """
    get the number of colors in an axes patches
    """
    colors = [
        str(patch.get_facecolor()) for patch in axes.patches
        if type(patch).__name__ == patchtype]
    return count_uniques(colors)

# reconfigurable please
def passes_max_colors(axes, fig, config_value):
    """
    lint rule for max-colors
    """
    # scatterplot
    if len(axes.collections) >= 1:
        return get_num_color_in_scatterplot(axes) <= config_value

    # radial
    if get_count_patch_type_count(axes.patches, 'Wedge') >= 1:
        return get_num_color_in_patches(axes, 'Wedge') <= config_value

    # rect
    if get_count_patch_type_count(axes.patches, 'Rect') >= 1:
        return get_num_color_in_patches(axes, 'Rect') <= config_value

    # check children otherwise
    return get_num_color_in_children(axes) <= config_value
