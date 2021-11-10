class ModularMatrix:
    def __init__(self,mod, *args) -> None:
        self.__rows = [[y%mod for y in x] for x in args]
        self.__mod = mod

    def __add__(self, other):
        sum = []
        if self.size == other.size and self.modulus == other.modulus:
            for row1, row2 in zip(self.rows, other.rows):
                sum.append([a + b for a,b in zip(row1, row2)])
            return ModularMatrix(self.modulus, *sum)
        elif self.size != other.size:
            raise ValueError("Matricies must be of equal size and modulus to perfrom addition")
        else:
            raise ValueError("Matricies must be of equal modulus to perform opertaion")
            
    def __sub__(self, other):
        diff = []
        if self.size == other.size and self.modulus == other.modulus:
            for row1, row2 in zip(self.rows, other.rows):
                diff.append([a - b for a,b in zip(row1, row2)])
            return ModularMatrix(self.modulus, *diff)
        elif self.size != other.size:
            raise ValueError("Matricies must be of equal size to perfrom subtraction")
        else:
            raise ValueError("Matricies must be of equal modulus to perform opertaion")
    
    def __mul__(self, other):
        if type(other) == ModularMatrix:
            return self.__mat_mul(self, other)
        elif type(other) == int:
            return self.__scalar_mul(self, other)

    def __rmul__(self, other):
        if type(other) == int:
            return self.__scalar_mul(self, other)
            
    def __str__(self):
        str_list = [" ".join([str(y) for y in x]) for x in self.__rows]
        return "\n".join(str_list)
    
    def __repr__(self):
        str_list = [" ".join([str(y) for y in x]) for x in self.__rows]
        return "\n".join(str_list)
    
    def __mat_mul(self, m1, m2):
        if m1.size[1] == m2.size[0] and m1.modulus == m2.modulus:
            product = []
            for row1 in m1.rows:
                new_row = []
                for row2 in m2.transposed.rows:
                    new_row.append(sum([n1 * n2 for n1,n2 in zip(row1, row2)]))
                product.append(new_row)
            
            return ModularMatrix(self.modulus, *product)
        elif m1.size[1] != m2.size[0]:
            raise ValueError("Left matrix must have same number of columns as the right matrix does rows")
        else:
            raise ValueError("Matricies must be of the same modulus to perform operation")
    
    def __scalar_mul(self, m, s):
        scalar_product = []
        for row in m.rows:
            scalar_product.append([x * s for x in row])
        
        return ModularMatrix(self.modulus, *scalar_product)
    
    def __2x2_det(self, m):
        ad = m.rows[0][0] * m.rows[1][1]
        cb = m.rows[1][0] * m.rows[0][1]
        return (ad - cb)%self.modulus

    def __2x2_inv(self, m):
        pass

    @property
    def size(self):
        return (len(self.__rows), len(self.__rows[0]))
    
    @property
    def rows(self):
        return self.__rows
    
    @property
    def cols(self):
        return ModularMatrix(self.modulus, self.transposed.rows)

    @property
    def modulus(self):
        return self.__mod
   
    @property
    def transposed(self):
        transposed = []
        for i in range(self.size[1]):
            row = []
            for j in range(self.size[0]):
                row.append(self.__rows[j][i])
            transposed.append(row)
        
        return ModularMatrix(self.modulus, *transposed)
    
    @property
    def determinant(self):
        if self.size[0] == self.size[1] == 2:
            return self.__2x2_det(self)


if __name__ == "__main__":
    test = [[2,5], [11,7]]
    a = ModularMatrix(13, *test)

    

    print(a.inverse)
