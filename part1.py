import collections
import pandas as pd

# ----------------------------------------------------------------------------------------------------------------------

class Struct(object):
    """
    Attributes:
        A (3x3 numpy array): translation vector of unit cell, or None
        X (pandas DataFrame: x, y, z, symbol): cartesian coordinates
    """

    def __init__(self):
        super().__init__()
        self.A = None
        self.X = pd.DataFrame(columns=['x', 'y', 'z', 'symbol'])

    @property
    def stoichiometry(self):
        """
        Returns:
            OrderedDict: stoichiometry sorted by symbol A-Z.
        """
        self.X.sort_values(by='symbol', inplace=True)
        return collections.OrderedDict(self.X.symbol.value_counts(ascending=True))

class D(collections.MutableMapping):
    """
    计算：
        ops = ['vasp', 'slurm']
    计算参数，包括材料相关，求值模式，简化近似，辅助行为：
        vasp:
            hidden = {'hidden'}: 不写入 INCAR
            kpoints = [template, ...]：KPOINTS 模板
            phi0 = path, rho0 = 0, rho = path：迭代初始值
            path
        slurm:
            remote
    参数规则:
        d.exec。
    """
    def __init__(self, *args, **kwargs):
        self._dict = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self._dict[key]

    # 避免意外 overwrite
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
