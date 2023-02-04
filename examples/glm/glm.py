# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np

# vec2 = np.dtype([("x", np.float32),
#                  ("y", np.float32)])
# vec3 = np.dtype([("x", np.float32),
#                  ("y", np.float32),
#                  ("z", np.float32)])
# vec4 = np.dtype([("x", np.float32),
#                  ("y", np.float32),
#                  ("z", np.float32),
#                  ("w", np.float32)])
# mat3x3 = np.dtype((np.float32, (3,3)))
# mat4x4 = np.dtype((np.float32, (4,4)))
# rgba = np.dtype([("r", np.float32),
#                  ("g", np.float32),
#                  ("b", np.float32),
#                  ("a", np.float32) ])

def normalize(X):
    return X/(1e-16+np.sqrt((np.array(X)**2).sum(axis=-1)))[..., np.newaxis]

def clip(V, vmin=0, vmax=1):
    return np.minimum(np.maximum(V,vmin),vmax)


def viewport(x, y, w, h, d):
    """ Viewport matrix """
    return np.array([[w/2, 0, 0, x+w/2],
                     [0, h/2, 0, y+h/2],
                     [0, 0, d/2,   d/2],
                     [0, 0, 0,       1]], dtype=np.float32)


def frustum(left, right, bottom, top, znear, zfar):
    """Create view frustum

    Parameters
    ----------
    left : float
        Left coordinate of the field of view.
    right : float
        Right coordinate of the field of view.
    bottom : float
        Bottom coordinate of the field of view.
    top : float
        Top coordinate of the field of view.
    znear : float
        Near coordinate of the field of view.
    zfar : float
        Far coordinate of the field of view.

    Returns
    -------
    View frustum matrix (4x4 array)
    """

    M = np.zeros((4, 4), dtype=np.float32)
    M[0, 0] = +2.0 * znear / (right - left)
    M[1, 1] = +2.0 * znear / (top - bottom)
    M[2, 2] = -(zfar + znear) / (zfar - znear)
    M[0, 2] = (right + left) / (right - left)
    M[2, 1] = (top + bottom) / (top - bottom)
    M[2, 3] = -2.0 * znear * zfar / (zfar - znear)
    M[3, 2] = -1.0
    return M


def perspective(fovy, aspect, znear, zfar):
    """Create perspective projection matrix

    Parameters
    ----------
    fovy : float
        The field of view along the y axis.
    aspect : float
        Aspect ratio of the view.
    znear : float
        Near coordinate of the field of view.
    zfar : float
        Far coordinate of the field of view.

    Returns
    -------
    Perspective projection matrix (4x4 array)
    """

    h = np.tan(0.5*np.radians(fovy)) * znear
    w = h * aspect
    return frustum(-w, w, -h, h, znear, zfar)


def ortho(left, right, bottom, top, znear, zfar):
    """Create orthographic projection matrix

    Parameters
    ----------
    left : float
        Left coordinate of the field of view.
    right : float
        Right coordinate of the field of view.
    bottom : float
        Bottom coordinate of the field of view.
    top : float
        Top coordinate of the field of view.
    znear : float
        Near coordinate of the field of view.
    zfar : float
        Far coordinate of the field of view.

    Returns
    -------
    Orthographic projection matrix (4x4 array)
    """

    M = np.zeros((4, 4), dtype=np.float32)
    M[0, 0] = +2.0 / (right - left)
    M[1, 1] = +2.0 / (top - bottom)
    M[2, 2] = -2.0 / (zfar - znear)
    M[3, 3] = 1.0
    M[0, 2] = -(right + left) / float(right - left)
    M[1, 3] = -(top + bottom) / float(top - bottom)
    M[2, 3] = -(zfar + znear) / float(zfar - znear)
    return M


def scale(x=1, y=None, z=None):
    """Non-uniform scaling along the x, y, and z axes

    Parameters
    ----------
    x : float
        X coordinate of the translation vector.
    y : float | None
        Y coordinate of the translation vector. If None, `x` will be used.
    z : float | None
        Z coordinate of the translation vector. If None, `x` will be used.

    Returns
    -------
    Scaling matrix (4x4 array)
    """

    y = y or x
    z = z or x
    return np.array([[x, 0, 0, 0],
                     [0, y, 0, 0],
                     [0, 0, z, 0],
                     [0, 0, 0, 1]], dtype=np.float32)


def translate(x=0, y=0, z=0):
    """
    Translate by an offset (x, y, z) .

    Parameters
    ----------
    x : float
        X coordinate of a translation vector.
    y : float | None
        Y coordinate of translation vector. If None, `x` will be used.
    z : float | None
        Z coordinate of translation vector. If None, `x` will be used.

    Returns
    -------
    Translation matrix (4x4 array)
    """
    
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]], dtype=np.float32)


def xrotate(theta=0):
    """Rotation about the X axis

    Parameters
    ----------
    theta : float
        Specifies the angle of rotation, in degrees.

    Returns
    -------
    Rotation matrix (4x4 array)
    """

    t = np.radians(theta)
    c, s = np.cos(t), np.sin(t)
    return np.array([[1, 0,  0, 0],
                     [0, c, -s, 0],
                     [0, s,  c, 0],
                     [0, 0,  0, 1]], dtype=np.float32)

