#!/usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

预测时长 = 6
数据精度 = 1
起始时间 = 2010

# LMC Automotive和EV-Volumes提供的数据显示，2022年全球电动汽车销量总计约780万辆，同比增长68%

序列 = [0.74, 4, 5.9, 11, 19, 33, 47]
天花板 = 9152

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
plt.rcParams['font.sans-serif'] = ['Songti SC']
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.rcParams['axes.unicode_minus'] = False


def arange(n, length):
  return np.arange(n, n + length, dtype=int)


def 线性(时间, a, b):
  return a + b * 时间


def 逻辑斯蒂(时间, 初值, 增长率):
  指数值 = np.exp(增长率 * 时间)
  return (天花板 * 指数值 * 初值) / (天花板 + (指数值 - 1) * 初值)


def 指数(时间, 初值, 增长率):
  return (增长率**时间) * 初值


def main():
  len_y = len(序列)
  x = arange(0, len_y)

  预测时间线 = arange(0, len_y + 预测时长)
  预测时段 = arange(起始时间, len_y + 预测时长)

  原始数据 = '原始数据'
  plt.plot(arange(起始时间, len_y), 序列, 's', marker='.', label=原始数据)

  li = [逻辑斯蒂, 指数, 线性]
  df = pd.DataFrame([], columns=['', 原始数据] + [i.__name__ for i in li])
  df[''] = 预测时段
  df[原始数据] = 序列 + [''] * 预测时长

  def 拟合(函数):
    函数名 = 函数.__name__
    popt = curve_fit(函数, x, 序列)[0]
    预测 = 函数(预测时间线, *popt)
    plt.plot(预测时段, 预测, label=函数名)
    df[函数名] = [round(i, 数据精度) for i in 预测]

  tuple(map(拟合, li))

  print(df)
  plt.legend(loc="best")
  plt.show()


if __name__ == "__main__":
  main()
