# Package Domain Coloring makes it possible to work with and
# visualize functions on the complex plane.
#
# Domain coloring is a method to show the behaviour of a function.
# Intricate patterns specific to the function can be observed and analyzed
# by mapping the outputs of a complex-valued function to different colors
# on the complex plane.
#
# Compared to other ways of envisioning complex-valued functions,
# domain coloring is quite intuitive and simple.
# Four dimensions are normally required to visualize a complex-valued function,
# however this can be reduced to two by representing two of the four dimensions as colors.
# One natural way to determine the colors is by mapping the length
# and the phase angle of a complex number to different brightness and hues respectively.
#
import matplotlib.pyplot as plt
import matplotlib.colors as cl
import numpy as np


def func_grid(func, re_range=(-10, 10), im_range=(-10, 10), step=0.01):
    """
    Create an equidistant array of function values on the complex plane
    bounded by im_range and re_range. The distance between two neighboring points is given by step.
    Inf values are set to 0.
    ______________________________________________________________________
    Input:
    func - A complex valued function.
    re_range  - A tuple containing the lower and upper bound (in order) for the real part of the array.
    im_range  - A tuple containing the lower and upper bound (in order) for the imaginary part of the array.
    step - The separation distance between two neighboring grid-points.
    Output:
    Return an array containing the function evaluated at each grid-point.
    ______________________________________________________________________
    """
    re_points = np.arange(re_range[0], re_range[1] + step, step)
    im_points = np.arange(im_range[1], im_range[0] - step, -step)
    result = func(re_points[np.newaxis, :] + im_points[:, np.newaxis] * 1j)
    result[np.real(result) == np.inf] = 0
    return result


def colors(func_val):
    """
    Return two arrays containing information about the colors for the given function values.
    __________________________________________________________________
    Input:
    func_val - An array containing the output of the function that is going to be visualized.
    Output:
    Return an array with the hues and an array the with the values for hsv color representation.
    __________________________________________________________________
    """
    angles = np.angle(func_val)
    hue = (angles + 2 * np.pi) % (2 * np.pi) / (2*np.pi)  # Changing from [-pi, pi] to [0, 1]
    value = 2/np.pi * np.arctan(np.absolute(func_val))
    return hue, value


def _grid_lines(func_val, grid):
    """Create grid-lines for the plot."""
    if grid == "ON":
        line_width = 0.15
    else:
        line_width = 0
    s = np.absolute(np.sin(np.pi/2*np.real(func_val)))**line_width\
        * np.absolute(np.sin(np.pi/2*np.imag(func_val)))**line_width
    return s


def domain_coloring(func_val, grid="ON"):
    """
    Visualizing the given function values on the complex plane using colors.
    ___________________________________________________________________________
    Input:
    func_val - An array containing the output of the function that is going to be visualized.
    grid - "ON" or "OFF" for the grid.
    Output:
    None
    ___________________________________________________________________________
    """
    hue, value = colors(func_val)
    s = _grid_lines(func_val, grid)
    hsv = np.zeros(func_val.shape + (3,))
    hsv[..., 0] = hue
    hsv[..., 1] = s
    hsv[..., 2] = value
    rgb = cl.hsv_to_rgb(hsv)
    plt.imshow(rgb)
    plt.axis("off")
    plt.show()


def _winding_path(val1, val2):
    """Calculate the winding difference between val1 and val2.
    Checking so that the values changes correctly."""
    # val1 = color[y2][i+1], color[y1][i], color[j][x2], color[j+1][x1]
    # val2 = color[y2][i], color[y1][i+1], color[j+1][x2], color[j][x1]
    winding = 0
    lim1 = 0.7  # Make sure the leap from the last color to the first color is done by element > lim1 and < lim2.
    lim2 = 0.3
    if val2 > lim1:
        if val1 < lim2:
            winding += 1 + val1 - val2
        else:
            winding += val1 - val2
    elif val2 < lim2:
        if val1 > lim1:
            winding += - 1 + val1 - val2
        else:
            winding += val1 - val2
    else:
        winding += val1 - val2
    return winding


