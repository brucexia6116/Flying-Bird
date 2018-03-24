import numpy as np

def scale(a, b=None, c=None):
    """
    Creates a matrix with a affine transformation that scales the geometry

    Usage:
    >>> scale(d) # returns Mat4 that scles by d in all riections
    >>> scale(dx, dy) # returns Mat3 that scales by dx, dy
    >>> scale([dx, dy]) # same as above
    >>> scale(np.array([dx, dy])) # same as above
    >>> scale(dx, dy, dz) # returns Mat4 that scales by dx, dy, dz
    >>> scale([dx, dy, dz]) # same as above
    >>> scale(np.array([dx, dy, dz])) # same as above

    :return: matrix that will scale by spesified value
    """

    if b is None and c is None:
        if type(a) == list:
            return scale(np.array(a, dtype=np.float32))
        elif type(a) == np.ndarray and len(a.shape) == 1:
            return np.diag(np.concatenate([a, np.array([1], dtype=a.dtype)]))
        elif type(a) is float or type(a) is np.float32 or type(a) is np.float64:
            return scale(np.array([a, a, a], np.float32))
        else: raise Exception("argument has wrong type or dimentions", a)
    elif c is None:
        return scale(np.array([a, b], dtype=np.float32))
    else:
        return scale(np.array([a, b, c], dtype=np.float32))

def translate(a, b=None, c=None):
    """
    Create a translation Matrix

    Usage:
    >>> translate(dx, dy) # translates by dx, dy (res is Mat3)
    >>> translate([dx, dy]) # same as above
    >>> translate(np.array([dx, dy])) # same as above
    >>> translate(dx, dy, dz) # tranlates by dx, dy, dz (res is Mat4)
    >>> translate([dx, dy, dz]) # same as above
    >>> translate(np.array([dx, dy, dz])) # same as above

    :return:
    """

    if b is None and c is None:
        if type(a) is list:
            return translate(np.array(a))
        elif type(a) is np.ndarray and len(a.shape) == 1:
            t = np.identity(a.size + 1)
            t[-1, 0:-1] = a
            return t
        else: raise Exception("Unkonwn paramters passed", a)
    elif c is None:
        return translate(np.array([a, b], np.float32))
    else:
        return translate(np.array([a, b, c], np.float32))

def rot(a, b=None, c=None, d=None):
    """
    Usage:
    >>> rot(alpha) # rotate in 2D by angle alpha (res is Mat3)
    >>> rot(alpha, x, y, z) # rotate in 3D by alpha (res is Mat4)
    >>> rot(alpha, np.array([x, y, z])) # same as above
    >>> rot(np.array([alpha, x, y, z])) # same as above
    >>> rot(alpha, 'x') # rotate in 3D by alpha arroung [1,0,0] (or 'y', 'z')

    :return: the matrix
    """

    if b is None and c is None and d is None:
        if type(a) is float:
            s = np.sin(a)
            c = np.cos(a)
            return np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]], np.float32)
        elif type(a) is np.ndarray:
            if len(a) == 4:
                return rot(*a)
    elif c is None and d is None:
        if type(a) is float and type(b) is str:
            switch = {
                'x': lambda s, c: np.array([
                            [1, 0, 0, 0],
                            [0, c, -s, 0],
                            [0, s, c, 0],
                            [0, 0, 0, 1]
                        ], np.float32),
                'y': lambda s, c: np.array([
                            [c, 0, s, 0],
                            [0, 1, 0, 0],
                            [-s, 0, c, 0],
                            [0, 0, 0, 1]
                        ], np.float32),
                'z': lambda s, c: np.array([
                            [c, -s, 0, 0],
                            [s, c, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]
                        ], np.float32)
            }
            if b in switch:
                return switch[b](np.sin(a), np.cos(a))
            else: raise Exception("undefined controle caracter", b)
        elif (type(a) is float) and (type(b) is np.ndarray) and (len(b) == 3):
            return rot(a, b[0], b[1], b[2])
    else:
        r = np.sqrt(b**2 + c**2 + d**2)
        x, y, z = b/r, c/r, d/r
        a = -a
        co = np.cos(a)
        co1 = 1.0 - co
        si = np.sin(a)
        return np.array([
            [co + x**2 * co1, x*y * co1 - z * si, x*z * co1 + y * si, 0],
            [y*x * co1 + z * si, co + y**2 * co1, y*z * co1 - x * si, 0],
            [z*x * co1 - y * si, z*y * co1 + x * si, co + z**2 * co1, 0],
            [0, 0, 0, 1]
        ], np.float32)

def perspective(fov, near, far, aspect):
    """
    Creates e perspective transformation matrix
    :param fov: filed of view, a angle between 0 and pi/2
    :param near: near plain distance
    :param far: far plain distance (far > near)
    :param aspect: aspect ratio of screen
    :return: the perspective matrix (Mat4)
    """

    ymax = near * np.tan(fov / 2)
    xmax = ymax * aspect
    return frustume(-xmax, xmax, -ymax, ymax, near, far)

def frustume(left, right, bottom, top, near, far):
    a = 2*near
    dx = right - left
    dy = top - bottom
    dz = far - near
    return np.array([
        [a / dx, 0, 0, 0],
        [0, a / dy, 0, 0],
        [(right + left)/dx, (top + bottom)/dy, (-far - near)/dz, -1],
        [0, 0, -a*far / dz, 0]
    ], np.float32)

def lookAt(eye, center, up):
    def makeArray(x):
        if type(x) is list or type(x) is tuple: return np.array(x)
        else: return x

    eye = makeArray(eye)
    center = makeArray(center)
    up = makeArray(up)

    forward = eye - center
    forward /= np.linalg.norm(forward)

    side = np.cross(up, forward)
    side /= np.linalg.norm(side)

    up = np.cross(forward, side)
    up /= np.linalg.norm(up)

    m = np.identity(4, np.float32)
    m[0, 0:3] = side
    m[1, 0:3] = up
    m[2, 0:3] = forward

    t = np.identity(4, np.float32)
    t[0:3, 3] = -eye

    return np.dot(m, t).transpose()

def place(m):
    """
    places Mat3 in mat 4 appropriatly
    :param m: the Mat3
    :return: the Mat4
    """

    M = np.identity(4)
    M[0:2, 0:2] = m[0:2, 0:2]
    M[-1, 0:-2] = m[-1, 0:-1]
    return M

def dot(l):
    """
    Multiply a list of matrecies in order
    :param l: list of matricies
    :return: product
    """
    if len(l) == 1:
        return l[0]
    else:
        return np.dot(dot(l[:-1]), l[-1])
