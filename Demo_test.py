from BsSYS.backtest_system import BacktestSystem, cal_increase_rate
import numpy as n
import matplotlib.pyplot as p
from Demo_model import Model


def run():
    Model.m_buy, Model.m_sell = \
        4.382683498990463, 7.2923661226289695

    position_series = Model.load('SHSE.000852')

    bs = BacktestSystem(position_series, Model.open_signal, Model.close_signal, True, False)
    bs.run()

    amount_record = bs.get_amount_record()
    profit = float(amount_record[-1])

    if len(bs.increase_record) == 0:
        win_rate = -1
    else:
        win_rate = n.sum(n.where(n.array(bs.increase_record) > 0, 1, 0)) / len(bs.increase_record)
        win_rate = float(win_rate)
    print('profit    : ', round(profit))
    print('open nums : ', len(bs.increase_record))
    print('win rate  : ', round(win_rate * 100))
    print('\n' * 3)

    amr = cal_increase_rate(amount_record)
    psr = cal_increase_rate(position_series[:, 1:2])
    amr = amr * 100
    psr = psr * 100
    p.plot(psr, label='position')
    p.plot(amr, label='benefit')
    p.legend()
    p.grid()
    p.show()


if __name__ == '__main__':
    run()






















