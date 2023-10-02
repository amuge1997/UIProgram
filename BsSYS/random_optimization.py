import numpy as n


class RandomOptimization:
    def __init__(self, x_range, func, loop):
        self.x_range = x_range
        self.func = func
        self.loop = loop

    def run(self):
        x_range = self.x_range
        func = self.func
        loop = self.loop

        record = []

        best_xs = None
        best_y = - n.inf

        for i in range(loop):
            print(f' epoch  : {i+1:>5} / {loop:>5}')
            xs = []
            for xi in x_range:
                low = xi[0]
                high = xi[1]
                if low > high:
                    raise Exception('low less than high!')
                rand_float = low + (high - low) * n.random.random()
                xs.append(rand_float)
            y = func(*xs)
            # print(y)
            if not isinstance(y, float) and not isinstance(y, n.ndarray) and y.shape != ():
                raise Exception('shape must be ()')

            record.append(
                {
                    'xs': xs,
                    'y': y
                }
            )
            if y > best_y:
                best_xs = xs
                best_y = y
            print(f'     xs : {xs}')
            print(f'best xs : {best_xs}')
            print(f'     y  : {y}')
            print(f'best y  : {best_y}')
            print()

        record = sorted(record, key=lambda e: e['y'])

        return record


def f(x1, x2):
    y = - (x1**2 + x2**2)
    return y


def run():
    ro = RandomOptimization(
        x_range=[[-5, 5], [-5, 5]],
        func=f,
        loop=10000
    )
    record = ro.run()
    best_xs = record[-1]['xs']
    for r in record:
        print(r)
    print()
    print(best_xs)
    print(n.round(best_xs))


if __name__ == '__main__':
    run()








