import numpy as n


class Model:
    m_buy = None
    m_sell = None

    index = 0

    @staticmethod
    def load(file_name):
        import json
        with open(f'data/{file_name}.json') as fp:
            ls = json.load(fp)
        position_series = n.zeros((len(ls), 3), dtype='float64')
        for i, dc in enumerate(ls):
            op = dc['open']
            cl = dc['close']
            vo = dc['volume']
            position_series[i, 0] = op
            position_series[i, 1] = cl
            position_series[i, 2] = vo
        return position_series

    @staticmethod
    def open_signal(visible_array):
        at_last_days = 22
        if visible_array.shape[0] < at_last_days:
            return False
        close_rate = Model.momentum(visible_array)
        if close_rate > Model.m_buy:
            return True
        else:
            return False

    @staticmethod
    def close_signal(visible_array):
        at_last_days = 22
        if visible_array.shape[0] < at_last_days:
            return False

        close_rate = Model.momentum(visible_array)
        if close_rate < Model.m_sell:
            return True
        else:
            return False

    @staticmethod
    def momentum(array):
        # array.shape = n, 1
        close = array[-21:, 1]
        f = close[-1] / close[-21]
        f = n.array(f) - 1
        f = f * 100
        return f