def yrotate(theta=0):
    """Rotation about the Y axis

    Parameters
    ----------
    theta : float
        Specifies the angle of rotation, in degrees.

    Returns
    -------
    Rotation matrix (4x4 array)
    """

    t = np.radians(theta)
    c, s = np.cos(t), np.sin(t)
    return  np.array([[ c, 0, s, 0],
                      [ 0, 1, 0, 0],
                      [-s, 0, c, 0],
                      [ 0, 0, 0, 1]], dtype=np.float32)

def zrotate(theta=0):
    """Rotation about the Z axis

    Parameters
    ----------
    theta : float
        Specifies the angle of rotation, in degrees.

    Returns
    -------
    Rotation matrix (4x4 array)
    """

    t = np.radians(theta)
    c, s = np.cos(t), np.sin(t)
    return np.array([[ c, -s, 0, 0],
                     [ s,  c, 0, 0],
                     [ 0,  0, 1, 0],
                     [ 0,  0, 0, 1]], dtype=np.float32)

def rotate(theta=0, x=0, y=0, z=1):
    """Rotation about an arbitrary X axis

    Parameters
    ----------
    theta : float
        Specifies the angle of rotation, in degrees.

    x,y,z : float
        Axis of rotation

    Returns
    -------
    Rotation matrix (4x4 array)
    """
    
    t = np.radians(theta)
    axis = normalize(np.asarray([x,y,z], dtype=np.float32))
    a = np.cos(t/2)
    b, c, d = -axis*np.sin(t/2)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac), 0],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab), 0],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc, 0],
                     [0,0,0,1]], dtype=np.float32)


def align(U, V):
    """ Find the rotation matrix that aligns U to V """
    a,b = normalize(U), normalize(V)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    K = np.array([[   0, -v[2], v[1]],
                  [ v[2],   0, -v[0]],
                  [-v[1], v[0],   0]])
    R = np.zeros((4,4), dtype=np.float32)
    R[:3, :3] = np.eye(3) + K + K@K * ((1 - c) / (s ** 2))
    R[3, 3] = 1
    return R

        
def fit_unit_cube(V):
    """ Fit vertices V into the unit cube (in place) """
    
    xmin, xmax = V[:,0].min(), V[:,0].max()
    ymin, ymax = V[:,1].min(), V[:,1].max()
    zmin, zmax = V[:,2].min(), V[:,2].max()
    scale = max([xmax-xmin, ymax-ymin, zmax-zmin])
    V /= scale
    V[:,0] -= (xmax+xmin)/2/scale
    V[:,1] -= (ymax+ymin)/2/scale
    V[:,2] -= (zmax+zmin)/2/scale
    return V

    
def transform(V, mvp, viewport=None):
    """
    Apply transform mvp to vertices V

    Parameters
    ----------
    V : (n,3) array
      Vertices array

    mvp: 4x4 array
      Transform matrix

    viewport: 4x4 array
      Viewport matrix (default is None)

    Returns
    -------
    (n,3) array of transformed vertices
    """
    
    V = np.asarray(V, dtype=np.float32) 
    shape = V.shape
    V = V.reshape(-1,3)
    ones = np.ones(len(V), dtype=float)
    V = np.c_[V.astype(float), ones]      # Homogenous coordinates
    V = V @ mvp.T                         # Transformed coordinates
    if viewport is not None:
        V = V @ viewport.T
    V = V/V[:,3].reshape(-1,1)            # Normalization
    V = V[:,:3]                           # Normalized device coordinates
    return V.reshape(shape)


def frontback(T):
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


def lookat(eye=(0,0,4.5), center=(0,0,0), up=(0,0,1)):
    """
    Creates a viewing matrix derived from an eye point, a reference
    point indicating the center of the scene, and an up vector.

    Parameters:
    -----------
    eye : array-like
       Eye point

    center : array-like
       Reference point

    up : array-like 
       Up vector

    Returns:
    --------
    View matrix (4x4 array)
    """
    
    Z = normalize(np.asarray(eye, dtype=np.float32) -
                  np.asarray(center, dtype=np.float32))
    Y = np.asarray(up, dtype=np.float32)
    X = normalize(np.cross(Y, Z))
    Y = normalize(np.cross(Z, X))    
    return np.array([
        [X[0], X[1], X[2], -np.dot(X, eye)],
        [Y[0], Y[1], Y[2], -np.dot(Y, eye)],
        [Z[0], Z[1], Z[2], -np.dot(Z, eye)],
        [0, 0, 0, 1]])


def camera(xrotation=25, yrotation=45, zoom=1, mode="perspective"):
    xrotation = min(max(xrotation, 0), 90)
    yrotation = min(max(yrotation, 0), 90)
    zoom = max(0.1, zoom)
    model = scale(zoom,zoom,zoom) @ xrotate(xrotation) @ yrotate(yrotation) 
    view  = translate(0, 0, -4.5)
    if mode == "ortho":
        proj  = ortho(-1, +1, -1, +1, 1, 100)
    else:
        proj  = perspective(25, 1, 1, 100)
    return proj @ view  @ model                   
