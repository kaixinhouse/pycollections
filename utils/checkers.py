# -*- coding: utf -*-

def is_valid_md5(md5):
    if not isinstance(md5, basestring):
        return False
    md5 = md5.lower()
    if len(md5) != 32:
        return False
    if any([c not in '0123456789abcdef' for c in md5]):
        return False
    return True
