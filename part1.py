# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# 不重要

import pandas as pd, os, collections, subprocess
import ase, ase.io

LIB_PATH = os.path.dirname(os.path.realpath(__file__))
POTCAR_PATH = "/home/xzhang1/src/VASP_PSP/potpaw_PBE.54/"

def periodic_table_lookup(symbol, column, periodic_table = pd.read_excel(LIB_PATH + '/periodic_table.xlsx')):
    """
    :param str symbol: 'Pb'
    :param str column: 'pot_encut'
    """
    return periodic_table.loc[periodic_table.symbol == symbol, column].values[0]

def template(i, o, d):
    """
    i.format(d)
    :param str i: input file path
    :param str o: output file path
    :param dict d:
    """
    with open(i, "r") as i:
        with open(o, "w") as o:
            o.write(
                i.read().format(**d)
            )

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


"""
考虑单电子单核解。考虑多电子多核解。考虑其近似最小化问题。计算参数：材料，求值模式，简化近似，辅助行为。一一对应 (args = True) kwargs，
其规则变换对应 kwargs.exec。
hidden = {'hidden'}：非官方 kwargs
phi0 = path, rho0 = 0, rho = path：KS波函数、电荷密度的初值
kpoints = [template, param, ...]：KPOINTS 定式与参数
path：文件夹路
type = vasp：
"""
class D(collections.MutableMapping):
    """
    禁止覆盖。KeyError返回None。
    """
    def __init__(self, *args, **kwargs):
        self._dict = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        if key in self._dict:
            return self._dict[key]
        return None

    def __setitem__(self, key, value):
        if key in self._dict and self._dict[key] != value:
            raise SyntaxError("overwrite")
        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def exec(self, expr):
        exec(expr, globals(), self)

    # exec 文件用 # 分块
    def exec_file(self, file):
        for i in range(3):
            with open(file, "r") as file:
                for block in file.read().split('#'):
                    try:
                        self.exec('#' + block)
                    except:
                        if i == 2:
                            raise
