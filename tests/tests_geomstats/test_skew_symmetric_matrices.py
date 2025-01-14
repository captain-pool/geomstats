"""Unit tests for the skew symmetric matrices."""
import random

import geomstats.backend as gs
from geomstats.geometry.skew_symmetric_matrices import SkewSymmetricMatrices
from tests.conftest import TestCase
from tests.data_generation import MatrixLieAlgebraTestData
from tests.parametrizers import MatrixLieAlgebraParametrizer


class TestSkewSymmetricMatrices(TestCase, metaclass=MatrixLieAlgebraParametrizer):

    space = algebra = SkewSymmetricMatrices

    class TestDataSkewSymmetricMatrices(MatrixLieAlgebraTestData):
        n_list = random.sample(range(2, 5), 2)
        space_args_list = [(n,) for n in n_list]
        shape_list = [(n, n) for n in n_list]
        n_samples_list = random.sample(range(2, 5), 2)
        n_points_list = random.sample(range(2, 5), 2)
        n_vecs_list = random.sample(range(2, 5), 2)

        def belongs_data(self):
            smoke_data = [
                dict(n=2, mat=[[0.0, -1.0], [1.0, 0.0]], expected=True),
                dict(n=3, mat=[[0.0, -1.0], [1.0, 0.0]], expected=False),
            ]
            return self.generate_tests(smoke_data)

        def baker_campbell_hausdorff_data(self):
            n_list = range(3, 10)
            smoke_data = []
            for n in n_list:
                space = SkewSymmetricMatrices(n)
                fb = space.basis[0]
                sb = space.basis[1]
                fb_sb_bracket = space.bracket(fb, sb)
                expected1 = fb + sb
                expected2 = expected1 + 0.5 * fb_sb_bracket
                expected3 = (
                    expected2
                    + 1.0 / 12.0 * space.bracket(fb, fb_sb_bracket)
                    - 1.0 / 12.0 * space.bracket(sb, fb_sb_bracket)
                )
                expected4 = expected3 - 1.0 / 24.0 * space.bracket(
                    sb, space.bracket(fb, fb_sb_bracket)
                )
                expected = [expected1, expected2, expected3, expected4]
                for order in range(1, 5):
                    smoke_data.append(
                        dict(
                            n=n,
                            matrix_a=fb,
                            matrix_b=sb,
                            order=order,
                            expected=expected[order - 1],
                        )
                    )

            return self.generate_tests(smoke_data)

        def basis_representation_matrix_representation_composition_data(self):
            return self._basis_representation_matrix_representation_composition_data(
                SkewSymmetricMatrices, self.space_args_list, self.n_samples_list
            )

        def matrix_representation_basis_representation_composition_data(self):
            return self._matrix_representation_basis_representation_composition_data(
                SkewSymmetricMatrices, self.space_args_list, self.n_samples_list
            )

        def basis_belongs_data(self):
            return self._basis_belongs_data(self.space_args_list)

        def basis_cardinality_data(self):
            return self._basis_cardinality_data(self.space_args_list)

        def random_point_belongs_data(self):
            smoke_space_args_list = [(2,), (3,)]
            smoke_n_points_list = [1, 2]
            return self._random_point_belongs_data(
                smoke_space_args_list,
                smoke_n_points_list,
                self.space_args_list,
                self.n_points_list,
            )

        def projection_belongs_data(self):
            return self._projection_belongs_data(
                self.space_args_list, self.shape_list, self.n_samples_list
            )

        def to_tangent_is_tangent_data(self):
            return self._to_tangent_is_tangent_data(
                SkewSymmetricMatrices,
                self.space_args_list,
                self.shape_list,
                self.n_vecs_list,
            )

    testing_data = TestDataSkewSymmetricMatrices()

    def test_belongs(self, n, mat, expected):
        skew = self.space(n)
        self.assertAllClose(skew.belongs(gs.array(mat)), gs.array(expected))

    def test_baker_campbell_hausdorff(self, n, matrix_a, matrix_b, order, expected):
        skew = SkewSymmetricMatrices(n)
        result = skew.baker_campbell_hausdorff(
            gs.array(matrix_a), gs.array(matrix_b), order=order
        )
        self.assertAllClose(result, gs.array(expected))
