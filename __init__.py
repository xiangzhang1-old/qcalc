# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# 不重要

import pandas as pd, os, unicodedata, re, collections, subprocess
import ase, ase.io

LIB_PATH = os.path.dirname(os.path.realpath(__file__))
POTCAR_PATH = "/home/xzhang1/src/VASP_PSP/potpaw_PBE.54/"

def _periodic_table_lookup(symbol, column, periodic_table = pd.read_excel(LIB_PATH + '/periodic_table.xlsx')):
    """
    :param str symbol: 'Pb'
    :param str column: 'pot_encut'
    """
    return periodic_table.loc[periodic_table.symbol == symbol, column].values[0]

def _slugify(value):
    """
    Make a string URL- and filename-friendly.
    Taken from django/utils/text.py. In Django, a "slug" is a URL- and filename-friendly string.

    :param unicode value: string to be converted
    :return: filename-friendly string
    :rtype: unicode
    :raises TypeError: if value is not unicode string
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value

"""---------------------------------------------------------------------------------------------------------------------

opt → struct → elecstruct

给定 struct Pb19S44，考虑其 elecstruct. 

A struct is defined by a list of atomic coordinates, and optionally the repeat pattern."""
class Struct(object):
    """
    :ivar np.array(3,3) A: translation vector of crystal cell, or None
    :ivar pd.DataFrame(x,y,z,symbol) X: cartesian coordinates, ascendingly sorted by symbol
    """

    def __init__(self):
        super().__init__()
        self.A = None
        self.X = pd.DataFrame(columns=['x', 'y', 'z', 'symbol'])

    """例："""
    @property
    def stoichiometry(self):
        """
        Make X sorted by symbol A-Z, returns count sorted by symbol A-Z.
        """
        self.X.sort_values(by='symbol', inplace=True)
        return collections.OrderedDict(self.X.symbol.value_counts(ascending=True))


"""考虑单电子单核解。考虑多电子多核解。考虑其近似最小化问题。考虑近似：材料，求值模式，简化近似，辅助行为。"""
# class dict:
# 考察 args, kwargs
# - args实现为args=True
# - _ 变量名前缀表示"隐藏"。Alternatively,

class Getopt(collections.MutableMapping):
    """
    考察 args, kwargs 的规则变换，规则为 python改：[2,3]
    - args实现为args=True
    - _ 变量名前缀表示"隐藏"，__getitem__时一并搜索。
    - __getitem__未搜索到时返回None。
    - __setitem__时禁止覆盖。
    """
    def __init__(self):
        self._dict = dict()

    def __getitem__(self, key):
        if key in self._dict:
            return self._dict[key]
        if key.startswith('_') and key[1:] in self._dict:
            return self._dict[key[1:]]
        return None

    def __setitem__(self, key, value):
        if key in self._dict and self._dict[key] != value:
            raise SyntaxError("overwrite")
        self._dict[key] = value

    def __delitem__(self, key):
        raise SyntaxError("overwrite")

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def exec(self, expr):
        exec(expr, globals(), self)

# getopt.exec("pbs=qd=True; opt=True; ediffg=1E-3")
#
# with open("getopt.vasp", "r") as file:     # if opt:   ediff=1E-4  # bourbaki
#     for line in file:
#         getopt.exec(line)

# ----------------------------------------------------------------------------------------------------------------------
# vasp(struct, getopt)

# 完成计算本应是上面一行代码，但有些平凡事务：

def _struct_to_poscar(struct):
    """
    :param Struct struct:
    :return: writes POSCAR4 to current directory
    """
    stoichiometry = ''.join([f'{k}{v}' for k,v in struct.stoichiometry.items()])
    atoms = ase.Atoms(symbols=struct.X['symbol'], positions=struct.X[['x','y','z']], cell=struct.A)
    ase.io.write("POSCAR", images=atoms, format="vasp")

def _struct_to_potcar(struct):
    """
    :param Struct struct:
    :return: writes POTCAR to current directory
    """
    for symbol in struct.stoichiometry:
        fp = POTCAR_PATH + _periodic_table_lookup(symbol, "pot") + "/POTCAR"
        # we will repeatedly use this trick: str.format(dict) and f"{var}"
        subprocess.run(f"cat {fp} >> POTCAR", shell=True)

def getopt_struct_to_vasp(getopt, struct):
    """
    :param Getopt getopt:
    :param Struct struct:
    :return: converts getopt, struct to VASP files (INCAR, POSCAR, KPOINTS, POTCAR) in current directory
    """
    os.chdir(getopt['path'])
    #
    with open("INCAR", "w") as file:
        for k, v in getopt.items():
            if not k.startswith('_'):
                file.write("{k} = {v}\n")

# 输出文本文件: INCAR, POSCAR, KPOINTS, POTCAR (struct, getopt), CHG



to_poscar(struct)

template("KPOINTS", getopt)

for symbol in struct.stoichiometry.keys():
    to_pot(symbol)

# 输出脚本文件
template("run", getopt)
subprocess.call("./run")


# § 图式关系

UID_OBJ = {}

PARENT_CHILD = []

FROM_TO = []


uid = UUID.UUID4()
UID_OBJ[uid] = _
PARENT_CHILD[__] = _
...
















# § Extensions





# ----

readyfunc_func = []

# ----

def suggest_host():
    pass

CLONE = []

def add_clone():
    pass

def cleanup_clone():
    pass


"""
§ 引文

1. InDesign 的默认设置是 1/4 的全角空格宽度（遵从 JIS），也就是约等于一个半角空格。源：zhihu 19587406
2. If provided, `locals` can be any mapping object. 源：Python3 官方文档，exec()
3. None of the built-in methods will call your custom __getitem__ / __setitem__, though. If you need total control over 
these, create a custom class that implements the collections.MutableMapping abstract base class instead. 
源：stackoverflow 7148419。
"""
