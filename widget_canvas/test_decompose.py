
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

    def test_decompose_scale_1(self):
        s = 0.5
        H = transform_2D.scale(s)

        values = decompose.decompose_matrix_2D(H)

        scale, shear, angle, translate, perspective = values

        np.testing.assert_equal(scale, s)
        np.testing.assert_equal(shear, [0, 0])
        np.testing.assert_equal(angle, 0)
        np.testing.assert_equal(translate, [0, 0])
        np.testing.assert_equal(perspective, [0, 0])

    def test_decompose_scale_2(self):
        s = 0.5, 0.1
        H = transform_2D.scale(s)

        values = decompose.decompose_matrix_2D(H)

        scale, shear, angle, translate, perspective = values

        np.testing.assert_equal(scale, s)
        np.testing.assert_equal(shear, [0, 0])
        np.testing.assert_equal(angle, 0)
        np.testing.assert_equal(translate, [0, 0])
        np.testing.assert_equal(perspective, [0, 0])

    def test_decompose_scale_shear(self):
        factor = 0.5
        angle = np.deg2rad(45)
        H = transform_2D.shear(factor, angle)

        values = decompose.decompose_matrix_2D(H)
        print(values)

        scale, shear, angle, translate, perspective = values

        np.testing.assert_equal(scale, 1)
        np.testing.assert_equal(shear, [factor, angle])
        np.testing.assert_equal(angle, 0)
        np.testing.assert_equal(translate, [0, 0])
        np.testing.assert_equal(perspective, [0, 0])


    # def test_shear_C(self):
    #     factor = -0.5
    #     angle = np.deg2rad(45)

    #     H = transform_2D.shear(factor, angle)

    #     self.assertTrue(transform_2D.is_valid(H))

    #     H0 = [[1.25, -.25, 0.0],
    #           [0.25, 0.75, 0.0],
    #           [0.0, 0.0, 1.0]]

    #     np.testing.assert_almost_equal(H, H0)





#     def test_decompose_shear(self):
#         p_shear_angle = np.deg2rad(5.)
#         p_shear_direction = [1., 0., 0.]

#         H = projections.transform.shear(p_shear_angle, p_shear_direction)
#         params = projections.transform.decompose(H)

#         q_scale, q_shear, q_angles, q_translate, q_perspective = params

#         self.assertTrue(np.tan(p_shear_angle) == q_shear[0])
#         self.assertTrue((q_shear[1:] == 0).all())
#         self.assertTrue((q_scale == 1).all())
#         self.assertTrue((q_angles == 0).all())
#         self.assertTrue((q_translate == 0).all())
#         self.assertTrue((q_perspective[:3] == 0).all())
#         self.assertTrue((q_perspective[3:] == 1).all())

#     def test_decompose_rotate(self):
#         p_angle = np.deg2rad(5.)

#         H = projections.transform.rotation(p_angle)
#         params = projections.transform.decompose(H)

#         q_scale, q_shear, q_angles, q_translate, q_perspective = params

#         self.assertTrue((q_angles[:2] == 0).all())
#         self.assertAlmostEqual(q_angles[2], p_angle)

#         self.assertTrue((q_scale == 1).all())
#         self.assertTrue((q_shear[1:] == 0).all())
#         # self.assertTrue((q_angles == 0).all())
#         self.assertTrue((q_translate == 0).all())
#         self.assertTrue((q_perspective[:3] == 0).all())
#         self.assertTrue((q_perspective[3:] == 1).all())

#     def test_decompose_translate(self):
#         v = [5., 0., 0.]

#         H = projections.transform.translation(v)

#         params = projections.transform.decompose(H)
#         q_scale, q_shear, q_angles, q_translate, q_perspective = params

#         self.assertTrue((v == q_translate).all())

#         self.assertTrue((q_scale == 1).all())
#         self.assertTrue((q_shear[1:] == 0).all())
#         self.assertTrue((q_angles == 0).all())
#         # self.assertTrue((q_translate == 0).all())
#         self.assertTrue((q_perspective[:3] == 0).all())
#         self.assertTrue((q_perspective[3:] == 1).all())


# Standalone.
if __name__ == '__main__':
    unittest.main(verbosity=2)
