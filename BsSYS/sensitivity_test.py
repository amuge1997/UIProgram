import numpy as n
import copy


class SensitivityTest:
    def __init__(self, xs, func, init_range, epoch, sample_nums):
        self.xs = xs
        self.func = func
        self.init_range = init_range
        self.epoch = epoch
        self.sample_nums = sample_nums

    def run(self, print_result, round_nums):
        func = self.func

        y_ori = func(*self.xs)
        print(f' Y : {y_ori}')
        print()

        epoch = self.epoch
        loop = self.sample_nums

        result_k_mean = [n.inf] * len(self.xs)
        result_k_std = [n.inf] * len(self.xs)
        result_k_max, result_k_min, result_k_max_abs = [n.inf] * len(self.xs), [n.inf] * len(self.xs), [n.inf] * len(self.xs)
        for i, x in enumerate(self.xs):
            xs_copy = copy.deepcopy(self.xs)
            last_k = n.inf
            k_mean = n.inf
            k_std = n.inf
            ks = []
            print(f'Testing the {i+1} parameter')
            for j in range(epoch):
                print(f' epoch  : {j + 1:>5} / {epoch:>5}')
                ks = []
                for lo2 in range(loop):
                    dx = self.init_range * n.random.rand() / 2**j
                    nx = x + dx
                    xs_copy[i] = nx
                    y = func(*xs_copy)
                    k_mean = (y_ori - y) / (x - nx)
                    ks.append(k_mean)
                k_mean = n.mean(ks)
                k_std = n.std(ks)
                print(f'k mean  : {k_mean}')
                print(f'k  std  : {k_std}')
                if n.abs(k_mean - last_k) < 1e-3:
                    break
                last_k = k_mean

            # print(ks)
            result_k_mean[i] = k_mean
            result_k_std[i] = n.std(ks)
            result_k_max[i] = n.max(ks)
            result_k_min[i] = n.min(ks)
            result_k_max_abs[i] = n.max(n.abs(ks))

            print()
            print(f'last mean : {k_mean}')
            print(f'last std  : {k_std}')
            print('\n')

        if print_result:
            print('k    mean :', n.round(result_k_mean, round_nums))
            print('k     std :', n.round(result_k_std, round_nums))
            print('k     max :', n.round(result_k_max, round_nums))
            print('k     min :', n.round(result_k_min, round_nums))
            print('k max abs :', n.round(result_k_max_abs, round_nums))

        result = (y_ori, result_k_mean, result_k_std, result_k_max, result_k_min, result_k_max_abs)
        return result


def f(x, y):
    return x**2 + y**2


def run():
    st = SensitivityTest(
        xs=[0, 2],
        func=f,
        init_range=10,
        epoch=3,
        sample_nums=5
    )
    y_ori, result_k_mean, result_k_std, result_k_max, result_k_min, result_k_max_abs = \
        st.run(print_result=True, round_nums=3)
    print()
    print(y_ori)


if __name__ == '__main__':
    run()
    pass
















