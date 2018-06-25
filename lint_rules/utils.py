def get_count_patch_type_count(patches, patch_type):
    count = 0
    for patch in patches:
        if type(patch).__name__ == patch_type:
            count += 1
    return count
