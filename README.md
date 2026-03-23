# Polymarket 量化交易系统

## 概述

本系统用于 Polymarket 5分钟预测市场的量化交易策略测试。

## 核心发现

### 关键结论（必须理解）

1. **Polymarket 5m 市场的本质**
   - 最后2秒会剧烈反转（暴力插针）
   - 无法预测，只能等结果确认后下单
   - 100%胜率的策略不存在

2. **时间 + 价格 = 确定性**
   - 单独看价格或时间都没有意义
   - 必须组合分析

3. **反转规律**
   | 价格区间 | 时间 | 胜率 | 结论 |
   |----------|------|------|------|
   | 0.80-0.90 | 任意 | 100% | 安全 |
   | 0.90-0.95 | 任意 | 0% | 必亏 |
   | 0.99+ | >2秒 | 100% | 安全 |
   | 0.99+ | <=2秒 | 88% | 有风险 |

4. **反转因子**
   - 价格0.90-0.95是临界点，最容易反转
   - 时间越接近结束，反转概率越高

## 策略说明

### 当前策略: 反向买入（赌反转不发生）

- **触发条件**: 价格在0.90-0.995区间
- **时间窗口**: 10s, 5s, 3s, 2s, 1.5s
- **动作**: 买反方向

### 逻辑

1. 当价格在0.90-0.995区间时，根据历史数据，这个区间100%会反转
2. 所以买反方向，赌反转不发生
3. 如果不反转，则盈利

## 安装

```bash
pip install requests
python pm_monitor.py
```

## API 说明

### 核心接口

1. **获取服务器时间**
```
GET https://clob.polymarket.com/time
返回: {"clock": 1774231447}
```

2. **获取市场信息**
```
GET https://polymarket.com/api/market?slug=btc-updown-5m-1774231200
返回: {
  "closed": false,
  "clobTokenIds": ["token_id_up", "token_id_down"]
}
```

3. **获取当前价格**
```
GET https://clob.polymarket.com/midpoint?token_id=xxx
返回: {"mid": 0.95}
```

4. **获取结算价**
```
GET https://clob.polymarket.com/last-trade-price?token_id=xxx
返回: {"price": 0.99}
```

### Slug 格式

```
{coin}-updown-{interval}-{period}

例如:
- btc-updown-5m-1774231200
- eth-updown-5m-1774231200
- btc-updown-15m-1774231200
```

### Period 计算

```python
# 5分钟周期
period = (timestamp // 300) * 300

# 15分钟周期
period = (timestamp // 900) * 900
```

## 目录结构

```
pm_quant/
├── README.md           # 本文档
├── pm_monitor.py      # 主程序入口
├── strategies/         # 策略模块
│   └── reverse.py     # 反向买入策略
├── utils/             # 工具模块
│   ├── api.py        # API封装
│   └── storage.py    # 订单存储
└── docs/             # 文档
    └── api_ref.md    # API参考
```

## 使用方法

1. 查看 README.md 了解策略逻辑
2. 运行 `python pm_monitor.py`
3. 查看日志和订单结果

## 注意事项

1. API 有频率限制，避免高频请求
2. 本系统仅供学习研究，不构成投资建议
3. 实际交易前请充分测试
