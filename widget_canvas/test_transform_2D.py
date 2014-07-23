
from __future__ import division, print_function, unicode_literals

import unittest
import numpy as np

import transform_2D

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


    numpy.testing.assert_allclose(actual, desired, rtol=1e-07, atol=0, err_msg='', verbose=True)
"""

#################################################


class Test_Basic_Stuff(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_homogeneous_single(self):
        points_A = [1.0, 2.1]

        points_B = [1.0, 2.1, 1.0]

        flag_A = transform_2D.is_homogeneous(points_A)
        flag_B = transform_2D.is_homogeneous(points_B)

        self.assertFalse(flag_A)
        self.assertTrue(flag_B)

    def test_is_homogeneous_multi(self):
        points_A = [[1.0, 2.1],
                    [1.7, 4.4],
                    [5.4, 6.0],
                    [0.0, 4.4],
                    [1.5, 5.6]]

        points_B = [[1.0, 2.1, 1.0],
                    [1.7, 4.4, 1.0],
                    [5.4, 6.0, 1.0],
                    [0.0, 4.4, 1.0],
                    [1.5, 5.6, 1.0]]

        flag_A = transform_2D.is_homogeneous(points_A)
        flag_B = transform_2D.is_homogeneous(points_B)

        self.assertFalse(flag_A)
        self.assertTrue(flag_B)

    def test_invalid_homogeneous(self):
        points_A = [1.0, 2.1, 0.0]
        points_B = [1.0, 2.1, 2.0]

        points_C = [[1.0, 2.1, 1.0],
                    [1.7, 4.4, 1.0],
                    [5.4, 6.0, 1.0],
                    [0.0, 4.4, 0.0],
                    [1.5, 5.6, 0.0]]

        self.assertRaises(ValueError, transform_2D.is_homogeneous, points_A)
        self.assertRaises(ValueError, transform_2D.is_homogeneous, points_B)
        self.assertRaises(ValueError, transform_2D.is_homogeneous, points_C)

    def test_force_homogeneous_single(self):
        points_A = [1.0, 2.1]

        points_B = [1.0, 2.1, 1.0]

        points_AH = transform_2D.force_homogeneous(points_A)
        points_BH = transform_2D.force_homogeneous(points_B)

        flag_A = transform_2D.is_homogeneous(points_AH)
        flag_B = transform_2D.is_homogeneous(points_BH)

        self.assertTrue(flag_A)
        self.assertTrue(flag_B)

    def test_force_homogeneous_multi(self):
        points_A = [[1.0, 2.1],
                    [1.7, 4.4],
                    [5.4, 6.0],
                    [0.0, 4.4],
                    [1.5, 5.6]]

        points_B = [[1.0, 2.1, 1.0],
                    [1.7, 4.4, 1.0],
                    [5.4, 6.0, 1.0],
                    [0.0, 4.4, 1.0],
                    [1.5, 5.6, 1.0]]

        points_AH = transform_2D.force_homogeneous(points_A)
        points_BH = transform_2D.force_homogeneous(points_B)

        flag_A = transform_2D.is_homogeneous(points_AH)
        flag_B = transform_2D.is_homogeneous(points_BH)

        self.assertTrue(flag_A)
        self.assertTrue(flag_B)

    def test_force_cartesian_single(self):
        points_A = [1.0, 2.1]

        points_B = [1.0, 2.1, 1.0]

        points_AH = transform_2D.force_cartesian(points_A)
        points_BH = transform_2D.force_cartesian(points_B)

        flag_A = transform_2D.is_homogeneous(points_AH)
        flag_B = transform_2D.is_homogeneous(points_BH)

        self.assertFalse(flag_A)
        self.assertFalse(flag_B)

    def test_force_cartesian_multi(self):
        points_A = [[1.0, 2.1],
                    [1.7, 4.4],
                    [5.4, 6.0],
                    [0.0, 4.4],
                    [1.5, 5.6]]

        points_B = [[1.0, 2.1, 1.0],
                    [1.7, 4.4, 1.0],
                    [5.4, 6.0, 1.0],
                    [0.0, 4.4, 1.0],
                    [1.5, 5.6, 1.0]]

        points_AH = transform_2D.force_cartesian(points_A)
        points_BH = transform_2D.force_cartesian(points_B)

        flag_A = transform_2D.is_homogeneous(points_AH)
        flag_B = transform_2D.is_homogeneous(points_BH)

        self.assertFalse(flag_A)
        self.assertFalse(flag_B)

    def test_is_valid(self):
        H = np.identity(3)

        flag = transform_2D.is_valid(H)
        self.assertTrue(flag)

    def test_is_not_valid(self):
        H = np.zeros(9).reshape(3, 3)

        flag = transform_2D.is_valid(H)
        self.assertFalse(flag)

    def test_is_singular(self):
        H = np.zeros(9).reshape(3, 3)

        flag = transform_2D.is_singular(H)
        self.assertTrue(flag)

    def test_is_not_singular(self):
        H = np.identity(3)

        flag = transform_2D.is_singular(H)
        self.assertFalse(flag)

    def test_identity(self):
        A = np.identity(3)
        B = transform_2D.identity()

        np.testing.assert_equal(A, B)

#################################################


class Test_Apply(unittest.TestCase):
    def setUp(self):
        points = [[0.5, 0.5],
                  [1.0, 1.0],
                  [1.1, 1.1],
                  [2.0, 1.0],
                  [2.1, 1.0],
                  [2.2, 1.0],
                  [2.3, 1.0],
                  [2.5, 1.0],
                  [2.7, 1.0],
                  [1.5, 1.5],
                  [1.5, 2.5]]

        self.points = np.asarray(points)

    def tearDown(self):
        pass

    def test_apply_identity(self):
        I = transform_2D.identity()

        P1 = np.asarray((1.1, 1.1))
        Q1 = transform_2D.apply(I, P1)

        np.testing.assert_equal(P1, Q1)

        P2 = np.asarray((1.1, 1.1, 1))
        Q2 = transform_2D.apply(I, P2)

        np.testing.assert_equal(P2, Q2)

        P3 = np.asarray([[1.1, 1.1], [2.3, 2.3]])
        Q3 = transform_2D.apply(I, P3)

        np.testing.assert_equal(P3, Q3)

    def test_apply_scale(self):
        value = 1.5

        H = transform_2D.identity()
        H[0, 0] = value
        H[1, 1] = value

        P1 = self.points
        Q1 = transform_2D.apply(H, P1)

        np.testing.assert_equal(P1*value, Q1)

    def test_apply_offset(self):
        value = 2.2

        H = transform_2D.identity()
        H[0, 2] = value
        H[1, 2] = value

        P1 = self.points
        Q1 = transform_2D.apply(H, P1)

        np.testing.assert_equal(P1 + value, Q1)

#################################################


class Test_Apply_Chain(unittest.TestCase):
    def setUp(self):
        points = [[0.5, 0.5],
                  [1.0, 1.0],
                  [1.1, 1.1],
                  [2.0, 1.0],
                  [2.1, 1.0],
                  [2.2, 1.0],
                  [2.3, 1.0],
                  [2.5, 1.0],
                  [2.7, 1.0],
                  [1.5, 1.5],
                  [1.5, 2.5]]

        self.points = np.asarray(points)

    def tearDown(self):
        pass

    def test_is_sequence(self):
        I1 = transform_2D.identity()
        I2 = transform_2D.identity()
        I3 = transform_2D.identity()

        H1 = I1
        H1[0, 0] = 3.5

        H2 = I2
        H2[0, 2] = 3.5
        H2[1, 2] = 1

        # Single transform is not a sequence of transforms.
        A = I1
        value = transform_2D._is_sequence_of_3x3(A)
        self.assertFalse(value)

        # Sequence of two or more transforms.
        A = [I1, I2]
        value = transform_2D._is_sequence_of_3x3(A)
        self.assertTrue(value)

        A = [I1, I2, I3]
        value = transform_2D._is_sequence_of_3x3(A)
        self.assertTrue(value)

        A = [H1, I2, I3]
        value = transform_2D._is_sequence_of_3x3(A)
        self.assertTrue(value)

        A = [H1, H2, I3]
        value = transform_2D._is_sequence_of_3x3(A)
        self.assertTrue(value)

        # Not at all like a trasnform.
        A = 5
        value = transform_2D._is_sequence_of_3x3(A)
        self.assertFalse(value)

        A = np.arange(5)
        value = transform_2D._is_sequence_of_3x3(A)
        self.assertFalse(value)

    # def test_build_chain(self):

    #     Ha = transform_2D.transform.rotation(a)
    #     Ha2 = projections.transform.rotation(a*2)

    #     Hz = projections.transform.concatenate(Ha, Ha)

    #     val = np.sum((Hz - Ha2)**2)
    #     self.assertAlmostEqual(val, 0)

    def test_apply_scale(self):
        value = 1.5

        H = transform_2D.identity()
        H[0, 0] = value
        H[1, 1] = value

        P1 = self.points
        Q1 = transform_2D.apply(H, P1)

        np.testing.assert_equal(P1*value, Q1)

    def test_apply_offset(self):
        value = 2.2

        H = transform_2D.identity()
        H[0, 2] = value
        H[1, 2] = value

        P1 = self.points
        Q1 = transform_2D.apply(H, P1)

        np.testing.assert_equal(P1 + value, Q1)

#################################################


class Test_Build_Transforms(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_offset(self):
        dx = 5.1
        dy = -4.5

        v = dx, dy
        Ha = transform_2D.offset(v)

        Hb = [[1, 0, dx],
              [0, 1, dy],
              [0, 0, 1]]

        np.testing.assert_equal(Ha, Hb)

    def test_rotation(self):
        a = np.deg2rad(5.)
        c = np.cos(a)
        s = np.sin(a)

        H = transform_2D.rotate(a)

        self.assertTrue(transform_2D.is_valid(H))

        self.assertAlmostEqual(H[0, 0], c)
        self.assertAlmostEqual(H[0, 1], -s)
        self.assertAlmostEqual(H[1, 1], c)
        self.assertAlmostEqual(H[1, 0], s)

    def test_scale_single(self):
        fac = 0.5
        H = transform_2D.scale(fac)

        self.assertTrue(transform_2D.is_valid(H))

        self.assertAlmostEqual(H[0, 0], fac)
        self.assertAlmostEqual(H[1, 1], fac)
        self.assertAlmostEqual(H[2, 2], 1)

    def test_scale_vector(self):
        fac = 0.5, 0.2
        H = transform_2D.scale(fac)

        self.assertTrue(transform_2D.is_valid(H))

        self.assertAlmostEqual(H[0, 0], fac[0])
        self.assertAlmostEqual(H[1, 1], fac[1])
        self.assertAlmostEqual(H[2, 2], 1)

    def test_shear(self):
        a = np.deg2rad(5.)
        c = np.cos(a)
        s = np.sin(a)

        d = [0., 1.]
        H = transform_2D.shear(a, d)

        self.assertTrue(transform_2D.is_valid(H))

        self.assertAlmostEqual(H[1, 0], -0.08748866)
        self.assertAlmostEqual(H[0, 1], 0)

        d = [1., 0., 1.]
        H = transform_2D.shear(a, d)

        self.assertTrue(transform_2D.is_valid(H))

        self.assertAlmostEqual(H[1, 0], 0)
        self.assertAlmostEqual(H[0, 1], 0.08748866)

#     def test_perspective(self):

#         values = [0.1, 0., 0.]
#         H_pers = projections.transform.perspective(values)

#         a = np.deg2rad(5.)
#         # c = np.cos(a)
#         # s = np.sin(a)

#         H_rotate = projections.transform.rotation(a)

#         H = projections.transform.concatenate(H_pers, H_rotate)

#         self.assertTrue(H[3, 0] == values[0], values[0])

#     def test_shape_match_array(self):
#         f = 2.
#         g = 3.
#         A = 10
#         B = 20
#         C = A*f
#         D = B*g
#         img_src = np.zeros(A*B).reshape(A, B)
#         img_dst = np.zeros(C*D).reshape(C, D)

#         H = projections.transform.shape_match(img_src, img_dst)

#         # print(H)
#         self.assertTrue(H[0, 0] == g)
#         self.assertTrue(H[1, 1] == f)
#         self.assertTrue(H[2, 2] == 1)

#     def test_shape_match_shape(self):
#         f = 2.
#         g = 3.
#         A = 10
#         B = 20
#         C = A*f
#         D = B*g
#         img_src = np.zeros(A*B).reshape(A, B)
#         img_dst = np.zeros(C*D).reshape(C, D)

#         H = projections.transform.shape_match(img_src.shape, img_dst.shape)

#         # print(H)
#         self.assertTrue(H[0, 0] == g)
#         self.assertTrue(H[1, 1] == f)
#         self.assertTrue(H[2, 2] == 1)


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


# class Test_Manipulate_Transforms(unittest.TestCase):
#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass

#     def test_invert_identity_3D(self):
#         H = np.identity(3)
#         H_inv = projections.transform.invert(H)

#         val = np.sum((H - H_inv)**2)
#         self.assertAlmostEqual(val, 0)

#     def test_invert_identity_4D(self):
#         H = np.identity(4)
#         H_inv = projections.transform.invert(H)

#         val = np.sum((H - H_inv)**2)
#         self.assertAlmostEqual(val, 0)

#     def test_invert_accept_sequence(self):
#         H = np.identity(3).tolist()
#         H_inv = projections.transform.invert(H)

#         val = np.sum((H - H_inv)**2)
#         self.assertAlmostEqual(val, 0)

#     def test_invert_scale(self):
#         a = 0.5
#         b = 10.0

#         H = np.identity(3)
#         H[0, 0] = a
#         H[1, 1] = b
#         H_inv = projections.transform.invert(H)

#         self.assertTrue(H_inv[0, 0] == 1./a)
#         self.assertTrue(H_inv[1, 1] == 1./b)

#     def test_invert_translate(self):
#         a = 5.5
#         b = -12.4

#         H = np.identity(3)
#         H[0, 2] = a
#         H[1, 2] = b

#         H_inv = projections.transform.invert(H)

#         self.assertTrue(H_inv[0, 2] == -a)
#         self.assertTrue(H_inv[1, 2] == -b)

#     def test_invert_rotate(self):
#         a = np.deg2rad(5.)

#         H = projections.transform.rotation(a)
#         H_inv = projections.transform.invert(H)

#         # print()
#         # print(np.cos(a))
#         # print(H)
#         # print(H_inv)

#         self.assertTrue(H[0, 0] == H[1, 1] == np.cos(a))
#         self.assertTrue(H[1, 0] == -H[0, 1] == np.sin(a))
#         self.assertTrue(H[0, 1] == -H[1, 0] == -np.sin(a))

#         self.assertTrue(H_inv[0, 0] == H[1, 1])
#         self.assertTrue(H_inv[1, 1] == H[1, 1])
#         self.assertTrue(H_inv[0, 1] == -H[0, 1])
#         self.assertTrue(H_inv[1, 0] == -H[1, 0])

#     def test_concatenate_angles(self):
#         a = np.deg2rad(5.)

#         Ha = projections.transform.rotation(a)
#         Ha2 = projections.transform.rotation(a*2)

#         Hz = projections.transform.concatenate(Ha, Ha)

#         val = np.sum((Hz - Ha2)**2)
#         self.assertAlmostEqual(val, 0)

#     def test_concatenate_angles_and_offsets(self):
#         a = np.deg2rad(5.)
#         d = [10, -10]

#         Ha = projections.transform.rotation(a)
#         Ht = projections.transform.translation(d)

#         Hq = projections.transform.concatenate(Ht, Ha)
#         Hz = projections.transform.concatenate(Ha, Ht)

#         # Rotation parts should be the same.
#         val = np.sum((Hq[:2, :2] - Hz[:2, :2])**2)
#         self.assertAlmostEqual(val, 0)

#         # Offset parts should NOT be the same.
#         self.assertAlmostEqual(Hz[0, 3], 10)
#         self.assertAlmostEqual(Hz[1, 3], -10)
#         self.assertAlmostEqual(Hq[0, 3], 10.83350441)
#         self.assertAlmostEqual(Hq[1, 3], -9.09038955)


# Standalone.
if __name__ == '__main__':
    unittest.main(verbosity=2)
