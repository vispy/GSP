# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import numpy as np
from gsp import glm
from gsp.core import Buffer, Color
from gsp.transform import Transform
from gsp.io.command import command


class Light(Transform):
    """
    Light transform allows to modify faces color according to light parameters
    """

    @command("transform.Light")
    def __init__(self,
                 direction : list         = (1,1,1),
                 ambient_color : Color    = (1,0,0,0.2),
                 diffuse_color : Color    = (1,1,1,0.8),
                 specular_color : Color   = (1,1,1,0)):
        """
        Light transform allows to modify faces color according to light parameters

        Parameters
        ----------
        direction:
            Direction of the light
        ambient_color:
            Ambient color, alpha component being strength
        diffuse_color:
            Diffuse color, alpha component being strength
        specular_color:
            Specular color, alpha component being shininess
        """

        Transform.__init__(self, __no_command__ = True)
        self._direction = np.asanyarray(direction)

        self._ambient_color = np.asanyarray(ambient_color)
        self._ambient_strength = self._ambient_color[3]
        self._ambient_color[3] = 1

        self._diffuse_color = np.asanyarray(diffuse_color)
        self._diffuse_strength = self._diffuse_color[3]
        self._diffuse_color[3] = 1

        self._specular_color = np.asanyarray(specular_color)
        self._shininess = self._specular_color[3]
        self._specular_color[3] = 1

    def copy(self):
        transform = Transform.copy(self)
        transform._direction = self._direction
        transform._ambient_color = self._ambient_color
        transform._ambient_strength = self._ambient_strength
        transform._diffuse_color = self._diffuse_color
        transform._diffuse_strength = self._diffuse_strength
        transform._specular_color = self._specular_color
        transform._shininess = self._shininess
        return transform

    def evaluate(self, buffers):

        if self._next:
            F = self._next.evaluate(buffers)
        else:
            F = self._buffer

        # Faces center
        C = F.mean(axis=1)

        # Faces normal
        N = glm.normalize(np.cross(F[:,2]-F[:,0], F[:,1]-F[:,0]))

        # Relative light direction
        D = glm.normalize(C - self._direction)

        # Diffuse term
        diffuse = glm.clamp((N*D).sum(-1).reshape(-1,1))

        # Specular term
        specular = 0
        if self._shininess:
            specular = np.power(diffuse, self._shininess)

        ambient_color = glm.sRGBA_to_RGBA(self._ambient_color)
        diffuse_color = glm.sRGBA_to_RGBA(self._diffuse_color)
        specular_color = glm.sRGBA_to_RGBA(self._specular_color)
        color = (             ambient_color * self._ambient_strength
                 + diffuse *  diffuse_color * self._diffuse_strength
                 + specular * specular_color)
        color[:,3] = 1
        color = glm.RGBA_to_sRGBA(color)

        return np.minimum(1, color)
