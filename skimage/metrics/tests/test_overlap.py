from skimage.metrics.overlap import Rectangle
from skimage._shared import testing

height1, width1 = 2, 4
rectangle1 = Rectangle((0, 0), size=(height1, width1))  # bottom right in (1,3) thus

height2 = width2 = 3
rectangle2 = Rectangle((1, 3), size=(height2, width2))

rectangle3 = Rectangle((0, 0), bottom_right=(2, 2))

rectangle4 = Rectangle((10, 10), size=(5, 5))

rect_inter13 = Rectangle.intersection_rectangles(rectangle1, rectangle3)

union_area13 = Rectangle.union_area(rectangle1, rectangle3)


def test_area():
    assert rectangle1.get_area() == height1 * width1
    assert rectangle2.get_area() == height2 * width2
    assert rectangle3.get_area() == 3*3


def test_constructor_size():
    assert rectangle1.bottom_right == (1, 3)


def test_constructor_bottom_corner():
    assert rectangle3.get_size() == (3, 3)


def test_intersection():
    assert not Rectangle.is_intersecting(rectangle1, rectangle2)
    assert Rectangle.is_intersecting(rectangle1, rectangle3)


def test_eq_operator():# Intersection rectangle and == comparison
    assert rect_inter13 == Rectangle((0, 0), bottom_right=(1, 2))
    assert rect_inter13 != 5
    with testing.raises(ValueError):
        Rectangle.intersection_rectangles(rectangle1, rectangle2)


def test_union():
    assert union_area13 == (rectangle1.get_area() + rectangle3.get_area() - rect_inter13.get_area())


def test_IoU():
    assert Rectangle.intersection_over_union(rectangle1, rectangle3) == rect_inter13.get_area()/union_area13
