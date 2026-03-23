#!/usr/bin/env python3
"""
Polymarket 量化交易系统 - 主入口

使用方法:
    python pm_monitor.py

策略说明:
    - 反向买入: 当价格在0.90-0.995区间时，买反方向
    - 时间窗口: 10s, 5s, 3s, 2s, 1.5s
    - 赌反转不发生
"""

from strategies.reverse import ReverseStrategy
from utils.storage import Storage
import time

def main():
    print("=" * 50)
    print("Polymarket 量化交易系统")
    print("=" * 50)
    print("策略: 反向买入 (0.90-0.995)")
    print("时间: 10s, 5s, 3s, 2s, 1.5s")
    print("=" * 50)
    
    storage = Storage()
    strategy = ReverseStrategy(storage)
    
    while True:
        try:
            strategy.run()
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n退出程序")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
