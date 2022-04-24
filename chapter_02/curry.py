#  currying in Python

def factory(x):
    def mult(y):
        return x*y
    return mult

mult2 = factory(2)
mult11 = factory(11)

print(mult2(4))
print(mult11(3))

