# -*- coding: utf-8 -*-
import pandas as pd, os, unicodedata, re, collections
"""
§ 前言

opt → struct → elecstruct. 

给定 struct Pb19S44，考虑其 elecstruct. 

考虑单电子单核解。考虑多电子多核解。考虑其近似最小化问题。考虑近似 approx：材料，求值模式，简化近似，辅助行为。
"""

# § Constants

script_dir = os.path.dirname(os.path.realpath(__file__))

periodic_table = pd.read_excel(script_dir + '/periodic_table.xlsx')     #: pd.DataFrame, Periodic table


def slugify(value):
    """
    Make a string URL- and filename-friendly.

    Normalizes string into unicode, converts to lowercase, removes non-alpha-nu-
    merics, and converts spaces to hyphens.

    Taken from django/utils/text.py. In Django, a "slug" is a URL- and filename-
    friendly string.

    :param unicode value: String to be converted
    :return: Filename-friendly string
    :rtype: unicode
    :raises TypeError: if value is not unicode string

    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    return value


"""§ struct, approx"""


class Struct(object):
    """
    A struct is defined by a list of atomic coordinates, and optionally the repeat pattern.

    :ivar np.array(3,3) A: translation vector of crystal cell, or None
    :ivar pd.DataFrame(x,y,z,symbol) X: atomic coordinates

    """

    def __init__(self):
        super().__init__()
        self.A = None
        self.X = pd.DataFrame(columns=['x', 'y', 'z', 'symbol'])


class Approx(collections.MutableMapping):
    """
    考察 args, kwargs 的规则变换，规则为 python改：[2,3]

    - args实现为args=True
    - _变量名前缀表示"隐藏"，__getitem__时一并搜索。
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


"""§ 求解"""
# 完成计算本应是一行代码，但 i) Approx → Bash转换， ii) 本地 → 远程转换 造成一些程序细节。


def convert_approx_to_vasp(struct, approx):
    """
    1. 规则变换
    2. 输出文本文件、脚本文件

    """
    return path

def submit(path):
    ./submit


def retrieve(path):
    ./retrieve


"""§ 记录"""
# 图式数据库


UID = {}


IN = {}


ARC = {}


# § Extensions

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
