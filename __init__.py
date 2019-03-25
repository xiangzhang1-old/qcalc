# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# 不重要

import pandas as pd, os, unicodedata, re, collections, subprocess
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
    we will repeatedly use this trick: str.format(**dict) and f"{var}"
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
其规则变换对应 exec(kwargs)。
hidden = {'hidden'}：非官方 kwargs
phi0 = path, rho0 = 0, rho = path：KS波函数、电荷密度的初值
kpoints = [template, param, ...]：KPOINTS 定式与参数
path：文件夹路径
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
# for i in range(3):
#     with open("d.exec.vasp.py", "r") as file:
#         for block in file.read().split('#'):
#             try:
#                 d.exec('#'+block)
#             except:
#                 if i == 2:
#                     raise

# ----------------------------------------------------------------------------------------------------------------------
# vasp(struct, getopt)

# 完成计算本应是上面一行代码，但有些平凡的转换：

def d_struct_to_vasp(d, struct):
    """
    输出文本文件: INCAR, POSCAR4, KPOINTS, POTCAR, CHGCAR/WAVECAR
    :param dict d:
    :param Struct struct:
    :return: converts d, struct to VASP files (INCAR, POSCAR, KPOINTS, POTCAR) in current directory
    """
    os.chdir(d['path'])
    #
    with open("INCAR", "w") as file:
        for k, v in d.items():
            if k not in d['hidden']:
                file.write("{k} = {v}\n")
    #
    atoms = ase.Atoms(symbols=struct.X['symbol'], positions=struct.X[['x', 'y', 'z']], cell=struct.A)
    ase.io.write("POSCAR", images=atoms, format="vasp")
    #
    template(i = f"{LIB_PATH}/KPOINTS.template.{d['kpoints'][0]}", o = "KPOINTS", d = d)
    #
    for symbol in struct.stoichiometry:
        fp = POTCAR_PATH + periodic_table_lookup(symbol, "pot") + "/POTCAR"
        subprocess.run(f"cat {fp} >> POTCAR", shell=True)
    #
    for path in [d[k] for k in ['rho', 'rho0', 'phi0'] if k in d]:
        subprocess.run(f"rsync -a -h --info=progress2 {path} .", shell=True)

def d_to_slurm(d):
    template(i = f"{LIB_PATH}/submit.template.vasp.{d['host']}", o = "submit", d = d)
    template(i = f"{LIB_PATH}/job.template.vasp.{d['host']}", o = "job", d = d)

# ----------------------------------------------------------------------------------------------------------------------
uuid_object = pd.DataFrame(columns=['uuid', 'object'])                      # 关系 (uuid, object)
prev_next = pd.DataFrame(columns=['prev', 'next'])                          # 关系 (uuid "prev", uuid "next")
parent_child = pd.DataFrame(columns=['parent', 'child'])                    # 关系 (uuid "parent", uuid "child")
original_doppelganger = pd.DataFrame(columns=['original', 'doppelganger'])  # 关系 (uuid "original", uuid "doppelganger")