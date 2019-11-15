# ----------------------------------------------------------------------------------------------------------------------
ops = {
    'vasp': [
        lambda h: h.d.exec('d_exec_vasp.py'),
        lambda h: d_struct_to_vasp(h.d, h.struct)
    ],
    'slurm': [
        lambda h: submit(h.d),
        lambda h: is_finished_on_slurm(h.d),
        lambda h: retrieve(h.d)
    ]
}

class DCG:
    """
    Dynamic computational graph. Stepwise execution.

    Example use:
        g(d=d, struct=struct).set_ops('vasp', 'slurm').step()

    :ivar *: `__init__` allows any attributes to be added
    :ivar list ops:
    """
    def __init__(self, **kwargs):
        """
        :param dict **kwargs: attributes to be added
        """
        self.__dict__.update(kwargs)

    def set_ops(self, *collections):
        """
        :param list *collections: keys in `ops`
        """
        self.ops = [op for collection in collections for op in ops[collection]]
        return self

    def step(self):
        if self.ops[0](self) in [True, None]:
            self.ops.pop(0)
            self.step()