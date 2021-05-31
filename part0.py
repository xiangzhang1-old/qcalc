import os
import pandas as pd

LIB_PATH = os.path.dirname(os.path.realpath(__file__))
POTCAR_PATH = "/home/xzhang1/src/VASP_PSP/potpaw_PBE.54/"

def periodic_table_lookup(symbol, column, periodic_table = pd.read_excel(LIB_PATH + '/periodic_table.xlsx')):
    """
    Args:
        symbol (str): 'Pb'
        column (str): 'pot_encut'
    """
    return periodic_table.loc[periodic_table.symbol == symbol, column].values[0]

def template(i, o, d):
    """i.format(d)

    Args:
        i (str): input file path
        o （str): output file path
        d (dict):
    """
    with open(i, "r") as i:
        with open(o, "w") as o:
            o.write(
                i.read().format(**d)
            )