def winding_num(hue, rect):
    """
    Find the winding number for a rectangle on the complex plane.
    A positive winding number is given by this order of colors:
    red -> orange -> yellow -> green -> turquoise -> blue -> indigo -> violet -> red.
    This algorithm is going counterclockwise in the complex plane.
    _________________________________________________________________
    Input:
    hue - An array containing the hues for the complex function.
    rect - Two tuples in a list representing two corners of a rectangle that is not adjacent to each other.
    The tuples should correspond to a point (col, row) in the given hue-array.
    Output:
    Return an integer that is the winding number of the given rectangle.
    _________________________________________________________________
    """
    x1, y1 = rect[0]
    x2, y2 = rect[1]
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    winding = 0
    for i in range(x1, x2):
        winding += _winding_path(hue[y2][i+1], hue[y2][i])
        winding += _winding_path(hue[y1][i], hue[y1][i+1])
    for j in range(y1, y2):
        winding += _winding_path(hue[j][x2], hue[j+1][x2])
        winding += _winding_path(hue[j+1][x1], hue[j][x1])
    return int(round(winding))


def _calc_zeros(hue, value, rect, zero_index, tol):
    """Calculate the zeros recursively using smaller rectangles."""
    x1, y1 = rect[0]
    x2, y2 = rect[1]

    # Base Case 3x3 matrix since this algorithm needs to be able to traverse around the root and find colors
    if y2 - y1 <= 3 and x2 - x1 <= 3:
        for i in range(x1, x2):
            for j in range(y1, y2):
                if value[j][i] < tol:
                    zero_index.add((i, j))
        return
    # Stop searching in rectangle and check the edges for zeros.
    # Winding number == 0 means that there are no more zeros in the rectangle that this algorithm can find.
    if winding_num(hue, rect) == 0:
        for i in range(x1, x2):
            if value[y1][i] < tol:
                zero_index.add((i, y1))
            if value[y2][i] < tol:
                zero_index.add((i, y2))
        for j in range(y1, y2):
            if value[j][x1] < tol:
                zero_index.add((x1, j))
            if value[j][x2] < tol:
                zero_index.add((x2, j))
    else:
        # Recursion with smaller rectangles
        if y2 - y1 < x2 - x1:
            _calc_zeros(hue, value, [(x1, y1), (int(np.ceil((x2 + x1) / 2)), y2)], zero_index, tol)
            _calc_zeros(hue, value, [(int(np.ceil((x2 + x1) / 2)), y1), (x2, y2)], zero_index, tol)
        else:
            _calc_zeros(hue, value, [(x1, y1), (x2, int(np.ceil((y2 + y1) / 2)))], zero_index, tol)
            _calc_zeros(hue, value, [(x1, int(np.ceil((y1 + y2) / 2))), (x2, y2)], zero_index, tol)
    return


