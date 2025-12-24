#模拟行人分布
import numpy as np


def get_footfalls(pattern="right_hand", iterations=10000, discipline=8):
    """
    根据不同模式生成落脚点坐标
    pattern: "single" (单列) 或 "double" (并排)
    我个人加了一个靠右或靠左
    """
    if pattern == "single":
        # 单一正态分布，模拟大家走中间
        #normal是正态分布函数
        xs = np.random.normal(50, 10, iterations)
        ys = np.random.normal(50, 15, iterations)

    elif pattern == "double":
        # 并排走：一半人偏左，一半人偏右
        # 资深程序员会用 np.concatenate 合并两个分布
        half = iterations // 2
        # 左侧人流 (中心在35)
        xs_left = np.random.normal(35, discipline, half)
        # 右侧人流 (中心在65)
        xs_right = np.random.normal(65, discipline, half)

        xs = np.concatenate([xs_left, xs_right])
        ys = np.random.normal(50, 15, iterations)

    elif pattern == "right_hand":
        half = iterations // 2
        xs_down = np.random.normal(35, discipline, half)
        xs_up = np.random.normal(65, discipline, half)
        xs = np.concatenate([xs_down, xs_up])

        ys_up = np.random.normal(40,5, half)
        ys_down = np.random.normal(60,5, half)
        ys = np.concatenate([ys_down, ys_up])


    return xs, ys