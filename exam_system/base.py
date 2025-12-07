#!/usr/local/bin/python


import pystache
render = pystache.Renderer(escape=lambda x:x)

def tostr(x):
    if isinstance(x, str):
        return x
    elif isinstance(x, (tuple, list)):
        return tuple(map(tostr, x))
    elif hasattr(x, 'dumps'):
        return x.dumps()
    else:
        return str(x)

        
class BaseTemplate:
    r"""
    template for math problems or the proof

    __template: str, template of a problem
    parameter: dict, parameters of a problem

    __str__: str
    totex: str, translate it to tex grammar

    Examples:
    --------
    >>> bt = BaseTemplate('I love {{name}}', {'name':'Lily'})
    >>> print(bt)
    # I love Lily

    import mymat
    bt = BaseTemplate('Matrix A = {{matrix}}', {'matrix':mymat.MyMat('1,2;3,4')})
    print(bt.totex())  # never use print(bt)
    # Matrix A = \begin{bmatrix}
    # 1.0 & 2.0\\
    # 3.0 & 4.0
    # \end{bmatrix}
    """

    def __init__(self, template='', parameter={}):
        self.template = template
        self.parameter = parameter

    def __len__(self):
        return len(self.parameter)

    def __getitem__(self, key):
        return self.parameter[key]

    def __setitem__(self, key, value):
        self.parameter[key] = value

    def update(self, *args, **kwargs):
        self.parameter.update(*args, **kwargs)

    @classmethod
    def fromDict(cls, d):
        return cls(d['template'], d['parameter'])

    def format(self, parameter=None):
        # the core of the class
        # call render method
        if parameter is None:
            parameter = self.parameter
        return render.render(self.template, parameter)

    def __str__(self):
        # convert to string
        parameter = {key: tostr(val) for key, val in self.parameter.items()}
        return self.format(parameter)

    def totex(self):
        # convert to tex form
        parameter = {}
        for key, val in self.parameter.items():
            if hasattr(val, 'totex'):
                parameter[key] = val.totex()
            elif hasattr(val, 'dumps'):
                parameter[key] = val.dumps()
            else:
                parameter[key] = tostr(val)
        return self.format(parameter)

    def setstate_template(self, state):
        self.template = state['template']

    def __setstate__(self, state):
        self.setstate_template(state)
        if 'parameter' in state:
            if state['parameter']:
                self.parameter = state['parameter']
            else:
                self.parameter = {}
        else:
            self.parameter = {}

    def convert(self, func):
        # convert the values in parameter dictionary
        if callable(func):
            for key, val in self.parameter.items():
                self.parameter[key] = func(val)
        elif isinstance(func, dict):
            for key, val in self.parameter.items():
                self.parameter[key] = func[val]
        else:
            # func is a constant
            for key, val in self.parameter.items():
                self.parameter[key] = func

    def mask_with(self, keys={'answer'}, mask='***'):
        '''mask the some parameters
        In examination, you have to mask the answer
        In login interface, you have to mask the password
        '''
        for key in keys:
            self[key] = mask