def zeros(hue, value, re_range, im_range, rect=None, tol=10**(-2)):
    """
    Find the roots of an analytic function within a given rectangle on the complex plane.
    This algorithm uses the colors from the domain coloring and the winding number to find the zeros.
    If there are more than one zero within the rectangle this algorithm might fail to find some of them.
    Might also fail if the function has many values close to zero (but not equal to zero).
    If no starting rectangle is given this algorithm will search for roots in the whole array.
    ______________________________________________________________________________________________
    Input:
    hue - An array containing the hues for the complex function.
    value - An array containing the values of the hsv color representation of the function.
    re_range  - A tuple containing the lower and upper bound (in order) for the real part.
    im_range  - A tuple containing the lower and upper bound (in order) for the imaginary part.
    rect - Two tuples in a list representing two corners of a rectangle that is not adjacent to each other.
    The tuples should correspond to a point (col, row) in the given hue- or value-array.
    tol - Allowed error for the roots.
    Output:
    Returns a list with the roots that the algorithm found and a list of their indices.
    ______________________________________________________________________________________________
    """
    # row = y, col = x
    row, col = hue.shape

    # Starting rectangle
    if rect is None:
        rect = [(0, 0), (col-1, row-1)]
    else:
        x1, y1 = rect[0]
        x2, y2 = rect[1]
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        rect = [(x1, y1), (x2, y2)]

    # Find the indices where the roots are
    zero_index = set()
    zero_list = []
    _calc_zeros(hue, value, rect, zero_index, tol)

    # Find corresponding complex root
    step = (re_range[1] - re_range[0])/(row-1)  # Off by one in row
    for index in zero_index:
        col, row = index
        re = re_range[0] + col*step
        im = im_range[0] + row*step
        zero_list.append(re + im*1j)

    return zero_list, list(zero_index)


def _brightness(value, x, y, light_val, x_val=True, max_val=True):
    """Find the needed difference from the root to achieve the sought light_val.
    Return zero if not possible to find the difference."""
    diff = 0
    light = 0
    try:
        while light < light_val:
            light = value[y][x]
            if max_val:
                if x_val:
                    x += 1
                else:
                    y += 1
            else:
                if x_val:
                    x -= 1
                else:
                    y -= 1
            diff += 1
            if x < 0 or y < 0:
                raise IndexError
    except IndexError:
        return None
    return diff


def zoom_fit_zero(zero_index, value, re_range, im_range, step, light_val=0.95):
    """
    Returning bounds for re_range, im_range, and step that gives a better view of the zeros.
    Return current re_range, im_range and step if this algorithm cannot find a better view.
    ___________________________________________________________________________________________
    Input:
    zero_index - List containing indices of the zeros in the array
    value - An array containing the values of the hsv color representation of the function.
    re_range  - A tuple containing the current setting for lower and upper bound for the real part.
    im_range  - A tuple containing the current setting for lower and upper bound for the imaginary part.
    step - The current separation distance between two neighboring grid-points.
    light_val - A float in the interval (0, 1) that guarantees a certain light for the output.
    Output:
    Return step and two tuples containing re_range and im_range found with this algorithm to zoom into zeros.
    ___________________________________________________________________________________________
    """

    if not zero_index:
        return re_range, im_range, step

    x_max = zero_index[0][0]
    x_min = zero_index[0][0]
    y_max = zero_index[0][1]
    y_min = zero_index[0][1]

    for y, x in zero_index[1:]:
        if x > x_max:
            x_max = x
        elif x < x_min:
            x_min = x
        if y > y_max:
            y_max = y
        elif y < y_min:
            y_min = y
    # Find how much each value needs to change
    diff_x_min = _brightness(value, x_min, y_min, light_val, max_val=False, x_val=True)
    diff_y_min = _brightness(value, x_max, y_min, light_val, max_val=False, x_val=False)
    diff_x_max = _brightness(value, x_max, y_max, light_val, max_val=True, x_val=True)
    diff_y_max = _brightness(value, x_min, y_max, light_val, max_val=True, x_val=False)
    if diff_x_min is None or diff_x_max is None or diff_y_min is None or diff_y_max is None:
        return re_range, im_range, step

    num_re_step = (re_range[1] - re_range[0])/step  # Total number of elements in a row
    row, col = value.shape
    lower_bound_re = re_range[0] + (x_min - diff_x_min + 1) * step  # Off by one that is already in col and row
    upper_bound_re = re_range[1] - (col - x_max - diff_x_max) * step
    lower_bound_im = im_range[0] + (y_min - diff_y_min + 1) * step
    upper_bound_im = im_range[1] - (row - y_max - diff_y_max) * step
    new_re_range = (lower_bound_re, upper_bound_re)
    new_im_range = (lower_bound_im, upper_bound_im)
    new_step = (upper_bound_re - lower_bound_re)/num_re_step

    return new_re_range, new_im_range, new_step


