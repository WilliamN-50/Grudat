# Domain coloring package

## Documentation (1.0.1)

### - Overview

Package Domain Coloring makes it possible to work with and visualize functions on the complex plane.

Domain coloring is a method to show the behaviour of a function.
Intricate patterns specific to the function can be observed and analyzed by mapping the outputs of a complex-valued function to different colors on the complex plane.

Compared to other ways of envisioning complex-valued functions, domain coloring is quite intuitive and simple.
Four dimensions are normally required to visualize a complex-valued function, however this can be reduced to two by representing two of the four dimensions as colors.
One natural way to determine the colors is by mapping the length and the phase angle of a complex number to different brightness and hues respectively.

### - Index

- **def** [func_grid](#func_grid)

- **def** [colors](#colors)

- **def** [domain_coloring](#domain)

- **def** [winding_num](#winding)

- **def** [zeros](#zeros)

- **def** [zoom_fit_zero](#zoom)

- **def** [branch_cut](#branch)

### - Constants

This section is empty.

### - Variables

This section is empty.

### - Functions

<a name="func_grid">**def** func_grid </a>

<pre><code><b>def</b> func_grid(func, re_range=(-10, 10), im_range=(-10, 10), step = 0.01)
</code></pre>

Create an equidistant array of function values on the complex plane bounded by im_range and re_range.
The distance between two neighboring points is given by step.
Inf values are set to 0.

- Input:

func - A complex valued function.

re_range  - A tuple containing the lower and upper bound (in order) for the real part of the array.

im_range  - A tuple containing the lower and upper bound (in order) for the imaginary part of the array.

step - The separation distance between two neighboring grid-points.

- Output:

Return an array containing the function evaluated at each grid-point.

____________________________________________________________________________________

<a name="colors">**def** colors </a>

<pre><code><b>def</b> colors(func_val)
</code></pre>

Return two arrays containing information about the colors for the given function values.

- Input:

func_val - An array containing the output of the function that is going to be visualized.

- Output:

Return an array with the hues and an array the with the values for hsv color representation.

____________________________________________________________________________________

<a name="domain">**def** domain_coloring </a>
<pre><code><b>def</b> domain_coloring(func_val, grid="ON")
</code></pre>

Visualizing the given function values on the complex plane using colors.

- Input:

func_val - An array containing the output of the function that is going to be visualized.

grid - "ON" or "OFF" for the grid

- Output:

None

____________________________________________________________________________________

<a name="winding">**def** winding_num </a>
<pre><code><b>def</b> winding_num(hue, rect)
</code></pre>

Find the winding number for a rectangle on the complex plane.
A positive winding number is given by this order of colors:

red -> orange -> yellow -> green -> turquoise -> blue -> indigo -> violet -> red.

This algorithm is going counterclockwise in the complex plane.

- Input:

hue - An array containing the hues for the complex function.

rect - Two tuples in a list representing two corners of a rectangle that is not adjacent to each other. The tuples should correspond to a point (col, row) in the given hue-array.

- Output:

Return an integer that is the winding number of the given rectangle.

____________________________________________________________________________________

<a name="zeros">**def** zeros </a>
<pre><code><b>def</b> zeros(hue, value, re_range, im_range, rect=None, tol=10**(-2))
</code></pre>

Find the roots of an analytic function within a given rectangle on the complex plane.
This algorithm uses the colors from the domain coloring and the winding number to find the zeros.
If there are more than one zero within the rectangle this algorithm might fail to find some of them.
Might also fail if the function has several values close to zero (but not equal to zero).
If no starting rectangle is given this algorithm will search for roots in the whole array.

- Input:

hue - An array containing the hues for the complex function.

value - An array containing the values of the hsv color representation of the function.

re_range  - A tuple containing the lower and upper bound (in order) for the real part.

im_range  - A tuple containing the lower and upper bound (in order) for the imaginary part.

rect - Two tuples in a list representing two corners of a rectangle that is not adjacent to each other. The tuples should correspond to a point (col, row) in the given hue- or value-array.

tol - Allowed error for the roots.

- Output:

Returns a list with the roots that the algorithm found and a list of their indices.

____________________________________________________________________________________

<a name="zoom">**def** zoom_fit_zero </a>
<pre><code><b>def</b> zoom_fit_zero(zero_index, value, re_range, im_range, step, light_val=0.95)
</code></pre>

Returning bounds for re_range, im_range, and step that gives a better view of the zeros.
Return current re_range, im_range and step if this algorithm cannot find a better view.

- Input:

zero_index - List containing indices of the zeros in the array

value - An array containing the values of the hsv color representation of the function.

re_range  - A tuple containing the current setting for lower and upper bound for the real part.

im_range  - A tuple containing the current setting for lower and upper bound for the imaginary part.

step - The current separation distance between two neighboring grid-points.

light_val - A float in the interval (0, 1) that guarantees a certain light for the output.

- Output:

Return step and two tuples containing re_range and im_range found with this algorithm to zoom into zeros.
____________________________________________________________________________________

<a name="branch">**def** branch_cut </a>
<pre><code><b>def</b> branch_cut(hue, value, re_range, im_range, step)
</code></pre>

Find if there is a branch cut or a branch point in the function using the colors.
Detects branches along the re- and im-axis.
Return False if the axis are out of range.
This algorithm might fail for graphs with not good enough resolution.

- Input:

hue - An array containing the hues for the complex function.

value - An array containing the values of the hsv color representation of the function.

re_range  - A tuple containing the lower and upper bound (in order) for the real part.

im_range  - A tuple containing the lower and upper bound (in order) for the imaginary part.

step - The separation distance between two neighboring grid-points.

- Output:

Return True if there is a branch cut or branch point, otherwise return False.
____________________________________________________________________________________

### - Types

This section is empty.

## Source files

[domain-coloring.py](https://gits-15.sys.kth.se/grudat21/wnguyen-ovn7/blob/master/domain_coloring.py)

## References

3Blue1Brown. [Video] Available at: [https://www.youtube.com/watch?v=b7FxPsqfkOY].

Wikipedia. 2021. Domain Coloring. [https://en.wikipedia.org/wiki/Domain_coloring].

James Schloss. Domain Coloring [https://www.algorithm-archive.org/contents/domain_coloring/domain_coloring.html].


____________________________________________________________________________________
