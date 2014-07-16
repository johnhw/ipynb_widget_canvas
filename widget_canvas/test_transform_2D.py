
from __future__ import division, print_function, unicode_literals

import unittest
import numpy as np

import transform_2D


class Test_Basic_Stuff(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gohlke_imported(self):
        self.assertTrue(hasattr(projections, 'gohlke'))
        self.assertTrue(hasattr(projections.gohlke, 'transformations'))
        self.assertTrue(hasattr(projections.gohlke.transformations, 'identity_matrix'))

    def test_homo_4d_to_3d(self):
        H = [[1, 2, 3, 5],
             [6, 7, 8, 9],
             [10, 11, 12, 13],
             [14, 15, 16, 1]]

        H_true = [[1, 2, 5],
                  [6, 7, 9],
                  [14, 15, 1]]
        H_true = np.asarray(H_true)

        H_test = projections.transform.homo_4d_to_3d(H)

        # print()
        # print(np.asarray(H))
        # print(H_test)
        self.assertTrue((H_test - H_true == 0).all())

    def test_homo_3d_to_4d(self):
        H = [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 1]]

        H_true = [[1, 2, 0, 3],
                  [4, 5, 0, 6],
                  [0, 0, 1, 0],
                  [7, 8, 0, 1]]

        H_true = np.asarray(H_true)

        H_test = projections.transform.homo_3d_to_4d(H)

        # print()
        # print(np.asarray(H))
        # print(H_test)
        # print(H_true)
        self.assertTrue((H_test - H_true == 0).all())


