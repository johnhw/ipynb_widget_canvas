
from __future__ import division, print_function, unicode_literals

import unittest
import numpy as np

import transform_2D
import decompose

"""
Kinds of tests:
    self.assertTrue(value)
    self.assertFalse(value)

    self.assertGreater(first, second, msg=None)
    self.assertGreaterEqual(first, second, msg=None)
    self.assertLess(first, second, msg=None)
    self.assertLessEqual(first, second, msg=None)

    self.assertAlmostEqual(first, second, places=7, msg=None, delta=None)
    self.assertNotAlmostEqual(first, second, places=7, msg=None, delta=None)

    self.assertItemsEqual(actual, expected, msg=None)
    self.assertSequenceEqual(seq1, seq2, msg=None, seq_type=None)
    self.assertListEqual(list1, list2, msg=None)
    self.assertTupleEqual(tuple1, tuple2, msg=None)
    self.assertSetEqual(set1, set2, msg=None)
    self.assertDictEqual(expected, actual, msg=None)

    self.assertRaises(Exception, some_func, arg, arg_nother)

    np.testing.assert_equal(A, B)
    np.testing.assert_allclose(actual, desired, rtol=1e-07, atol=0, err_msg='', verbose=True)
"""

#################################################


class Test_Decompose(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_decompose_translate_A1(self):
        s = 0.1, 10.0
        H = transform_2D.offset(s)

        as_transforms = False
        values = decompose.decompose(H, as_transforms=as_transforms)

        # H_translate, H_scale, H_shear, H_rotate, H_perspective = values
        offset, persp, scale, shear, angle = values

        np.testing.assert_almost_equal(offset, s)
        np.testing.assert_almost_equal(scale, [1, 1])
        np.testing.assert_almost_equal(shear, 0)
        np.testing.assert_almost_equal(angle, 0)
        np.testing.assert_almost_equal(persp, [0, 0])

    def test_decompose_translate_A2(self):
        s = 0.1, 10.0
        H = transform_2D.offset(s)

        as_transforms = True
        values = decompose.decompose(H, as_transforms=as_transforms)

        H_translate, H_scale, H_shear, H_rotate, H_perspective = values
        # offset, persp, scale, shear, angle = values

        I = transform_2D.identity()

        np.testing.assert_almost_equal(H_translate, H)
        np.testing.assert_almost_equal(H_scale, I)
        np.testing.assert_almost_equal(H_shear, I)
        np.testing.assert_almost_equal(H_rotate, I)
        np.testing.assert_almost_equal(H_perspective, I)

    def test_decompose_scale_A1(self):
        s = 0.5
        H = transform_2D.scale(s)

        as_transforms = False
        values = decompose.decompose(H, as_transforms=as_transforms)

        # H_translate, H_scale, H_shear, H_rotate, H_perspective = values
        offset, persp, scale, shear, angle = values

        np.testing.assert_almost_equal(scale, (s, s))
        np.testing.assert_almost_equal(shear, 0)
        np.testing.assert_almost_equal(angle, 0)
        np.testing.assert_almost_equal(offset, [0, 0])
        np.testing.assert_almost_equal(persp, [0, 0])

    def test_decompose_scale_A2(self):
        s = 0.5
        H = transform_2D.scale(s)

        as_transforms = True
        values = decompose.decompose(H, as_transforms=as_transforms)

        H_translate, H_scale, H_shear, H_rotate, H_perspective = values
        # offset, persp, scale, shear, angle = values

        I = transform_2D.identity()

        np.testing.assert_almost_equal(H_translate, I)
        np.testing.assert_almost_equal(H_scale, H)
        np.testing.assert_almost_equal(H_shear, I)
        np.testing.assert_almost_equal(H_rotate, I)
        np.testing.assert_almost_equal(H_perspective, I)

    def test_decompose_scale_B1(self):
        s = 0.5, 0.1
        H = transform_2D.scale(s)

        as_transforms = False
        values = decompose.decompose(H, as_transforms=as_transforms)

        # H_translate, H_scale, H_shear, H_rotate, H_perspective = values
        offset, persp, scale, shear, angle = values

        np.testing.assert_almost_equal(scale, s)
        np.testing.assert_almost_equal(shear, 0)
        np.testing.assert_almost_equal(angle, 0)
        np.testing.assert_almost_equal(offset, [0, 0])
        np.testing.assert_almost_equal(persp, [0, 0])

    def test_decompose_scale_B2(self):
        s = 0.5, 0.1
        H = transform_2D.scale(s)

        as_transforms = True
        values = decompose.decompose(H, as_transforms=as_transforms)

        H_translate, H_scale, H_shear, H_rotate, H_perspective = values
        # offset, persp, scale, shear, angle = values

        I = transform_2D.identity()

        np.testing.assert_almost_equal(H_translate, I)
        np.testing.assert_almost_equal(H_scale, H)
        np.testing.assert_almost_equal(H_shear, I)
        np.testing.assert_almost_equal(H_rotate, I)
        np.testing.assert_almost_equal(H_perspective, I)

    def test_decompose_shear_A1(self):
        s = 0.55
        H = transform_2D.shear(s)

        as_transforms = False
        values = decompose.decompose(H, as_transforms=as_transforms)

        # H_translate, H_scale, H_shear, H_rotate, H_perspective = values
        offset, persp, scale, shear, angle = values

        np.testing.assert_almost_equal(offset, [0, 0])
        np.testing.assert_almost_equal(scale, [1, 1])
        np.testing.assert_almost_equal(shear, s)
        np.testing.assert_almost_equal(angle, 0)
        np.testing.assert_almost_equal(persp, [0, 0])

    def test_decompose_shear_A2(self):
        s = 0.55
        H = transform_2D.shear(s)

        as_transforms = True
        values = decompose.decompose(H, as_transforms=as_transforms)

        H_translate, H_scale, H_shear, H_rotate, H_perspective = values
        # offset, persp, scale, shear, angle = values

        I = transform_2D.identity()

        np.testing.assert_almost_equal(H_translate, I)
        np.testing.assert_almost_equal(H_scale, I)
        np.testing.assert_almost_equal(H_shear, H)
        np.testing.assert_almost_equal(H_rotate, I)
        np.testing.assert_almost_equal(H_perspective, I)

    def test_decompose_rotate_A1(self):
        s = np.pi*0.2
        H = transform_2D.rotate(s)

        as_transforms = False
        values = decompose.decompose(H, as_transforms=as_transforms)

        # H_translate, H_scale, H_shear, H_rotate, H_perspective = values
        offset, persp, scale, shear, angle = values

        np.testing.assert_almost_equal(offset, [0, 0])
        np.testing.assert_almost_equal(scale, [1, 1])
        np.testing.assert_almost_equal(shear, 0)
        np.testing.assert_almost_equal(angle, s)
        np.testing.assert_almost_equal(persp, [0, 0])

    def test_decompose_rotate_A2(self):
        s = np.pi*0.2
        H = transform_2D.rotate(s)

        as_transforms = True
        values = decompose.decompose(H, as_transforms=as_transforms)

        H_translate, H_scale, H_shear, H_rotate, H_perspective = values
        # offset, persp, scale, shear, angle = values

        I = transform_2D.identity()

        np.testing.assert_almost_equal(H_translate, I)
        np.testing.assert_almost_equal(H_scale, I)
        np.testing.assert_almost_equal(H_shear, I)
        np.testing.assert_almost_equal(H_rotate, H)
        np.testing.assert_almost_equal(H_perspective, I)

    def test_decompose_perspective_A1(self):
        s = 0.1, 0.2
        H = transform_2D.perspective(s)

        as_transforms = False
        values = decompose.decompose(H, as_transforms=as_transforms)

        # H_translate, H_scale, H_shear, H_rotate, H_perspective = values
        offset, persp, scale, shear, angle = values

        np.testing.assert_almost_equal(offset, [0, 0])
        np.testing.assert_almost_equal(scale, [1, 1])
        np.testing.assert_almost_equal(shear, 0)
        np.testing.assert_almost_equal(angle, 0)
        np.testing.assert_almost_equal(persp, s)

    def test_decompose_perspective_A2(self):
        s = 0.1, 0.2
        H = transform_2D.perspective(s)

        as_transforms = True
        values = decompose.decompose(H, as_transforms=as_transforms)

        H_translate, H_scale, H_shear, H_rotate, H_perspective = values
        # offset, persp, scale, shear, angle = values

        I = transform_2D.identity()

        np.testing.assert_almost_equal(H_translate, I)
        np.testing.assert_almost_equal(H_scale, I)
        np.testing.assert_almost_equal(H_shear, I)
        np.testing.assert_almost_equal(H_rotate, I)
        np.testing.assert_almost_equal(H_perspective, H)


# Standalone.
if __name__ == '__main__':
    unittest.main(verbosity=2)
