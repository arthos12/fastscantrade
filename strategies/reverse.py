#!/usr/bin/env python3
"""
反向买入策略

当价格在0.90-0.995区间时，买反方向。
赌价格会反转（根据历史数据，这个区间100%会反转）
"""

import requests
from datetime import datetime

class ReverseStrategy:
    """反向买入策略"""
    
    # 时间窗口
    TIME_WINDOWS = [10, 5, 3, 2, 1.5]
    
    # 价格区间
    PRICE_MIN = 0.90
    PRICE_MAX = 0.995
    
    def __init__(self, storage):
        self.storage = storage
        self.base_url = "https://clob.polymarket.com"
        self.markets = [
            ("btc", "5m"),
            ("eth", "5m"),
        ]
    
    def get_server_time(self):
        """获取服务器时间"""
        r = requests.get(f"{self.base_url}/time")
        return r.json() if r.status_code == 200 else None
    
    def get_market_price(self, coin, interval, period):
        """获取市场价格"""
        slug = f"{coin}-updown-{interval}-{period}"
        r = requests.get(
            f"https://polymarket.com/api/market?slug={slug}",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        if r.status_code != 200:
            return None, None
        
        m = r.json()
        if m.get('closed') or not m.get('clobTokenIds'):
            return None, None
        
        token_ids = m['clobTokenIds']
        
        up = requests.get(f"{self.base_url}/midpoint?token_id={token_ids[0]}").json()
        down = requests.get(f"{self.base_url}/midpoint?token_id={token_ids[1]}").json()
        
        return float(up.get('mid', 0)), float(down.get('mid', 0))
    
    def run(self):
        """运行策略"""
        ts = self.get_server_time()
        if not ts:
            return
        
        period = (ts // 300) * 300
        end_ts = period + 300
        remain = end_ts - ts
        
        if remain <= 0:
            return
        
        now = datetime.now().strftime("%H:%M:%S")
        
        for coin, interval in self.markets:
            up, down = self.get_market_price(coin, interval, period)
            if up is None:
                continue
            
            # 记录日志
            if remain <= 20:
                print(f"📊 {now} | {coin.upper()} | Up={up:.2f} Down={down:.2f} | 剩{remain}秒", flush=True)
            
            # 检查触发条件
            for t in self.TIME_WINDOWS:
                if remain <= t:
                    # Up在0.90-0.995区间，买跌
                    if self.PRICE_MIN <= up < self.PRICE_MAX:
                        order = {
                            "time": now,
                            "coin": coin,
                            "interval": interval,
                            "trend": f"反买_{t}s",
                            "direction": "买跌",
                            "price": up,
                            "remaining": remain,
                            "status": "pending"
                        }
                        print(f"🔔 {now} | {coin.upper()} | 反买{t}s | 买跌@{up:.2f} | 剩{remain}秒", flush=True)
                        self.storage.save(order)
                    
                    # Down在0.90-0.995区间，买涨
                    if self.PRICE_MIN <= down < self.PRICE_MAX:
                        order = {
                            "time": now,
                            "coin": coin,
                            "interval": interval,
                            "trend": f"反买_{t}s",
                            "direction": "买涨",
                            "price": down,
                            "remaining": remain,
                            "status": "pending"
                        }
                        print(f"🔔 {now} | {coin.upper()} | 反买{t}s | 买涨@{down:.2f} | 剩{remain}秒", flush=True)
                        self.storage.save(order)
