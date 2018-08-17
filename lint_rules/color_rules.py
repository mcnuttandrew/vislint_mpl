"""
Lint rules for color based rules
"""

from matplotlib.colors import to_rgba, rgb_to_hsv
from lint_rules.utils import get_count_patch_type_count, has_method

def get_uniques(colors):
    """
    build a list of unique colors tuples
    """
    seen_colors = {}
    for color in colors:
        if not color in seen_colors:
            seen_colors[color] = True

    return seen_colors.keys()

def get_colors_in_scatterplot(axes):
    """
    extract the number of colors in a scatterplot
    """
    colors = []
    for collection in axes.collections:
        for color in collection.get_facecolors():
            colors.append(tuple(list(color)))
    return get_uniques(colors)

DATA_COLOR_OBJECTS = {
    "Rectangle": True,
    "Line2D": True
}

def get_colors_in_children(axes):
    """
    get number of colors in an axes children
    """
    colors = []
    for child in axes.get_children():
        if type(child).__name__ in DATA_COLOR_OBJECTS:
            color = child.get_color() if has_method(child, 'get_color') else child.get_facecolor()
            colors.append(color)
    return get_uniques(colors)


def get_colors_in_patches(axes, patchtype):
    """
    get the number of colors in an axes patches
    """
    colors = [
        patch.get_facecolor() for patch in axes.patches
        if type(patch).__name__ == patchtype]
    return get_uniques(colors)

def get_colors_from_object(axes):
    """
    adaptor for conecting to various type of charts
    """
    # scatterplot
    if len(axes.collections) >= 1:
        print("scatterplot")
        return get_colors_in_scatterplot(axes)

    # radial
    if get_count_patch_type_count(axes.patches, 'Wedge') >= 1:
        print("radial")
        return get_colors_in_patches(axes, 'Wedge')

    # rect
    if get_count_patch_type_count(axes.patches, 'Rect') >= 1:
        print("rect")
        return get_colors_in_patches(axes, 'Rect')

    # check children otherwise
    print("other")
    return get_colors_in_children(axes)

def passes_max_colors(axes, fig, config_value):
    """
    lint rule for max-colors
    """
    return len(get_colors_from_object(axes)) <= config_value

def maybe_convert_hex(color):
    """
    Convert a given color to a tuple representation, may accept hex or tuples
    """
    return to_rgba(color) if isinstance(color, str) else color

def passes_printable_colors(axes, fig, config_value):
    """
    lint rule for printable colors
    algorithm: get unique colors, convert to hsv representation, count unique gray values,
    if the number of these colors is different then fail.

    Could be configured to accept a minimum threshold distance between the color values
    """
    background_color = fig.patch.get_facecolor()
    values = [
        rgb_to_hsv(maybe_convert_hex(color)[0:3])[2]
        for color in get_colors_from_object(axes)
        if color != background_color
        ]

    return len(get_uniques(values)) == len(values)
