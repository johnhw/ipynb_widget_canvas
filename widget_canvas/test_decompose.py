
from __future__ import division, print_function, unicode_literals

import unittest
import numpy as np

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


class Test_Basic_Stuff(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_homogeneous_single(self):
        pass

# class Test_Decompose_Transforms(unittest.TestCase):
#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass

#     def test_decompose_scale_scalar(self):
#         p_scale = 0.5
#         H_scale = projections.transform.scale(p_scale)
#         val = projections.transform.decompose(H_scale)

#         scale, shear, angles, translate, perspective = val

#         metric = (scale == p_scale).all()
#         self.assertTrue(metric)

#     def test_decompose_scale_2vec(self):
#         p_scale = 0.5, 0.5
#         H = projections.transform.scale(p_scale)
#         params = projections.transform.decompose(H)

#         q_scale, q_shear, q_angles, q_translate, q_perspective = params

#         vtest = [0.5, 0.5, 1.]
#         metric = (q_scale == vtest).all()
#         self.assertTrue(metric)

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
