"""
Module defining a number of functions to quantify the overlap between shapes.
for instance rectangles representing detections by bounding-boxes.

"""
from functools import reduce


class Rectangle:
    """
    Construct a rectangle using the (r,c) coordinates for the top left corner,
    and either the coordinates of the botton right corner
    or the rectangle dimensions (height, width).

    Parameters
    ----------
    top_left : tuple of 2 ints
        (r,c)-coordinates for the top left corner of the rectangle.

    bottom_right : tuple of 2 ints, optional, default=None
        (r,c)-coordinates for the bottom right corner of the rectangle.

    dimensions : tuple of 2 ints, optional, default=None
        dimensions of the rectangle (height, width). The default is None.

    Raises
    ------
    ValueError
        If none or both of bottom_right and dimensions are provided.

    Returns
    -------
    Rectangle object.
    """

    def __init__(self, top_left, *, bottom_right=None, dimensions=None):
        self.top_left = top_left
        self._r = top_left[0]
        self._c = top_left[1]

        if (bottom_right is None) and (dimensions is None):
            raise ValueError("One of bottom_right or dimensions argument should be provided.")

        if (bottom_right is not None) and (dimensions is not None):
            raise ValueError("Either specify the bottom_right or dimensions, not both.")

        if bottom_right is not None:
            self.bottom_right = bottom_right

        elif dimensions is not None:
            self.bottom_right = tuple(
                    top + size - 1 for top, size in zip(top_left, dimensions)
                    )

    @property
    def height(self):
        # use negative indexing in anticipation of nD hyperrectangles.
        return self.bottom_right[-2] - self.top_left[-2] + 1

    @property
    def width(self):
        # use negative indexing in anticipation of nD hyperrectangles.
        return self.bottom_right[-1] - self.top_left[-1] + 1

    def __eq__(self, rectangle2):
        """Return true if 2 rectangles have the same position and dimension."""
        if not isinstance(rectangle2, Rectangle):
            return False

        if (self.top_left == rectangle2.top_left and
           self.bottom_right == rectangle2.bottom_right):
            return True

        return False

    def get_area(self):
        """Return the rectangle area in pixels."""
        return reduce(lambda a, b: a * b, self.get_dimensions())

    def get_dimensions(self):
        """Return the (height, width) dimensions in pixels."""
        return tuple(
                bottom - top + 1
                for top, bottom in zip(self.top_left, self.bottom_right)
                )



def is_intersecting(rectangle1, rectangle2):
    """
    Check if 2 rectangles are intersecting.

    Adapted from post from Aman Gupta
    at https://www.geeksforgeeks.org/find-two-rectangles-overlap/.

    Parameters
    ----------
    rectangle1 : a Rectangle object
        First rectangle.
    rectangle2 : a second Rectangle object
        Second rectangle

    Returns
    -------
    True if the rectangles are intersecting.
    """
    # If one rectangle is on left side of other
    if (rectangle1.top_left[1] >= rectangle2.bottom_right[1] or
       rectangle2.top_left[1] >= rectangle1.bottom_right[1]):
        return False

    # If one rectangle is above other
    if (rectangle1.top_left[0] >= rectangle2.bottom_right[0] or
       rectangle2.top_left[0] >= rectangle1.bottom_right[0]):
        return False

    return True

def intersection_rectangle(rectangle1, rectangle2):
    """
    Return a Rectangle corresponding to the intersection between 2 rectangles.

    Parameters
    ----------
    rectangle1 : a Rectangle object
        First rectangle.
    rectangle2 : a second Rectangle object
        Second rectangle

    Raises
    ------
    ValueError
        If the rectangles are not intersecting.
        Use is_intersecting to first test if the rectangles are intersecting.

    Returns
    -------
    Rectangle object representing the intersection.
    """
    if not is_intersecting(rectangle1, rectangle2):
        raise ValueError("""The rectangles are not intersecting.
                         Use is_intersecting to first test if the rectangles are intersecting.""")

    # determine the (r, c)-coordinates of the top left and bottom right corners
    # for the intersection rectangle
    r = max(rectangle1._r, rectangle2._r)
    c = max(rectangle1._c, rectangle2._c)
    bottom_right_r = min(rectangle1.bottom_right[0], rectangle2.bottom_right[0])
    bottom_right_c = min(rectangle1.bottom_right[1], rectangle2.bottom_right[1])

    return Rectangle((r, c), bottom_right=(bottom_right_r, bottom_right_c))


def intersection_area(rectangle1, rectangle2):
    """
    Return the intersection area between 2 rectangles.

    Parameters
    ----------
    rectangle1 : Rectangle
    rectangle2 : Rectangle

    Returns
    -------
    Intersection, float
        a float value corresponding to the intersection area.
    """
    if not is_intersecting(rectangle1, rectangle2):
        return 0

    # Compute area of the intersecting box
    return intersection_rectangle(rectangle1, rectangle2).get_area()


def union_area(rectangle1, rectangle2):
    """Compute the area for the rectangle corresponding to the union of 2 rectangles."""
    return (rectangle1.get_area()
            + rectangle2.get_area()
            - intersection_area(rectangle1, rectangle2))

def intersection_over_union(rectangle1, rectangle2):
    """
    Compute the ratio intersection aera over union area for a pair of rectangle.
    The intersection over union (IoU) ranges between 0 (no overlap) and 1 (full overlap).
    """
    return intersection_area(rectangle1, rectangle2) / union_area(rectangle1, rectangle2)
