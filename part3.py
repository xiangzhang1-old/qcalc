# ----------------------------------------------------------------------------------------------------------------------
"""Op"""

op_dict = {
    'vasp': [
        lambda h: h.d.exec('d_exec_vasp.py'),
        lambda h: d_struct_to_vasp(h.d, h.struct)
    ],
    'slurm': [
        lambda h: submit(h.d),
        lambda h: is_complete(h.d),
        lambda h: retrieve(h.d)
    ]
}

class Graph:
    """A collection of ops, to be stepwise executed.

    Example:
        dcn(d=d, struct=struct).set_ops('vasp', 'slurm').step()

    Attributes:
        ops (list): list of lambda functions to execute
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def set_ops(self, *ops):
        """
        Args:
            ops (list): contains op_dict's keys
        """
        self.ops = []
        for op in ops:
            self.ops += op_dict[op]
        return self

    def step(self):
        if self.ops[0](self) in [True, None]:
            self.ops.pop(0)
            self.step()