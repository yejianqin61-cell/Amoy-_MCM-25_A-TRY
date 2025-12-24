import numpy as np
from models.config import MATERIAL_LIBRARY


def init_stair(width=100, length=100):
    """初始化台阶：1.0代表满高度 [cite: 55, 219]"""
    return np.ones((width, length))


#受力函数 (The Kernel)


def apply_wear_archard(stair, x, y, material_name, weight=70, aging_factor = 1.0):
    """
    根据建模手的 Archard 模型进行物理更新
    V = k * (W * L) / H
    """

    # 获取物理参数
    H = MATERIAL_LIBRARY[material_name]["h_value"]
    k = 1e-4  # 磨损系数，可作为敏感性分析的变量
    W = weight * 9.8  # 法向载荷
    L = 0.05  # 单次踩踏滑动距离

    # 计算物理 delta (这里简化为深度增量)
    physical_delta = (k * W * L) / H * aging_factor
    # 1. 定义一个 5x5 的受力权重矩阵
    # 资深程序员通常称之为 "Kernel" (卷积核)
    #非对称矩阵代表上下楼梯受力不同
    kernel = np.array([
        [0.6, 0.8, 0.7, 1.0, 1.0],
        [0.9, 0.8, 0.8, 0.9, 1.0],
        [0.3, 0.8, 1.0, 0.8, 0.3],  # 中心受力最强 (1.0)
        [0.2, 0.5, 0.8, 0.5, 0.2],
        [0.1, 0.2, 0.3, 0.2, 0.1]
    ])

    # 2. 计算切片的边界 (注意不要超出台阶边缘)
    x_start, x_end = int(x - 2), int(x + 3)
    y_start, y_end = int(y - 2), int(y + 3)

    # 3. 底层更新逻辑：
    # 我们只修改 stair[x_start:x_end, y_start:y_end] 这一小块
    # 减去的量 = delta * kernel
    stair[x_start:x_end, y_start:y_end] -= physical_delta * kernel

    return stair