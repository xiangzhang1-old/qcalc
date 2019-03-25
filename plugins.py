def exec_short(s, d):  # helper
    """
    Convenience function. Accepts 'opt' and 'spin=fm', hides opt, evaluates [1,2,3] and unquoted string. No overwrite.
    """
    old = d.copy()
    if '=' not in s:                            # opt
        s = slugify(s)                          # clean
        d[s] = True
        d['hidden'].add(s)                      # hides opt
    elif '=' in s:                              # spin=fm
        l, r = slugify(l), slugify(r)
        assert l == slugify(l)
        try:
            d[l] = eval(r)                      # evaluates [1,2,3]
        except NameError:
            d[l] = r                            # unquoted string
    assert old.items() <= d.items()             # no overwrite


def slugify(value):
    """
    Make a string URL- and filename-friendly.
    Taken from django/utils/text.py. In Django, a "slug" is a URL- and filename-friendly string.

    :param unicode value: string to be converted
    :return: filename-friendly string
    :rtype: unicode
    :raises TypeError: if value is not unicode string
    """
    value = unicodedata.normalize('NFKD', value)
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value

def suggest_host():
    pass

# plugin: 自动继承 struct，自动覆盖 phi0, rho0, rho

ready_run = []