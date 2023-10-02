import numpy as n
import copy


class BacktestSystem:
    def __init__(self, position_series, open_func, close_func, is_ignore_open_close_same_time, is_show_running=True):
        # 至少两列 第一列为开盘价 第二列为收盘价 所有开平仓都使用后一日的开盘价
        self.position_series = position_series    # n, 2
        self.amount_record = n.zeros((position_series.shape[0], 1))

        self.open_signal = open_func
        self.close_signal = close_func

        self.is_ignore_open_close_same_time = is_ignore_open_close_same_time
        self.is_show_running = is_show_running

        self.amount = 10**2
        self.is_hold = False

        self.buy_price = None

        self.increase_record = []

    # # 根据可视序列返回是否开仓
    # @staticmethod
    # def open_signal(visible_array):
    #     return False
    #
    # # 返回是否平仓
    # @staticmethod
    # def close_signal(visible_array):
    #     return False

    def run_open(self, current_time_index):
        if self.is_show_running:
            print(current_time_index, '买入')

        if current_time_index < self.position_series.shape[0] - 1:
            after_price = self.position_series[current_time_index + 1, 0]  # 使用后一日开盘价
        else:
            after_price = self.position_series[current_time_index, 1]  # 使用该日收盘价

        self.buy_price = after_price

        self.is_hold = True

    def run_amount(self, current_time_index):
        if current_time_index < self.position_series.shape[0] - 1:
            before_price = self.position_series[current_time_index, 0]
            after_price = self.position_series[current_time_index + 1, 0]  # 使用后一日开盘价卖出
        else:
            before_price = self.position_series[current_time_index, 0]
            after_price = self.position_series[current_time_index, 1]  # 使用该日收盘价卖出
        increase = (after_price - before_price) / before_price
        self.amount = self.amount * (1 + increase)

    def run_close(self, current_time_index):
        if self.is_show_running:
            print(current_time_index, '平仓')

        if current_time_index < self.position_series.shape[0] - 1:
            after_price = self.position_series[current_time_index + 1, 0]  # 使用后一日开盘价
        else:
            after_price = self.position_series[current_time_index, 1]  # 使用该日收盘价

        increase = (after_price - self.buy_price) / self.buy_price
        self.increase_record.append(increase)
        self.buy_price = None

        self.is_hold = False

    def get_amount_record(self):
        return copy.deepcopy(self.amount_record)

    def run(self):
        ps = self.position_series
        if self.is_show_running:
            print('进入 主函数循环')
            print()
        for current_time_index in range(ps.shape[0]):
            if self.is_show_running:
                print('迭代')
            visible_series = ps[:current_time_index+1, ...]

            if self.is_show_running:
                print('>>> i              =', current_time_index)
                print('>>> before is_hold =', self.is_hold)
                print()
                print('>>> enter open_signal')

            is_open = self.open_signal(visible_series)

            if self.is_hold:
                self.run_amount(current_time_index)
            self.amount_record[current_time_index] = self.amount

            if is_open and not self.is_hold:
                self.run_open(current_time_index)

            if self.is_show_running:
                print()
                print('>>> enter close_signal')

            is_close = self.close_signal(visible_series)
            if not is_open and is_close and self.is_hold:
                self.run_close(current_time_index)

            if is_open and is_close and not self.is_ignore_open_close_same_time:
                raise Exception('同时出现开仓平仓信号')

            if self.is_show_running:
                print()
                print('>>> after is_hold  =', self.is_hold)
                print('>>> is_open        =', is_open)
                print('>>> is_close       =', is_close)
                print('>>> amount         =', self.amount)
                print('\n'*3)


def cal_increase_rate(array_ori):
    array = array_ori[:, 0]  # n,
    a0 = array[0]
    rate = (array_ori - a0) / a0
    return rate











































