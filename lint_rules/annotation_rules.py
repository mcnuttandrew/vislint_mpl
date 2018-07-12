def passes_require_annotation(axes, fig, config_value):
    annotations = [x.get_text() for x in axes.get_children() if type(x).__name__ == 'Annotation']
    return len(annotations) > 0
