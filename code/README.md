楼梯磨损动态模拟算子 (Stair Wear Simulation Engine)
1. 模块概述 (Overview)本模块是 2025 美赛 A 题建模方案的核心实现层。通过离散化网格模拟技术，将行人行为模式与物理磨损定律（Archard's Law）相结合，量化分析不同材质在长期使用下的几何退化特征。
2. 核心算法逻辑 (Core Logic)
   2.1 物理模型：Archard 磨损定律我们放弃了简单的线性减值，采用了标准的工程磨损模型：V = ( K * W * L )/ H .
       载荷 (W): 默认设为 70kg (可调)。硬度 (H): 从 config.py 动态读取，支持 Granite (800MPa) 与 Wood (30MPa) 的物理差异分析。老化因子 (aging_factor): 引入随迭代次数增加的加速系数，模拟石材受损后的结构弱化。
   2.2 行为建模：行人落脚点分布支持多种社会行为模式模拟：Right-hand Mode: 模拟对流交通流，通过 y 轴偏移产生非对称磨损坑位，用于反推古迹交通规则。Dynamic Kernel: 使用 5 * 5 非对称卷积核模拟单次踩踏的压力分布。
3. 文件结构 (File Structure)Plaintextcode/
├── main.py              # 仿真主程序：负责批量模拟、多材质对比及结果产出
├── models/
│   ├── config.py        # 材质库配置：包含不同石材的硬度 (H) 与磨损率参数
│   ├── pedestrian.py    # 行人模块：生成符合正态分布或特定社交规则的落脚点
│   └── wear_logic.py    # 物理算子：实现 Archard 公式及网格高度更新逻辑
└── README.md            # 本说明文档
4. 快速启动 (Usage)确保已配置 Python 环境并安装 numpy, matplotlib, scipy。
5. 产出物说明 (Outputs)磨损体积 (V): 自动计算矩阵积分，为“使用频率反推”提供核心物理量。剖面特征: 提取 y=50 处的截面数据，支持单双峰统计分析及路径稳定性评估。
6. 感谢使用，非常欢迎提出修改建议！
