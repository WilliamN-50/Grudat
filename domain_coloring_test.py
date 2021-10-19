# Unittest for domain_coloring
#
import numpy as np
from domain_coloring import *


# Test function 1
def func1(z):
    return z


# Test function 2
def func2(z):
    return z**2


# Test function 3
def func3(z):
    return z**3-1


# Test function 4
def func4(z):
    return np.log(z)


# Test function 5
def func5(z):
    return np.arctan(z)


# Testing the colors and function values
def test_domain_color():
    # Getting 3x3 array with function values evaluated at f(z) = z
    result = func_grid(func1, re_range=(-1, 1), im_range=(-1, 1), step=1)
    a = np.array([[-1+1j, 0+1j, 1+1j], [-1+0j, 0+0j, 1+0j], [-1-1j, 0-1j, 1-1j]])
    np.testing.assert_equal(result, a)

    # Getting color
    hue, value = colors(result)

    # hue is a color circle from (0, 1)
    h = np.array([[0.375, 0.25, 0.125], [0.5, 0., 0.], [0.625, 0.75, 0.875]])
    np.testing.assert_allclose(hue, h)

    # value only depends on the length of complex numbers and a special function f(z) = pi/2*arctan(abs(z))
    # values found using calculator
    v = np.array([[0.608173448, 0.5, 0.608173448], [0.5, 0., 0.5], [0.608173448, 0.5, 0.608173448]])
    np.testing.assert_allclose(value, v)


# Testing of winding number. Winding number gives a hint of how many roots there might be inside a path.
def test_winding():
    # Size of the arrays for this test is 201x201
    rect = [(0, 0), (200, 200)]
    re_range = (-10, 10)
    im_range = (-10, 10)
    step = 0.1

    # Test case 1: f(z) = z has one root at z=0 with multiplicity 1
    result = func_grid(func1, re_range=re_range, im_range=im_range, step=step)
    h, v = colors(result)
    winding = winding_num(h, rect)
    np.testing.assert_equal(winding, 1)

    # Test case 2: f(z) = z**2 has one root at z=0 with multiplicity 2
    result = func_grid(func2, re_range=re_range, im_range=im_range, step=step)
    h, v = colors(result)
    winding = winding_num(h, rect)
    np.testing.assert_equal(winding, 2)

    # Test case 3: f(z) = z**3 - 1 has a total of three roots at z=1, z=-1/2+j*sqrt(3/4) and z=-1/2-j*sqrt(3/4)
    result = func_grid(func3, re_range=re_range, im_range=im_range, step=step)
    h, v = colors(result)
    winding = winding_num(h, rect)
    np.testing.assert_equal(winding, 3)

    # Test case 4: f(z) = z**3 - 1 now only including z=1 in the path.
    rect = [(100, 0), (200, 200)]
    winding = winding_num(h, rect)
    np.testing.assert_equal(winding, 1)


# Testing zeros and zoom_fit_zero
def test_zero():
    # Size of the arrays for this test is 401x401.
    re_range = (-5, 5)
    im_range = (-5, 5)
    step = 0.025

    # Test case 1 for zeros: f(z) = z
    result = func_grid(func1, re_range=re_range, im_range=im_range, step=step)
    h, v = colors(result)
    root, index = zeros(h, v, re_range, im_range)
    np.testing.assert_allclose(root, [0+0j], atol=step)  # step is the absolute tolerance

    # Test case 1 for zoom_fit_zero:
    new_re_range, new_im_range, new_step = zoom_fit_zero(index, v, re_range, im_range, step, light_val=0.8)
    shrinking_x = new_re_range[0] > re_range[0] and new_re_range[1] < re_range[1]
    shrinking_y = new_im_range[0] > im_range[0] and new_im_range[1] < re_range[1]
    np.testing.assert_equal((shrinking_x and shrinking_y), True)

    # Since the location of the root for f(z) = z is symmetric with respect to chosen ranges
    # for this case the exact value of the sought light_val could be found:
    # Zero location at (200, 200)
    # Calculations:
    # index_light = 200 +- (new_range[i])/step for i =1, 2
    np.testing.assert_equal(v[324][200] > 0.8, True)
    np.testing.assert_equal(v[323][200] > 0.8, False)
    np.testing.assert_equal(v[200][76] > 0.8, True)
    np.testing.assert_equal(v[200][77] > 0.8, False)
    # There are four more cases for the two other directions, but they will give the same result due to symmetry.

    # Test case 2 for zeros: f(z) = z**3 - 1
    result = func_grid(func3, re_range=re_range, im_range=im_range, step=step)
    h, v = colors(result)
    root, index = zeros(h, v, re_range, im_range, tol=0.02)  # tol=0.02 is required to find all three of the zeros
    np.testing.assert_allclose(root, [(-0.5-np.sqrt(3/4)*1j), (1 + 0j), (-0.5+np.sqrt(3/4)*1j)], atol=step)

    # Test case 2 for zoom_fit_zero:
    new_re_range, new_im_range, new_step = zoom_fit_zero(index, v, re_range, im_range, step, light_val=0.8)
    shrinking_x = new_re_range[0] > re_range[0] and new_re_range[1] < re_range[1]
    shrinking_y = new_im_range[0] > im_range[0] and new_im_range[1] < re_range[1]
    np.testing.assert_equal((shrinking_x and shrinking_y), True)


# Testing for branches
def test_branch():
    # Size of the arrays for this test is 401x401.
    re_range = (-10, 10)
    im_range = (-10, 10)
    step = 0.05

    # Test case 1: f(z) = log(z)
    result = func_grid(func4, re_range=re_range, im_range=im_range, step=step)
    h, v = colors(result)
    branch = branch_cut(h, v, re_range, im_range, step)
    np.testing.assert_equal(branch, True)

    # Test case 2: f(z) = z
    result = func_grid(func1, re_range=re_range, im_range=im_range, step=step)
    h, v = colors(result)
    branch = branch_cut(h, v, re_range, im_range, step)
    np.testing.assert_equal(branch, False)

    # Test case 3: f(z) = log(z) Out of bound
    re_range = (1, 21)
    im_range = (1, 21)
    step = 0.05
    result = func_grid(func4, re_range=re_range, im_range=im_range, step=step)
    h, v = colors(result)
    branch = branch_cut(h, v, re_range, im_range, step)
    np.testing.assert_equal(branch, False)

    # Test case 4: f(z) = log(z) only negative x-axis
    re_range = (-21, -1)
    im_range = (-10, 10)
    step = 0.05
    result = func_grid(func4, re_range=re_range, im_range=im_range, step=step)
    h, v = colors(result)
    branch = branch_cut(h, v, re_range, im_range, step)
    np.testing.assert_equal(branch, True)

    # Test case 5: f(z) = arctan(z) only positive y_axis
    re_range = (-10, 10)
    im_range = (1, 21)
    step = 0.05
    result = func_grid(func5, re_range=re_range, im_range=im_range, step=step)
    h, v = colors(result)
    branch = branch_cut(h, v, re_range, im_range, step)
    np.testing.assert_equal(branch, True)


# Unittest
def main():
    test_domain_color()
    test_winding()
    test_zero()
    test_branch()


if __name__ == '__main__':
    main()
