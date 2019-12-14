import argparse
import typing
import unittest
from dataclasses import dataclass


PairGen = typing.Generator[typing.Tuple[int, int], None, None]


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Rectangle:
    top_left: Point
    bottom_right: Point

    def __post_init__(self):
        """
        Validate that 2 points are placed correctly.

        Rectangle is described by top-left and bottom-right points
        """
        err_msg = (f'Wrong rectange {self.top_left} x {self.bottom_right}'
                   f'You should provide 2 points - top-left and bottom-right')
        if self.top_left.x >= self.bottom_right.x:
            raise ValueError(err_msg)
        if self.top_left.y <= self.bottom_right.y:
            raise ValueError(err_msg)


def _split_2(l: typing.Iterable[int]) -> PairGen:
    """
    Small utility to split list by pairs.

    It does not verify the length of initial data.
    """
    it = iter(l)
    yield from zip(*[it, it])


def check_overlap(rect_a: Rectangle, rect_b: Rectangle) -> bool:
    """
    Check if 2 rectangles overlap

    The conditions when rectangles do not overlap are:

    1. One rectangle is on left side of left edge of other rectangle.
    2. One rectangle is above top edge of other rectangle.
    """
    if rect_a.top_left.x > rect_b.bottom_right.x:
        return False

    if rect_b.top_left.x > rect_a.bottom_right.x:
        return False

    if rect_a.bottom_right.y > rect_b.top_left.y:
        return False

    if rect_b.bottom_right.y > rect_a.top_left.y:
        return False

    return True


class OverlapTest(unittest.TestCase):
    """Unit test for overlapping rectangles"""

    def _check_both(self, rects: typing.List[Rectangle], is_true: bool = True):
        """
        Utility methof to verify that result does not depend
        on order of rectangles

        I.e. this is always valid::

            check_overlap(rect_a, rect_b) == check_overlap(rect_b, rect_a)
        """
        checker = self.assertTrue if is_true else self.assertFalse

        checker(check_overlap(*rects))
        checker(check_overlap(*rects[::-1]))

    def test_overlap_half(self):
        # Contain half of rectangle
        rects = [
            Rectangle(Point(0, 2), Point(2, 1)),
            Rectangle(Point(0, 3), Point(3, 0))
        ]
        self._check_both(rects)

    def test_overlap_corner(self):
        # Contain only one corner
        rects = [
            Rectangle(Point(0, 2), Point(2, 0)),
            Rectangle(Point(1, 3), Point(3, 1))
        ]
        self._check_both(rects)

    def test_overlap_contains(self):
        # One rectangle fully contains another
        rects = [
            Rectangle(Point(0, 10), Point(10, 0)),
            Rectangle(Point(1, 5), Point(5, 1))
        ]
        self._check_both(rects)

    def test_overlap_cross(self):
        # Corner is inside other rectangle, but do overlap
        rects = [
            Rectangle(Point(0, 4), Point(10, 2)),
            Rectangle(Point(2, 6), Point(8, 0))
        ]
        self._check_both(rects)

    def test_no_overlap_aside(self):
        # Rectangle aside of another
        rects = [
            Rectangle(Point(0, 2), Point(2, 0)),
            Rectangle(Point(3, 2), Point(5, 0))
        ]
        self._check_both(rects, False)

    def test_no_overlap_above(self):
        # Rectangle above another
        rects = [
            Rectangle(Point(0, 2), Point(2, 0)),
            Rectangle(Point(0, 5), Point(2, 3))
        ]
        self._check_both(rects, False)


def main():
    parser = argparse.ArgumentParser(
        description="Check if rectangles overlap"
    )
    parser.add_argument(
        'coords', nargs=8, type=int,
        help="4 points (X, Y) for 2 rectangles - "
             "top-left and bottom-right for each"
    )
    args = parser.parse_args()
    points = [Point(*c) for c in _split_2(args.coords)]
    rect_a, rect_b = [Rectangle(*p) for p in _split_2(points)]

    print(rect_a)
    print(rect_b)
    print('Overlap', check_overlap(rect_a, rect_b))


if __name__ == '__main__':
    main()
