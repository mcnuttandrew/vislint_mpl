"""
Grab bag utility file
"""


def get_count_patch_type_count(patches, patch_type):
    """
    count the number of a type of patches in a patches list
    """
    count = 0
    for patch in patches:
        if type(patch).__name__ == patch_type:
            count += 1
    return count

def has_method(input_obj, method):
    """
    check if an object has a method
    """
    return method in dir(input_obj)

def print_methods(input_obj):
    """
    debugging method used for printing out all of the methods of an object
    """
    print('\n'.join([x for x in dir(input_obj)]))
