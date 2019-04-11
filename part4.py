import unicodedata, re

def exec_short(s, d):
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

# ----------------------------------------------------------------------------------------------------------------------
def uuid4():
    """
    Generates a random UUID.UUID4 encoded in base57.
    Taken from shortuuid.
    Encodes a UUID into a string (LSB first) according to the alphabet. If leftmost (MSB) bits 0, string might be shorter
    """
    alphabet = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
    unique_id = uuid.uuid4().int
    output = ""
    while unique_id:
        unique_id, digit = divmod(unique_id, len(alphabet))
        output += alphabet[digit]
    return output

uuid_object = pd.DataFrame(columns=['uuid', 'object'])                      # 关系 (uuid, object)
from_to = pd.DataFrame(columns=['from', 'to'])                              # 关系 (uuid "from", uuid "to")
parent_child = pd.DataFrame(columns=['parent', 'child'])                    # 关系 (uuid "parent", uuid "child")
original_doppelganger = pd.DataFrame(columns=['original', 'doppelganger'])  # 关系 (uuid "original", uuid "doppelganger")

def object2s(relation, column1, object1, column2):
    # 求所有 object2 使得 relation(column1 = object1, column2 = object2) 成立
    uuid1 = uuid_object.query("object = @object1").uuid.item()
    uuid2 = relation.query(f"{column1} = {uuid1}")[column2].item()
    object2s = uuid_object.query(f"uuid = {uuid2}").object
    return object2s



# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def suggest_host():
    pass

# ----------------------------------------------------------------------------------------------------------------------
# plugin: 自动继承 struct，自动覆盖 phi0, rho0, rho

