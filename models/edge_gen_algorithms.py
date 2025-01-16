import numpy as np

def generate_catmull_rom_curve(resolution, points):
    """
    Generate a Catmull-Rom spline curve.

    :param resolution: Number of points to interpolate between each segment.
    :param points: List of interpolation points [(x, y, z), ...]. Minimum 3 points.
    :return: List of points [(x, y, z), ...] representing the generated curve.
    """
    if len(points) < 3:
        raise ValueError("At least 3 points are required for Catmull-Rom interpolation.")

    def catmull_rom_point(p0, p1, p2, p3, t):
        """
        Compute a point on the Catmull-Rom spline.

        :param p0: Control point 0.
        :param p1: Control point 1 (start of the segment).
        :param p2: Control point 2 (end of the segment).
        :param p3: Control point 3.
        :param t: Parameter t in [0, 1].
        :return: Interpolated point (x, y, z).
        """
        t2 = t * t
        t3 = t2 * t

        # Basis matrix coefficients
        c0 = -0.5 * t3 + t2 - 0.5 * t
        c1 =  1.5 * t3 - 2.5 * t2 + 1.0
        c2 = -1.5 * t3 + 2.0 * t2 + 0.5 * t
        c3 =  0.5 * t3 - 0.5 * t2

        # Compute interpolated point
        x = c0 * p0[0] + c1 * p1[0] + c2 * p2[0] + c3 * p3[0]
        y = c0 * p0[1] + c1 * p1[1] + c2 * p2[1] + c3 * p3[1]
        z = c0 * p0[2] + c1 * p1[2] + c2 * p2[2] + c3 * p3[2]

        return (x, y, z)

    # List to store the generated curve points
    curve_points = []

    # Iterate over segments defined by points
    for i in range(len(points) - 1):
        # Define control points
        p0 = points[i - 1] if i > 0 else points[i]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else points[i + 1]

        # Generate points for the segment
        for j in range(resolution):
            t = j / resolution
            curve_points.append(catmull_rom_point(p0, p1, p2, p3, t))

    # Add the last point
    curve_points.append(points[-1])

    return curve_points

def generate_arc_curve_og(resolution, points):
    
    if len(points) != 3:
        raise ValueError("Exactly 3 points are required for Arc interpolation.")

    print(f"points ----------> {points}")
    A = np.array(points[0]) # end point
    B = np.array(points[1]) # handler point
    C = np.array(points[2]) # end point

    def mod(v):
        return np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

    u1 = (B-A)

    u = u1/mod(u1)

    w1 = np.cross(C-A, u1)

    w = w1/mod(w1)

    v = np.cross(w,u)

    b = (np.dot(B-A, u), 0)

    c = (np.dot(C-A, u), np.dot(C-A, v))

    h = ( (c[0] - b[0]/2)**2 + c[1]**2 - (b[0]/2)**2 ) / ( 2 * c[1] )

    Cn = A + ((b[0]/2) * u ) + (h * v) # center of the circle

    r = mod(Cn - A) # Radius of the circle

    axis = np.cross((B-A)/mod(B-A), (C-A)/mod(C-A))
    a = u
    b = np.cross(axis, a)

    def arc_point(t, c, a, b, r):
        return (
            c[0] + r*np.cos(t)*a[0] + r*np.sin(t)*b[0],
            c[1] + r*np.cos(t)*a[1] + r*np.sin(t)*b[1],
            c[2] + r*np.cos(t)*a[2] + r*np.sin(t)*b[2]
        )
    
    def get_arc_param(p, c, a, b, r):
        k = (p[0] - c[0]) / r
        R = np.sqrt(a[0]**2 + b[0]**2)
        phi = np.arctan2(b[0], a[0])
        t = np.arcsin(k / R) - phi

        return t
    
    t1 = get_arc_param(A, Cn, a, b, r)
    t2 = get_arc_param(C, Cn, a, b, r)

    e2 = 0
    e1 = 0
    if t2>t1:
        e2 = t2
        e1 = t1
    else:
        e2 = t1
        e1 = t2

    d = (e2 - e1) / resolution

    curve_points = []
    i = e1
    while i <= e2:
        curve_points.append(arc_point(i, Cn, a, b, r))
        i += d
    
    print("Completed ARC Generation")
    print(f"curve_points ----------> {curve_points}")
    
    return curve_points

def generate_arc_curve(resolution, points):
    if len(points) != 3:
        raise ValueError("Exactly 3 points are required for Arc interpolation.")

    # Extract points
    A = np.array(points[0])  # Start point
    B = np.array(points[1])  # Control point
    C = np.array(points[2])  # End point

    def normalize(v):
        return v / np.linalg.norm(v)

    # Basis vectors
    u = normalize(B - A)
    w = normalize(np.cross(C - A, B - A))
    v = np.cross(w, u)

    # Calculate intermediate parameters
    b_u = np.dot(B - A, u)
    c_u = np.dot(C - A, u)
    c_v = np.dot(C - A, v)

    # Compute circle center and radius
    h = ((c_u - b_u / 2) ** 2 + c_v ** 2 - (b_u / 2) ** 2) / (2 * c_v)
    Cn = A + (b_u / 2) * u + h * v
    r = np.linalg.norm(Cn - A)

    # Calculate angle parameters for the arc
    def get_arc_param(p):
        dp = p - Cn
        return np.arctan2(np.dot(dp, v), np.dot(dp, u))

    t1 = get_arc_param(A)
    t2 = get_arc_param(C)

    # Ensure angles are ordered correctly
    if t2 < t1:
        t1, t2 = t2, t1

    # Generate arc points
    t_values = np.linspace(t1, t2, resolution)
    curve_points = [
        (Cn + r * np.cos(t) * u + r * np.sin(t) * v).tolist()
        for t in t_values
    ]

    return curve_points

def generate_bspline_curve(resolution, verts):
    """
    Generate a B-spline curve from given control points.

    Parameters:
        resolution (int): Number of points to generate on the B-spline curve.
        verts (list of list/tuple): Control points (at least 3 points).
            verts[0] and verts[-1] are endpoints, and verts[1:-1] are control points.

    Returns:
        list: List of points forming the B-spline curve.
    """
    if len(verts) < 3:
        raise ValueError("At least 3 control points are required to generate a B-spline.")

    # Define the B-spline basis matrix
    basis_matrix = np.array([
        [-1,  3, -3,  1],
        [ 3, -6,  3,  0],
        [-3,  0,  3,  0],
        [ 1,  4,  1,  0]
    ]) / 6.0

    # Ensure verts is a numpy array
    verts = np.array(verts)

    # Add extra points at the start and end to handle endpoints properly
    extended_verts = np.vstack([verts[0], verts, verts[-1]])

    # Initialize result list
    bspline_points = [verts[0]]

    # Iterate through the segments formed by control points
    for i in range(len(extended_verts) - 3):
        # Extract 4 control points for the current segment
        P = extended_verts[i:i+4]

        # Generate points for the current segment
        for j in range(resolution):
            t = j / (resolution - 1)  # Parameter t in [0, 1]
            T = np.array([t**3, t**2, t, 1])
            point = T @ basis_matrix @ P
            bspline_points.append(point)

    bspline_points.append(verts[-1])
    return bspline_points
