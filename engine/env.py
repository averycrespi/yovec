from copy import deepcopy
from typing import Any


class Env:
    """Represents a program environment."""
    def __init__(self, overwrite: bool=True):
        self.state = {}
        self.overwrite = overwrite

    def __str__(self) -> str:
        return '\n'.join('{} = {}'.format(k, str(v)) for k, v in self.state.items())

    def __getitem__(self, k: str) -> Any:
        return self.state[k]

    def items(self):
        return self.state.items()

    def update(self, k: str, v: Any) -> 'Env':
        """Update the environment."""
        if not self.overwrite and k in self.state.keys():
            raise KeyError('cannot overwrite existing key: {}'.format(k))
        new = deepcopy(self)
        new.state[k] = v
        return new
