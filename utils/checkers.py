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


if __name__ == '__main__':
    print is_valid_md5('12345')
    print is_valid_md5('37adc72339a0c2c755e7fef346906330')
