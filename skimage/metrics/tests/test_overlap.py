from skimage.metrics.overlap import (
        BoundingBox,
        intersect,
        overlap,
        intersection_over_union,
        )
from skimage._shared import testing

height1, width1 = 2, 4
r1 = BoundingBox((0, 0), dimensions=(height1, width1))

height2 = width2 = 3
r2 = BoundingBox((2, 3), dimensions=(height2, width2))  # share part of top side with r1

r3 = BoundingBox((0, 0), bottom_right=(2, 3))  # included in r1, intersect with r2 in (2,3)

rect_inter13 = overlap(r1, r3)


def test_area():
    assert r1.area == height1 * width1
    assert r2.area == height2 * width2
    assert r3.area == 2 * 3


def test_constructor_dimensions():
    assert tuple(r1.top_left) == (0, 0)
    assert tuple(r1.bottom_right) == (height1, width1)
    with testing.raises(ValueError):
        BoundingBox((0, 0), dimensions=(-5, 5))


def test_constructor_bottom_corner():
    assert tuple(r3.top_left) == (0, 0)
    assert tuple(r3.dimensions) == (2, 3)
    with testing.raises(ValueError):
        BoundingBox((2, 2), bottom_right=(0, 0))


def test_intersection():
    assert intersect(r1, r2)
    assert intersect(r1, r3)


def test_overlap():
    assert not overlap(r1, r2)   # border intersection only
    assert not overlap(r2, r3)   # corner intersection only
    # test when included see test_eq_operator


def test_full_overlap():
    assert overlap(r1, r1) == r1
    assert intersection_over_union(r1, r1) == 1


def test_eq_operator():  # Intersection rectangle and == comparison
    assert rect_inter13 == r3


def test_eq_other_obj():
    with testing.raises(TypeError):
        _ = r2 == (1, 2, 3, 4)


def test_str():
    assert str(r3) == 'BoundingBox((0, 0), bottom_right=(2, 3))'


def test_IoU():
    union_area13 = r1.area + r3.area - rect_inter13.area
    assert intersection_over_union(r1, r3) == rect_inter13.area / union_area13
