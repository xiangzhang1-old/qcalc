import os, subprocess
import pandas as pd
import ase

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

# ----------------------------------------------------------------------------------------------------------------------

def d_struct_to_vasp(d, struct):
    """输出 INCAR, POSCAR4, KPOINTS, POTCAR。拷贝 CHGCAR/WAVECAR。
    """
    with open("INCAR", "w") as file:
        for k, v in d.items():
            if k not in d['hidden']:
                file.write("{k} = {v}\n")
    #
    atoms = ase.Atoms(symbols=struct.X['symbol'], positions=struct.X[['x', 'y', 'z']], cell=struct.A)
    ase.io.write("POSCAR", images=atoms, format="vasp")
    #
    template(i = f"{LIB_PATH}/KPOINTS.{d['kpoints'][0]}", o = "KPOINTS", d = d)
    #
    for symbol in struct.stoichiometry:
        potcar = POTCAR_PATH + periodic_table_lookup(symbol, "pot") + "/POTCAR"
        subprocess.run(f"cat {potcar} >> POTCAR", shell=True)
    #
    for path in [d[k] for k in ['rho', 'rho0', 'phi0'] if k in d]:
        subprocess.run(f"rsync -a -h --info=progress2 {path} .", shell=True)

# ----------------------------------------------------------------------------------------------------------------------

def submit(d):
    template(i = f"{LIB_PATH}/submit.{d['software']}.{d['cluster']}", o = "submit", d = d)
    template(i = f"{LIB_PATH}/job.{d['software']}.{d['cluster']}", o = "job", d = d)
    subprocess.run("bash submit", shell=True)

def is_complete_on_slurm(d):
    template(i=f"{LIB_PATH}/is_complete.{d['cluster']}", o="is_complete", d = d)
    return eval(subprocess.check_output("bash is_complete", shell=True))

def retrieve(d):
    template(i=f"{LIB_PATH}/retrieve.{d['cluster']}", o="retrieve", d = d)
    subprocess.run("bash retrieve", shell=True)




