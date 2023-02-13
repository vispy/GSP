# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------

class Color:
    def __init__(self, red : float,
                       green : float,
                       blue : float,
                       alpha : float):
        self._color = red, green, blue, alpha

    def __array__(self):
        return self._color

    def __getitem__(self, index):
        return self._color[index]
    
    def __len__(self):
        return len(self._color)
