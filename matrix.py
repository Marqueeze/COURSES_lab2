from fractions import Fraction


class Matrix(object):

    @classmethod
    def identity_matrix(cls, dim: int):
        im = cls(dim)
        for i in range(dim):
            im[i, i] = 1
        return im

    def __init__(self, dim: int, fill=0):
        if dim < 1:
            raise Exception('Dimension cannot be <1')
        self.dim = dim
        self.A = [[Fraction(fill)] * self.dim for _ in range(self.dim)]

    def __getitem__(self, indexes):
        if isinstance(indexes, tuple):
            return self.A[indexes[0]][indexes[1]]
        else:
            return self.A[indexes]

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            self.A[key[0]][key[1]] = Fraction(value)
        else:
            self.A[key] = value

    def __repr__(self):
        represent = ""
        for i in range(len(self.A)):
            represent += ', '.join(map(lambda x: '{}/{}'.format(x.numerator, x.denominator), self.A[i])) + "\n"
        return represent

    def __str__(self):
        return self.__repr__()

    def _non_matrix_op(self, other, op):
        func = {'add': lambda x, y: x + y,
                'mul': lambda x, y: x * y}[op]

        result = Matrix(self.dim)
        if isinstance(other, Matrix):
            if other.dim == self.dim and other.dim == self.dim:
                for i in range(result.dim):
                    for j in range(result.dim):
                        result[i, j] = func(self[i, j], other[i, j])
            else:
                raise Exception('Trying to operate ({s}, {s}) matrix with ({o}, {o}) matrix'
                                .format(s=self.dim, o=other.dim))

        elif isinstance(other, int) or isinstance(other, float):
            for i in range(result.dim):
                for j in range(result.dim):
                    result[i, j] = func(self[i, j], other)
        else:
            raise Exception('Type mismatch. Matrix cannot be operated to {}'.format(type(other)))
        return result

    def __add__(self, other):
        return self._non_matrix_op(other, 'add')

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return self._non_matrix_op(other, 'mul')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __matmul__(self, other):
        if isinstance(other, Matrix):
            if self.dim == other.dim:
                result = Matrix(self.dim)

                for i in range(self.dim):
                    for j in range(self.dim):
                        acc = 0

                        for k in range(self.dim):
                            acc += self[i, k] * other[k, j]

                        result[i, j] = acc
            else:
                raise Exception('Dimension mismatch. Trying to multiple ({s}, {s}) matrix with ({o}, {o})'
                                .format(s=self.dim, o=other.dim))
        else:
            raise Exception('Cannot MatMul Matrix with non-matrix object. Try standard multiplication')

        return result

    def transpose(self):
        for i in range(self.dim):
            for j in range(i, self.dim):
                tmp = self[i, j]
                self[i, j] = self[j, i]
                self[j, i] = tmp
        return self

    def _change_zero(self, start_index):
        check = False
        for i in range(start_index + 1, self.dim):
            if self[i, start_index] != 0:
                tmp = self[i]
                self[i] = self[start_index]
                self[start_index] = tmp
                check = True
                break
        if not check:
            raise Exception("Inverse matrix does not exist")
        return self

    def copy(self):
        result = Matrix(dim=self.dim)
        for i in range(result.dim):
            for j in range(result.dim):
                result[i, j] = self[i, j]
        return result

    def inverse(self):
        self_copy = self.copy()
        ident_mat = Matrix.identity_matrix(self.dim)

        if self_copy[0, 0] == 0:
            self_copy._change_zero(0)

        mult = self_copy[0, 0]
        for j in range(0, self_copy.dim):
            ident_mat[0, j] = ident_mat[0, j] / mult
            self_copy[0, j] = self_copy[0, j] / mult

        for k in range(0, self_copy.dim):
            for i in range(0, self_copy.dim):
                if k != i:
                    mult = self_copy[i, k] / self_copy[k, k]
                    for j in range(0, self_copy.dim):
                        ident_mat[i, j] -= ident_mat[k, j] * mult
                        self_copy[i, j] -= self_copy[k, j] * mult

                    if self_copy[i, i] == 0:
                        self_copy._change_zero(i)

                    ii = self_copy[i, i]
                    for j in range(0, self_copy.dim):
                        ident_mat[i, j] /= ii
                        self_copy[i, j] /= ii

        return ident_mat

    def determinant(self):
        pass
