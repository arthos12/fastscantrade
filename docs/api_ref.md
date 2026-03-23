# Polymarket API 参考文档

## 基础信息

- Base URL: `https://clob.polymarket.com`
- Market API: `https://polymarket.com/api/market`

## 接口列表

### 1. 获取服务器时间

```
GET /time
```

**响应:**
```json
{
  "clock": 1774231447
}
```

### 2. 获取市场信息

```
GET https://polymarket.com/api/market?slug={slug}
```

**Slug 格式:**
```
{coin}-updown-{interval}-{period}

例如:
- btc-updown-5m-1774231200
- eth-updown-5m-1774231200
- btc-updown-15m-1774231200
```

**周期计算:**
```python
# 5分钟周期
period = (timestamp // 300) * 300

# 15分钟周期
period = (timestamp // 900) * 900

# 1小时周期
period = (timestamp // 3600) * 3600
```

**响应:**
```json
{
  "closed": false,
  "clobTokenIds": [
    "1983727689725329802454924510332527708353933011449136766088074793852407328940",  // YES/UP token
    "14358520627259820377704892172571021679021596587155324463704326866455266133028"   // NO/DOWN token
  ]
}
```

### 3. 获取中间价格

```
GET /midpoint?token_id={token_id}
```

**响应:**
```json
{
  "mid": 0.95
}
```

### 4. 获取结算价（最后成交价）

```
GET /last-trade-price?token_id={token_id}
```

**响应:**
```json
{
  "price": 0.99
}
```

## Token ID 说明

每个市场有两个 outcome:
- 第一个是 YES/UP (预测上涨)
- 第二个是 NO/DOWN (预测下跌)

## 常用市场

| 市场 | Slug示例 |
|------|----------|
| BTC 5m | btc-updown-5m-{period} |
| ETH 5m | eth-updown-5m-{period} |
| BTC 15m | btc-updown-15m-{period} |
| SOL 5m | sol-updown-5m-{period} |

## 注意事项

1. API 有频率限制，避免高频请求
2. 部分接口需要 User-Agent header
3. 结算价需要等市场关闭后才能获取