def branch_cut(hue, value, re_range, im_range, step):
    """"
    Find if there is a branch cut or a branch point in the function using the colors.
    Detects branches along the re- and im-axis.
    Return False if the axis are out of range. It might fail for graphs with not good enough resolution.
    _____________________________________________________________________
    Input:
    hue - An array containing the hues for the complex function.
    value - An array containing the values of the hsv color representation of the function.
    re_range  - A tuple containing the lower and upper bound (in order) for the real part.
    im_range  - A tuple containing the lower and upper bound (in order) for the imaginary part.
    step - The separation distance between two neighboring grid-points.
    Output:
    Return True if there is a branch cut or branch point, otherwise return False.
    _____________________________________________________________________
    """
    row, col = hue.shape
    re_axis_in = im_range[0] < 0 < im_range[1]
    im_axis_in = re_range[0] < 0 < re_range[1]
    branch_lim = 0.4  # A good lower bound for changes. Found by going through common functions with branch-cut.
    deviation = 2  # Deviation from the axis
    lim1 = 0.9  # Make sure the leap from the last color to the first color is done by element > lim1 and < lim2.
    lim2 = 0.1
    tol = 0.2  # Tolerance to avoid zeros.

    if not(re_axis_in or im_axis_in):
        return False
    if re_axis_in:
        # Finding where the re-axis is.
        y_zero1 = int(np.ceil(np.abs(im_range[0])/step)-deviation)
        y_zero2 = int(np.ceil(np.abs(im_range[0])/step)+deviation)
        for i in range(col):
            first_con = hue[y_zero1][i] > lim1 and hue[y_zero2][i] < lim2
            second_con = hue[y_zero2][i] > lim1 and hue[y_zero1][i] < lim2
            if not (first_con or second_con):
                if value[y_zero1][i] > tol and value[y_zero2][i] > tol:
                    if np.abs(hue[y_zero1][i] - hue[y_zero2][i]) > branch_lim:
                        return True
    if im_axis_in:
        # Finding where the im-axis is.
        x_zero1 = int(np.ceil(np.abs(re_range[0]) / step)-deviation)
        x_zero2 = int(np.ceil(np.abs(re_range[0]) / step)+deviation)
        for j in range(row):
            first_con = hue[j][x_zero1] > lim1 and hue[j][x_zero2] < lim2
            second_con = hue[j][x_zero2] > lim1 and hue[j][x_zero1] < lim2
            if not (first_con or second_con):
                if value[j][x_zero1] > tol and value[j][x_zero2] > tol:
                    if np.abs(hue[j][x_zero1] - hue[j][x_zero2]) > branch_lim:
                        return True
    return False


# Example of usage
def main():
    re_range = (-10, 10)
    im_range = (-10, 10)
    step = 0.01
    max_elem = int(np.floor((re_range[1] - re_range[0])/step))

    # Creating arrays for color
    func = lambda z: z**3 - 1
    result = func_grid(func, re_range=re_range, im_range=im_range, step=step)
    hue, value = colors(result)

    # Winding number
    winding = winding_num(hue, [(0, 0), (max_elem, max_elem)])
    print("This function has a winding number of:", str(winding))
    
    # Branch cuts
    branch = branch_cut(hue, value, re_range, im_range, step)
    if branch:
        print("This function has a branch cut or branch point.")

    # Zeros
    root, index = zeros(hue, value, re_range, im_range, tol=9*10**(-3))
    re_range, im_range, step = zoom_fit_zero(index, value, re_range, im_range, step, light_val=0.99)
    result2 = func_grid(func, re_range=re_range, im_range=im_range, step=step)

    # Domain coloring
    domain_coloring(result2)


if __name__ == '__main__':
    main()
