def add(*args):
    sum = 0
    for num in args:
        sum+=num

    print(sum)


def calculate(n, **kwargs):

    print(kwargs)

    n += kwargs['add']
    n *= kwargs['multiply']

    print(n)


class Car:

    def __init__(self, **kw):
        self.make = kw['make'] # will error if the kwarg is not passed
        self.model = kw.get('model') # will set to none if the kwarg is not passed


def main():
    add(1,2,3)
    add(1, 2, 3,4,5,6,7)
    add(90,3,5,222,89,433,10)
    print()
    calculate(2,add=3, multiply=5)
    calculate(0, add=20, multiply=1)
    calculate(22, add=13, multiply=9)
    print()
    my_car = Car(make = 'Nissan', model = 'GTR')
    print(my_car.make)
    print(my_car.model)


if __name__ == "__main__":
    main()
