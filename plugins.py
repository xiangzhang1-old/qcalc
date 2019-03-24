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