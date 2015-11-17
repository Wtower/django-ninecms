""" Permissions utility functions """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

# noinspection PyPackageRequirements
from guardian.shortcuts import get_groups_with_perms, assign_perm, remove_perm


def get_perms(obj, fields, suffix):
    """ Get all groups which have perms on an object, categorized by permission names (fields)
    To be mainly used in form operations to obtain the initial value of fields
    The guardian `get_groups_with_perms()` returns a dictionary of groups, with relevant permissions
    The list comprehension statement below hecks if the field is in the dict, and appends the group

    :param obj: the record object for which to get permissions
    :param fields: the permission names to categorize
    :param suffix: an additional string that, when appended on the field name, will give us the perm name
    :return: a dictionary of fields: groups list
    """
    groups = get_groups_with_perms(obj, attach_perms=True) if obj else {}
    perms = {}
    for field in fields:
        perms[field] = list(key for (key, val) in groups.items() if field + suffix in val)
    return perms


def set_perms(obj, fields, suffix, perms):
    """ Set group perms on an object
    To be mainly used in form operations, from which the cleaned data of fields are obtained
    Check if group is in new perms and not in old, and assign, or vice versa

    :param obj: the record object for which to get permissions
    :param fields: the permission names to categorize
    :param suffix: an additional string that, when appended on the field name, will give us the perm name
    :param perms:
    :return: a dictionary of fields: groups list
    """
    old_perms = get_perms(obj, fields, suffix)
    for field in fields:
        for group in perms[field]:
            if group not in old_perms[field]:
                assign_perm(field + suffix, group, obj)
        for group in old_perms[field]:
            if group not in perms[field]:
                remove_perm(field + suffix, group, obj)
