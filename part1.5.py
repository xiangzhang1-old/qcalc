# ----------------------------------------------------------------------------------------------------------------------
# vasp(d, struct)

def d_struct_to_vasp(d, struct):
    """
    输出文本文件: INCAR, POSCAR4, KPOINTS, POTCAR, CHGCAR/WAVECAR
    :param dict d:
    :param Struct struct:
    :return: converts d, struct to VASP files (INCAR, POSCAR, KPOINTS, POTCAR) in current directory
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
# slurm(d)

def submit(d):
    template(i = f"{LIB_PATH}/submit.{d['transforms'][0]}.{d['host']}", o = "submit", d = d)
    template(i = f"{LIB_PATH}/job.{d['transforms'][0]}.{d['host']}", o = "job", d = d)
    subprocess.run("bash submit", shell=True)

def is_complete_on_slurm(d):
    template(i=f"{LIB_PATH}/is_complete_on_slurm.{d['host']}", o="is_complete", d = d)
    return eval(subprocess.check_output("bash is_complete", shell=True))

def retrieve(d):
    template(i=f"{LIB_PATH}/retrieve.{d['host']}", o="retrieve", d = d)
    subprocess.run("bash retrieve", shell=True)




