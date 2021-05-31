import unicodedata, re

def slugify(value):
    """str.strip(), but better.

    Make a string URL- and filename-friendly.

    Args:
        value (unicode): string to be converted

    Returns:
        unicode: filename-friendly string

    Raises:
        TypeError: if value is not unicode string
    """
    value = unicodedata.normalize('NFKD', value)
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value

def exec_shorthand(d, text):
    # exec_shorthand(d, "insulator, qd, spin=fm")
    for _ in text.split(','):
        _ = slugify(_)
        if '=' not in _:        # insulator
            d[_] = None
        else:                   # kpoints=[1,1] or sp=in=fm
            l, r = _.split('=')
            l, r = slugify(l), slugify(r)
            try:                # kpoints=[1,1]
                d[l] = eval(r)
            except NameError:   # spin=fm
                d[l] = r

def exec_file(d, file):
    # 文件用 # 分块
    for i in range(3):
        with open(file, "r") as file:
            for block in file.read().split('#'):
                try:
                    d.exec('#' + block)
                except:
                    if i == 2:
                        raise
# ----------------------------------------------------------------------------------------------------------------------

def uuid4():
    """Generates a random UUID.UUID4 encoded in base57.

    Author: `shortuuid<https://github.com/skorokithakis/shortuuid/blob/master/shortuuid/main.py>`
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
original_symlink = pd.DataFrame(columns=['original', 'symlink'])            # 关系 (uuid "original", uuid "doppelganger")

def object2s(relation, column1, object1, column2):
    # 求所有 object2 使得 relation(column1 = object1, column2 = object2) 成立
    uuid1 = uuid_object.query("object = @object1").uuid.item()
    uuid2 = relation.query(f"{column1} = {uuid1}")[column2].item()
    object2s = uuid_object.query(f"uuid = {uuid2}").object
    return object2s

# ----------------------------------------------------------------------------------------------------------------------
def suggest_host():
    pass

# ----------------------------------------------------------------------------------------------------------------------
# plugin: 自动继承 struct，自动覆盖 phi0, rho0, rho

