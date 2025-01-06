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

def generate_arc_curve(resolution, points):
    """
    Generate points representing an arc of a circle passing through three points in 3D space.

    Parameters:
    p1: tuple of floats (x1, y1, z1) - First fixed point.
    p2: tuple of floats (x2, y2, z2) - Control point.
    p3: tuple of floats (x3, y3, z3) - Second fixed point.
    resolution: int - Number of points in the output arc.

    Returns:
    List of tuples representing points on the arc.
    """
    # Convert points to numpy arrays
    p1 = np.array(points[0])
    p2 = np.array(points[1])
    p3 = np.array(points[2])

    # Find the plane normal
    v1 = p2 - p1
    v2 = p3 - p1
    normal = np.cross(v1, v2)
    normal = normal / np.linalg.norm(normal)

    # Calculate the circle center and radius
    def find_circle_center(p1, p2, p3):
        mid1 = (p1 + p2) / 2
        mid2 = (p2 + p3) / 2

        normal1 = np.cross(p2 - p1, normal)
        normal2 = np.cross(p3 - p2, normal)

        # Set up linear equations to solve for center
        A = np.array([normal1, -normal2])
        b = np.array([np.dot(normal1, mid1), np.dot(normal2, mid2)])

        try:
            center = np.linalg.lstsq(A.T, b, rcond=None)[0]
        except np.linalg.LinAlgError:
            raise ValueError("The points do not define a unique circle.")
        return center

    center = find_circle_center(p1, p2, p3)
    radius = np.linalg.norm(p1 - center)

    # Generate points on the arc
    def angle_between(v1, v2):
        """Calculate the angle between two vectors."""
        v1_u = v1 / np.linalg.norm(v1)
        v2_u = v2 / np.linalg.norm(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    v_start = p1 - center
    v_end = p3 - center

    theta_start = 0
    theta_end = angle_between(v_start, v_end)

    # Determine direction of rotation
    if np.dot(np.cross(v_start, v_end), normal) < 0:
        theta_end = -theta_end

    theta = np.linspace(theta_start, theta_end, resolution)

    arc_points = []
    for t in theta:
        point = (center + np.cos(t) * v_start + np.sin(t) * np.cross(normal, v_start))
        arc_points.append(tuple(point))

    return arc_points


# Example usage
# interpolation_points = [
#     (0.0, 0.0, 0.0),
#     (1.0, 2.0, 0.0),
#     (4.0, 2.0, 0.0),
#     (7.0, 0.0, 0.0)
# ]
# resolution = 10
# curve = generate_catmull_rom_curve(resolution, interpolation_points)
# print(curve)
