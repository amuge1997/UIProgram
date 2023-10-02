from BsSYS.random_optimization import RandomOptimization
from BsSYS.backtest_system import BacktestSystem
import numpy as n
from Demo_model import Model


def func(m_buy, m_sell):

    Model.m_buy = m_buy
    Model.m_sell = m_sell

    def start_pos1():
        position_series = Model.load('SHSE.000852')
        Model.index = 0
        bs = BacktestSystem(position_series, Model.open_signal, Model.close_signal, True, False)
        bs.run()

        amount_record = bs.get_amount_record()

        if len(bs.increase_record) != 0:
            win_rate = n.sum(n.where(n.array(bs.increase_record) > 0, 1, 0)) / len(bs.increase_record)
            win_rate = win_rate
            open_nums = len(bs.increase_record)
        else:
            win_rate = 0
            open_nums = 0

        return amount_record, win_rate, open_nums

    ar1, _, _ = start_pos1()
    ret = ar1[-1, 0]
    return ret


def run():
    ro = RandomOptimization(
        func=func,
        x_range=[
            [-10, 10],
            [-10, 10],
        ],

        loop=100
    )
    record = ro.run()

    print()
    for r in record[-10:]:
        print(' y', r['y'])
        print('xs', r['xs'])
        print('xs', n.int64(n.round(r['xs'][:4])))
        print()


if __name__ == '__main__':
    run()












