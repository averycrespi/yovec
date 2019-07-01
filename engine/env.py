from copy import deepcopy


class Env:
    """Represents a program environment."""
    def __init__(self, overwrite=True):
        self.state = {}
        self.overwrite = overwrite

    def __str__(self):
        return '\n'.join('{} = {}'.format(k, str(v)) for k, v in self.state.items())

    def __getitem__(self, k):
        return self.state[k]

    def update(self, k, v):
        if not self.overwrite and k in self.state.keys():
            raise KeyError('cannot overwrite key: {}'.format(k))
        dupe = deepcopy(self)
        new.state[k] = v
        return new
