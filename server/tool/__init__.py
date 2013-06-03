import os

__all__ = []

for f in os.listdir(os.path.abspath(os.path.dirname(__file__))):
    if f[0] is '_' or f[-3:] not in ['.so', '.py']:
        continue
    plugin = f.split('.')[0]
    __all__.append(plugin)
    __import__(plugin, globals(), locals(), level=1)
del f
