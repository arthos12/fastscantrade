#!/usr/bin/env python3
"""
订单存储模块
"""

import json
import os

class Storage:
    """订单存储"""
    
    def __init__(self, filepath="/root/.openclaw/workspace/pm_orders.json"):
        self.filepath = filepath
        self.orders = self.load()
    
    def load(self):
        """加载订单"""
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except:
            return []
    
    def save(self, order):
        """保存订单"""
        order['id'] = len(self.orders) + 1
        self.orders.append(order)
        
        with open(self.filepath, 'w') as f:
            json.dump(self.orders, f, indent=2)
