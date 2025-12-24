import numpy as np
import matplotlib.pyplot as plt
import os

# 严格导入你的模块
from models.wear_logic import init_stair, apply_wear_archard
from models.pedestrian import get_footfalls
from models.config import MATERIAL_LIBRARY

# 1. 确保 data 文件夹存在
save_dir = 'data'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

iterations = 50000
test_materials = ["Granite", "Wood"]
current_pattern = "right_hand"

# 2. 生成统一落脚点
xs, ys = get_footfalls(pattern=current_pattern, iterations=iterations)

for mat_name in test_materials:
    stair = init_stair(100, 100)

    # --- 关键修正：从 config 中提取材质特定属性 ---
    mat_props = MATERIAL_LIBRARY[mat_name]
    h_val = mat_props["h_value"]  # 用于物理模型
    b_delta = mat_props["base_delta"]  # 用于环境老化基数

    print(f"正在模拟材质: {mat_name} (硬度: {h_val})...")

    for i in range(iterations):
        # 随时间的老化系数 (aging_factor)
        # 这里将 config 里的 base_delta 考虑进去
        current_aging = 1.0 + (i * 0.00001) * b_delta * 10000

        x = int(np.clip(xs[i], 5, 95))
        y = int(np.clip(ys[i], 5, 95))

        # 核心调用：将硬度等物理信息传给磨损算子
        stair = apply_wear_archard(stair, x, y, mat_name, aging_factor=current_aging)

    # 保存数据
    np.save(os.path.join(save_dir, f'stair_{mat_name}.npy'), stair)

# 3. 绘图并保存到 data 文件夹
plt.figure(figsize=(10, 6))
for mat_name in test_materials:
    data = np.load(os.path.join(save_dir, f'stair_{mat_name}.npy'))
    plt.plot(data[50, :], label=f"Material: {mat_name}")

plt.ylim(0, 1.1)
plt.legend()
plt.title("Comparison: Physical Wear Analysis (Archard Model)")
plt.grid(True)

# 修正：指定保存路径为 data 文件夹
plt.savefig(os.path.join(save_dir, 'comparison_plot.png'))
plt.show()