#!/usr/bin/env python3
import requests, time, json
from datetime import datetime, timezone

ORDERS_FILE = "/root/.openclaw/workspace/pm_orders.json"

def load_orders():
    try:
        with open(ORDERS_FILE, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except:
        return []

def save_orders(orders):
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=2)

orders = load_orders()

# 策略1: 0.75-0.85 + 时间10s 5s 3s 2s
# 策略2: 0.70-0.85 + 时间10s 5s 3s 2s
# 策略3: 反着买: 0.90-0.995 + 时间10s 5s 3s 2s
print("策略: 0.75-0.85(10s/5s/3s/2s), 0.70-0.85(10s/5s/3s/2s), 反着买", flush=True)

while 1:
    try:
        r = requests.get("https://clob.polymarket.com/time")
        ts = r.json() if r.status_code==200 else None
        if not ts: time.sleep(0.5); continue
        
        current_5m = (ts // 300) * 300
        
        for c,i,p in [("btc","5m",current_5m),("eth","5m",current_5m)]:
            mr = requests.get(f"https://polymarket.com/api/market?slug={c}-updown-{i}-{p}", headers={"User-Agent":"Mozilla/5.0"})
            if mr.status_code!=200: continue
            m = mr.json()
            if m.get('closed'): continue
            if not m.get('clobTokenIds'): continue
            
            up = float(requests.get(f"https://clob.polymarket.com/midpoint?token_id={m['clobTokenIds'][0]}").json().get('mid',0))
            down = float(requests.get(f"https://clob.polymarket.com/midpoint?token_id={m['clobTokenIds'][1]}").json().get('mid',0))
            
            end_ts = p + 300
            remain = end_ts - ts
            
            if remain <= 0: continue
            
            # 使用ET (东部时间) - Polymarket时区
            now = datetime.now(timezone(timedelta(hours=-4))).strftime("%H:%M:%S")
            
            if remain <= 20:
                print(f"📊 {now} | {c.upper()} | Up={up:.2f} Down={down:.2f} | 剩{remain}秒", flush=True)
            
            # 策略1: 0.75-0.85 + 时间10s 5s 3s 2s
            for t in [10, 5, 3, 2]:
                if remain <= t:
                    # Up在0.75-0.85区间，买涨
                    if 0.75 < up < 0.85:
                        orders.append({"id": len(orders)+1, "time": now, "coin": c, "interval": i, "trend": f"0.75-0.85_{t}s", "direction": "买涨", "price": up, "remaining": remain, "status": "pending"})
                        print(f"🔔 {now} | {c.upper()} | 0.75-0.85_{t}s | 买涨@{up:.2f} | 剩{remain}秒", flush=True)
                    # Down在0.75-0.85区间，买跌
                    if 0.75 < down < 0.85:
                        orders.append({"id": len(orders)+1, "time": now, "coin": c, "interval": i, "trend": f"0.75-0.85_{t}s", "direction": "买跌", "price": down, "remaining": remain, "status": "pending"})
                        print(f"🔔 {now} | {c.upper()} | 0.75-0.85_{t}s | 买跌@{down:.2f} | 剩{remain}秒", flush=True)
            
            # 策略2: 0.70-0.85 + 时间10s 5s 3s 2s
            for t in [10, 5, 3, 2]:
                if remain <= t:
                    # Up在0.70-0.85区间，买涨
                    if 0.70 < up < 0.85:
                        orders.append({"id": len(orders)+1, "time": now, "coin": c, "interval": i, "trend": f"0.70-0.85_{t}s", "direction": "买涨", "price": up, "remaining": remain, "status": "pending"})
                        print(f"🔔 {now} | {c.upper()} | 0.70-0.85_{t}s | 买涨@{up:.2f} | 剩{remain}秒", flush=True)
                    # Down在0.70-0.85区间，买跌
                    if 0.70 < down < 0.85:
                        orders.append({"id": len(orders)+1, "time": now, "coin": c, "interval": i, "trend": f"0.70-0.85_{t}s", "direction": "买跌", "price": down, "remaining": remain, "status": "pending"})
                        print(f"🔔 {now} | {c.upper()} | 0.70-0.85_{t}s | 买跌@{down:.2f} | 剩{remain}秒", flush=True)
            
            # 策略3: 0.90-0.995 反着买
            for t in [10, 5, 3, 2, 1.5]:
                if remain <= t:
                    # Up在0.90-0.995，买跌
                    if 0.90 <= up < 0.995:
                        orders.append({"id": len(orders)+1, "time": now, "coin": c, "interval": i, "trend": f"反买_0.90-0.995_{t}s", "direction": "买跌", "price": up, "remaining": remain, "status": "pending"})
                        print(f"🔔 {now} | {c.upper()} | 反买_0.90-0.995_{t}s | 买跌@{up:.2f} | 剩{remain}秒", flush=True)
                    # Down在0.90-0.995，买涨
                    if 0.90 <= down < 0.995:
                        orders.append({"id": len(orders)+1, "time": now, "coin": c, "interval": i, "trend": f"反买_0.90-0.995_{t}s", "direction": "买涨", "price": down, "remaining": remain, "status": "pending"})
                        print(f"🔔 {now} | {c.upper()} | 反买_0.90-0.995_{t}s | 买涨@{down:.2f} | 剩{remain}秒", flush=True)
            
            save_orders(orders)
        
        time.sleep(0.5)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}", flush=True)
        time.sleep(0.5)
