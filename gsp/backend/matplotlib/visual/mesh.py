# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from gsp.backend.matplotlib.core import Buffer
from gsp.backend.matplotlib.transform import Mat4x4, Transform


class Mesh:
    def __init__(self, viewport, vertices, faces,
                       fill_colors, edge_colors, edge_width=0.5,
                       mode = None):

        self._viewport = viewport
        self._mode = mode
        self._vertices = vertices
        self._faces = faces
        self._fill_colors = fill_colors
        self._edge_colors = edge_colors
        self._edge_width = edge_width
        self._collection = PolyCollection([], clip_on=False, snap=False)
        self._viewport.axes.add_collection(self._collection, autolim=False)
        self._transform = Mat4x4(np.zeros(16,np.float32))

    def frontback(self, T):
        """
        Sort front and back facing triangles

        Parameters:
        -----------
        T : (n,3) array

           Triangles to sort

        Returns:
        --------
        front and back facing triangles as (n1,3) and (n2,3) arrays (n1+n2=n)
        """
        Z = (T[:,1,0]-T[:,0,0])*(T[:,1,1]+T[:,0,1]) + \
            (T[:,2,0]-T[:,1,0])*(T[:,2,1]+T[:,1,1]) + \
            (T[:,0,0]-T[:,2,0])*(T[:,0,1]+T[:,2,1])
        return Z < 0, Z >= 0


    def render(self, transform):

        # Update internal transform with given transform
        self._transform.set_data(transform)

        # Get vertices
        if isinstance(self._vertices, Transform):
            vertices = self._vertices.evaluate()
        else:
            vertices = np.asarray(self._vertices)
        vertices = vertices.view(np.float32).reshape(-1,3)
        
        # Get faces
        if isinstance(self._faces, Transform):
            faces = self._faces.evaluate()
        else:
            faces = np.asarray(self._faces)
        faces = faces.view(np.int64).reshape(-1,3)
        
        # Compute tranformed triangles (T) and their (mean) depth (Z)
        T = self._transform(vertices)[faces]
        Z = -T[:,:,2].mean(axis=1)

        # Check which mode to use
        index = None
        if self._mode == "front":
            index, _ = self.frontback(T)
            T, Z = T[index], Z[index]
        elif self._mode == "back":
            _, index = self.frontback(T)
            T, Z = T[index], Z[index]

        # Fill colors
        FC = self._fill_colors
        if isinstance(FC, Transform):
            FC = FC.evaluate({"depth": Z, "index": index})
        elif index is not None:
            FC = np.asarray(FC)[index]
        else:
            FC = np.asarray(FC)

        # Edge colors
        EC = self._edge_colors
        if isinstance(EC, Transform):
            EC = EC.evaluate({"depth": Z, "index": index})
        elif index is not None:
            EC = np.asarray(EC)[index]
        else:
            EC = np.asarray(EC)
                
        # Get 2d triangles
        T = T[:,:,:2]
        
        # Sort triangles according to z buffer
        I = np.argsort(Z)
        
        self._collection.set_verts(T[I,:])
        self._collection.set_linewidths(self._edge_width)
        self._collection.set_facecolors(FC[I,:])
        self._collection.set_edgecolors(EC[I,:])
        self._collection.set_antialiased(True)
