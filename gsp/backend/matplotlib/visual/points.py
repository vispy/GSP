# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from typing import Union

Color = list[float,float,float,float]
     
class Points:
    def __init__(self,
                 positions   : Buffer,
                 diameters   : Union[Buffer, float], 
                 fill_colors : Union[Buffer, Color]
                 edge_colors : Union[Buffer, Color],
                 edge_widths : Union[Buffer, float]):
        
        self.positions = positions
        self.diameters = diameters
        self.fill_colors = fill_colors
        self.edge_colors = edge_colors
        self.edge_widths = edge_widths