class Test_Build_Transforms(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_transform_is_valid(self):
        H_good_a = np.identity(4)
        H_bad_a = np.identity(4)
        H_bad_a[3, 3] = 1.4
        H_bad_b = np.identity(3)

        self.assertTrue(projections.transform.transform_is_valid(H_good_a))
        self.assertFalse(projections.transform.transform_is_valid(H_bad_a))
        self.assertFalse(projections.transform.transform_is_valid(H_bad_b))

    def test_translation(self):
        v = [5., 0., 0.]
        H = projections.transform.translation(v)

        self.assertTrue(projections.transform.transform_is_valid(H))
        self.assertAlmostEqual(H[0, 3], 5)
        self.assertAlmostEqual(H[1, 3], 0)
        self.assertAlmostEqual(H[2, 3], 0)
        self.assertAlmostEqual(H[3, 3], 1)

        v = [3., 1., 0.]
        H = projections.transform.translation(v)

        self.assertTrue(projections.transform.transform_is_valid(H))
        self.assertAlmostEqual(H[0, 3], 3)
        self.assertAlmostEqual(H[1, 3], 1)
        self.assertAlmostEqual(H[2, 3], 0)
        self.assertAlmostEqual(H[3, 3], 1)

        v = [0., 1., -22.]
        H = projections.transform.translation(v)

        self.assertTrue(projections.transform.transform_is_valid(H))
        self.assertAlmostEqual(H[0, 3], 0)
        self.assertAlmostEqual(H[1, 3], 1)
        self.assertAlmostEqual(H[2, 3], -22)
        self.assertAlmostEqual(H[3, 3], 1)

    def test_rotation(self):
        a = np.deg2rad(5.)
        c = np.cos(a)
        s = np.sin(a)

        H = projections.transform.rotation(a)

        self.assertTrue(projections.transform.transform_is_valid(H))
        self.assertAlmostEqual(H[0, 0], c)
        self.assertAlmostEqual(H[0, 1], -s)
        self.assertAlmostEqual(H[1, 1], c)
        self.assertAlmostEqual(H[1, 0], s)

    def test_scale_single(self):
        fac = 0.5
        H = projections.transform.scale(fac)

        self.assertTrue(projections.transform.transform_is_valid(H))
        self.assertAlmostEqual(H[0, 0], fac)
        self.assertAlmostEqual(H[1, 1], fac)
        self.assertAlmostEqual(H[2, 2], fac)
        self.assertAlmostEqual(H[3, 3], 1)

    def test_scale_2vector(self):
        fac = 0.5, 0.2
        H = projections.transform.scale(fac)

        self.assertTrue(projections.transform.transform_is_valid(H))
        self.assertAlmostEqual(H[0, 0], fac[0])
        self.assertAlmostEqual(H[1, 1], fac[1])
        self.assertAlmostEqual(H[2, 2], 1)
        self.assertAlmostEqual(H[3, 3], 1)

    def test_shear(self):
        a = np.deg2rad(5.)

        d = [0., 1., 0.]
        H = projections.transform.shear(a, d)

        self.assertTrue(projections.transform.transform_is_valid(H))
        self.assertAlmostEqual(H[1, 0], -0.08748866)
        self.assertAlmostEqual(H[0, 1], 0)

        d = [1., 0., 0.]
        H = projections.transform.shear(a, d)

        self.assertTrue(projections.transform.transform_is_valid(H))
        self.assertAlmostEqual(H[1, 0], 0)
        self.assertAlmostEqual(H[0, 1], 0.08748866)

    def test_perspective(self):

        values = [0.1, 0., 0.]
        H_pers = projections.transform.perspective(values)

        a = np.deg2rad(5.)
        # c = np.cos(a)
        # s = np.sin(a)

        H_rotate = projections.transform.rotation(a)

        H = projections.transform.concatenate(H_pers, H_rotate)

        self.assertTrue(H[3, 0] == values[0], values[0])

    def test_shape_match_array(self):
        f = 2.
        g = 3.
        A = 10
        B = 20
        C = A*f
        D = B*g
        img_src = np.zeros(A*B).reshape(A, B)
        img_dst = np.zeros(C*D).reshape(C, D)

        H = projections.transform.shape_match(img_src, img_dst)

        # print(H)
        self.assertTrue(H[0, 0] == g)
        self.assertTrue(H[1, 1] == f)
        self.assertTrue(H[2, 2] == 1)

    def test_shape_match_shape(self):
        f = 2.
        g = 3.
        A = 10
        B = 20
        C = A*f
        D = B*g
        img_src = np.zeros(A*B).reshape(A, B)
        img_dst = np.zeros(C*D).reshape(C, D)

        H = projections.transform.shape_match(img_src.shape, img_dst.shape)

        # print(H)
        self.assertTrue(H[0, 0] == g)
        self.assertTrue(H[1, 1] == f)
        self.assertTrue(H[2, 2] == 1)


class Test_Estimate_Transforms(unittest.TestCase):
    def setUp(self):
        # Build model transform.
        a = np.deg2rad(30)
        f = (0.85, 1.2)
        o = (10, 30)

        H_a = projections.transform.rotation(a)
        H_b = projections.transform.scale(f)
        H_c = projections.transform.translation(o)

        H_model = projections.transform.concatenate(H_a, H_b, H_c)

        # Write to files.
        # import data_io
        # H_a = projections.transform.homo_in_3d(H_a)
        # H_b = projections.transform.homo_in_3d(H_b)
        # H_c = projections.transform.homo_in_3d(H_c)
        # H_model = projections.transform.homo_in_3d(H_model)
        # H_model_inv = projections.transform.invert(H_model)

        # data_io.write('H_a.yml', H_a.tolist())
        # data_io.write('H_b.yml', H_b.tolist())
        # data_io.write('H_c.yml', H_c.tolist())
        # data_io.write('H_m.yml', H_model.tolist())
        # data_io.write('H_m_inv.yml', H_model_inv.tolist())

        self.H_model = projections.transform.homo_in_3d(H_model)

        # Build test data.
        N_samples = 1000
        V_max = 500

        # True model data.
        self.data_src_true = np.random.uniform(0, V_max, size=(N_samples, 2))
        self.data_dst_true = projections.warp.warp_points(self.data_src_true, self.H_model)

        # Noisy observations.
        sigma_nice = 0.05
        self.sigma = sigma_nice
        sigma_crap = 5.
        self.frac_crap = 0.2

        # Nice noise.
        noise = np.random.normal(0., sigma_nice, size=(N_samples, 2))
        self.data_src_noisy = self.data_src_true + noise

        noise = np.random.normal(0., sigma_nice, size=(N_samples, 2))
        self.data_dst_noisy = self.data_dst_true + noise

        # Crappy noise.
        N_crap = int(N_samples*self.frac_crap)
        noise = np.random.normal(0., sigma_crap, size=(N_crap, 2))
        self.data_src_noisy[:N_crap, :] += noise

        noise = np.random.normal(0., sigma_crap, size=(N_crap, 2))
        self.data_dst_noisy[:N_crap, :] += noise

    def tearDown(self):
        pass

    def test_does_it_call(self):
        projections.transform.estimate(self.data_src_noisy, self.data_dst_noisy)

    def test_same_to_same(self):
        H, ix = projections.transform.estimate(self.data_src_noisy, self.data_src_noisy)
        err = np.sum((H - np.identity(3))**2)
        self.assertAlmostEqual(err, 0)

    def test_src_to_dst(self):
        # sigma_total is the computed noise on the observed difference between measured DST point
        # and the transformed SRC point.  The factor of 4 is due to noise being added to two
        # dimension in the SRC data and to two dimensions in the DST data.  In this case I expect
        # the number of estimated inliers to be related to the number of samples not affected by
        # the crappy noise.

        sigma_total = np.sum(4.*self.sigma**2)**.5
        threshold = 5*sigma_total

        H, ix = projections.transform.estimate(self.data_src_noisy, self.data_dst_noisy,
                                               threshold=threshold)
        N_inlier = np.sum(ix)
        err = np.sum((H - self.H_model)**2)

        # print()
        # print(sigma_total, threshold)
        # print(self.H_model)
        # print(H)
        # print(err)
        # print(np.sum(ix))

        N_samples = self.data_src_noisy.shape[0]
        N_crap = int(N_samples*self.frac_crap)
        N_inlier_model = N_samples - N_crap

        self.assertTrue(abs(N_inlier - N_inlier_model) < 5)
        self.assertTrue(err <= 2.e-3, err)


class Test_Decompose_Transforms(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_decompose_scale_scalar(self):
        p_scale = 0.5
        H_scale = projections.transform.scale(p_scale)
        val = projections.transform.decompose(H_scale)

        scale, shear, angles, translate, perspective = val

        metric = (scale == p_scale).all()
        self.assertTrue(metric)

    def test_decompose_scale_2vec(self):
        p_scale = 0.5, 0.5
        H = projections.transform.scale(p_scale)
        params = projections.transform.decompose(H)

        q_scale, q_shear, q_angles, q_translate, q_perspective = params

        vtest = [0.5, 0.5, 1.]
        metric = (q_scale == vtest).all()
        self.assertTrue(metric)

    def test_decompose_shear(self):
        p_shear_angle = np.deg2rad(5.)
        p_shear_direction = [1., 0., 0.]

        H = projections.transform.shear(p_shear_angle, p_shear_direction)
        params = projections.transform.decompose(H)

        q_scale, q_shear, q_angles, q_translate, q_perspective = params

        self.assertTrue(np.tan(p_shear_angle) == q_shear[0])
        self.assertTrue((q_shear[1:] == 0).all())
        self.assertTrue((q_scale == 1).all())
        self.assertTrue((q_angles == 0).all())
        self.assertTrue((q_translate == 0).all())
        self.assertTrue((q_perspective[:3] == 0).all())
        self.assertTrue((q_perspective[3:] == 1).all())

    def test_decompose_rotate(self):
        p_angle = np.deg2rad(5.)

        H = projections.transform.rotation(p_angle)
        params = projections.transform.decompose(H)

        q_scale, q_shear, q_angles, q_translate, q_perspective = params

        self.assertTrue((q_angles[:2] == 0).all())
        self.assertAlmostEqual(q_angles[2], p_angle)

        self.assertTrue((q_scale == 1).all())
        self.assertTrue((q_shear[1:] == 0).all())
        # self.assertTrue((q_angles == 0).all())
        self.assertTrue((q_translate == 0).all())
        self.assertTrue((q_perspective[:3] == 0).all())
        self.assertTrue((q_perspective[3:] == 1).all())

    def test_decompose_translate(self):
        v = [5., 0., 0.]

        H = projections.transform.translation(v)

        params = projections.transform.decompose(H)
        q_scale, q_shear, q_angles, q_translate, q_perspective = params

        self.assertTrue((v == q_translate).all())

        self.assertTrue((q_scale == 1).all())
        self.assertTrue((q_shear[1:] == 0).all())
        self.assertTrue((q_angles == 0).all())
        # self.assertTrue((q_translate == 0).all())
        self.assertTrue((q_perspective[:3] == 0).all())
        self.assertTrue((q_perspective[3:] == 1).all())


class Test_Manipulate_Transforms(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_invert_identity_3D(self):
        H = np.identity(3)
        H_inv = projections.transform.invert(H)

        val = np.sum((H - H_inv)**2)
        self.assertAlmostEqual(val, 0)

    def test_invert_identity_4D(self):
        H = np.identity(4)
        H_inv = projections.transform.invert(H)

        val = np.sum((H - H_inv)**2)
        self.assertAlmostEqual(val, 0)

    def test_invert_accept_sequence(self):
        H = np.identity(3).tolist()
        H_inv = projections.transform.invert(H)

        val = np.sum((H - H_inv)**2)
        self.assertAlmostEqual(val, 0)

    def test_invert_scale(self):
        a = 0.5
        b = 10.0

        H = np.identity(3)
        H[0, 0] = a
        H[1, 1] = b
        H_inv = projections.transform.invert(H)

        self.assertTrue(H_inv[0, 0] == 1./a)
        self.assertTrue(H_inv[1, 1] == 1./b)

    def test_invert_translate(self):
        a = 5.5
        b = -12.4

        H = np.identity(3)
        H[0, 2] = a
        H[1, 2] = b

        H_inv = projections.transform.invert(H)

        self.assertTrue(H_inv[0, 2] == -a)
        self.assertTrue(H_inv[1, 2] == -b)

    def test_invert_rotate(self):
        a = np.deg2rad(5.)

        H = projections.transform.rotation(a)
        H_inv = projections.transform.invert(H)

        # print()
        # print(np.cos(a))
        # print(H)
        # print(H_inv)

        self.assertTrue(H[0, 0] == H[1, 1] == np.cos(a))
        self.assertTrue(H[1, 0] == -H[0, 1] == np.sin(a))
        self.assertTrue(H[0, 1] == -H[1, 0] == -np.sin(a))

        self.assertTrue(H_inv[0, 0] == H[1, 1])
        self.assertTrue(H_inv[1, 1] == H[1, 1])
        self.assertTrue(H_inv[0, 1] == -H[0, 1])
        self.assertTrue(H_inv[1, 0] == -H[1, 0])

    def test_concatenate_angles(self):
        a = np.deg2rad(5.)

        Ha = projections.transform.rotation(a)
        Ha2 = projections.transform.rotation(a*2)

        Hz = projections.transform.concatenate(Ha, Ha)

        val = np.sum((Hz - Ha2)**2)
        self.assertAlmostEqual(val, 0)

    def test_concatenate_angles_and_offsets(self):
        a = np.deg2rad(5.)
        d = [10, -10]

        Ha = projections.transform.rotation(a)
        Ht = projections.transform.translation(d)

        Hq = projections.transform.concatenate(Ht, Ha)
        Hz = projections.transform.concatenate(Ha, Ht)

        # Rotation parts should be the same.
        val = np.sum((Hq[:2, :2] - Hz[:2, :2])**2)
        self.assertAlmostEqual(val, 0)

        # Offset parts should NOT be the same.
        self.assertAlmostEqual(Hz[0, 3], 10)
        self.assertAlmostEqual(Hz[1, 3], -10)
        self.assertAlmostEqual(Hq[0, 3], 10.83350441)
        self.assertAlmostEqual(Hq[1, 3], -9.09038955)


# Standalone.
if __name__ == '__main__':
    unittest.main(verbosity=2)
