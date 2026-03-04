import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz

# === 1. 获取基础金融数据 (Yahoo Finance) ===
def get_yahoo_data():
    tickers = {
        "US10Y": "^TNX",      # 10年美债
        "DXY": "DX-Y.NYB",    # 美元指数
        "VIX": "^VIX",        # 恐慌指数
        "HYG": "HYG",         # 高收益债
        "USDCNH": "CNH=X",    # 离岸人民币
        "AH_PREMIUM": "HSCAHPI.HK" # 恒生AH股溢价指数 (如果获取失败会显示N/A)
    }
    
    data = {}
    for name, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            # 获取最新价
            price = stock.fast_info['last_price']
            # 获取昨收价 (用于计算涨跌)
            prev_close = stock.fast_info['previous_close']
            
            # 格式化
            if name == "US10Y":
                fmt_price = f"{price:.2f}%"
            else:
                fmt_price = f"{price:.2f}"
                
            data[name] = {
                "value": fmt_price,
                "trend": "🔴" if price > prev_close else "🟢" if price < prev_close else "⚪"
            }
        except:
            data[name] = {"value": "N/A", "trend": "⚪"}
    return data

# === 2. 获取加密货币数据 (CoinGecko & DefiLlama API) ===
def get_crypto_data():
    data = {}
    
    # 2.1 BTC.D (比特币市占率) - 使用 CoinGecko
    try:
        url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            market_cap_percentage = response.json()['data']['market_cap_percentage']['btc']
            data['BTC.D'] = f"{market_cap_percentage:.1f}%"
        else:
            data['BTC.D'] = "Link"
    except:
        data['BTC.D'] = "Link"

    # 2.2 稳定币总市值 - 使用 DefiLlama
    try:
        url = "https://stablecoins.llama.fi/stablecoins?includePrices=true"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            pegged_assets = response.json()['peggedAssets']
            total_mcap = sum(asset['circulating']['peggedUSD'] for asset in pegged_assets if asset['symbol'] in ['USDT', 'USDC', 'DAI', 'FDUSD'])
            data['STABLE_CAP'] = f"${total_mcap/1e9:.1f}B" # 转换为十亿美元
        else:
            data['STABLE_CAP'] = "Link"
    except:
        data['STABLE_CAP'] = "Link"
        
    return data

# === 3. 生成 HTML 表格 ===
def generate_html(y_data, c_data):
    beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
    
    # 定义超链接 (对于无法自动获取的数据)
    links = {
        "RRP": "https://www.newyorkfed.org/markets/desk-operations/reverse-repo",
        "MMFI": "https://www.tradingview.com/symbols/MMFI/",
        "USDT_PREMIUM": "https://www.feixiaohao.com/data/stable.html", # 指向币安P2P页面自行查看
        "NORTH_FUNDS": "https://data.eastmoney.com/hsgt/index.html", # 东方财富北向资金
        "BTC_D_LINK": "https://www.tradingview.com/symbols/BTC.D/",
        "STABLE_LINK": "https://defillama.com/stablecoins"
    }

    # 处理数据回退 (如果API失败，显示链接)
    btcd_val = c_data.get('BTC.D', 'Link')
    if btcd_val == "Link":
        btcd_display = f"<a href='{links['BTC_D_LINK']}' target='_blank'>查看</a>"
    else:
        btcd_display = btcd_val

    stable_val = c_data.get('STABLE_CAP', 'Link')
    if stable_val == "Link":
        stable_display = f"<a href='{links['STABLE_LINK']}' target='_blank'>查看</a>"
    else:
        stable_display = stable_val

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>极简金矿</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: -apple-system, system-ui, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow-x: auto; }}
            h1 {{ text-align: center; margin-bottom: 5px; color: #333; }}
            .time {{ text-align: center; color: #888; font-size: 0.9em; margin-bottom: 20px; }}
            
            table {{ width: 100%; border-collapse: collapse; min-width: 1000px; }}
            th {{ background: #f8f9fa; color: #444; font-weight: 600; padding: 15px 10px; border-bottom: 2px solid #eee; text-align: center; font-size: 0.9em; }}
            td {{ padding: 15px 10px; text-align: center; border-bottom: 1px solid #eee; font-size: 1.1em; font-weight: 500; }}
            
            /* 状态颜色 */
            .trend {{ font-size: 0.8em; margin-left: 5px; }}
            
            /* 链接样式 */
            a {{ color: #0066cc; text-decoration: none; font-weight: bold; font-size: 0.9em; border: 1px solid #cce5ff; padding: 4px 8px; border-radius: 4px; background: #f0f7ff; }}
            a:hover {{ background: #e0efff; }}

            /* 响应式优化 */
            @media (max-width: 768px) {{
                .container {{ padding: 10px; }}
                th, td {{ padding: 10px 5px; font-size: 0.9em; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⛏️ 极简金矿</h1>
            <div class="time">更新时间: {beijing_time}</div>
            
            <table>
                <thead>
                    <tr>
                        <th>US10Y<br><span style="font-size:0.8em;color:#999">美债</span></th>
                        <th>DXY<br><span style="font-size:0.8em;color:#999">美元</span></th>
                        <th>RRP<br><span style="font-size:0.8em;color:#999">逆回购</span></th>
                        <th>VIX<br><span style="font-size:0.8em;color:#999">恐慌</span></th>
                        <th>HYG<br><span style="font-size:0.8em;color:#999">垃圾债</span></th>
                        <th>MMFI<br><span style="font-size:0.8em;color:#999">宽度</span></th>
                        <th>BTC.D<br><span style="font-size:0.8em;color:#999">市占率</span></th>
                        <th>USDT溢价<br><span style="font-size:0.8em;color:#999">场外</span></th>
                        <th>稳定币市值<br><span style="font-size:0.8em;color:#999">流动性</span></th>
                        <th>北向资金<br><span style="font-size:0.8em;color:#999">外资</span></th>
                        <th>USD/CNH<br><span style="font-size:0.8em;color:#999">汇率</span></th>
                        <th>AH溢价<br><span style="font-size:0.8em;color:#999">估值</span></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{y_data['US10Y']['value']}<span class="trend">{y_data['US10Y']['trend']}</span></td>
                        <td>{y_data['DXY']['value']}<span class="trend">{y_data['DXY']['trend']}</span></td>
                        <td><a href="{links['RRP']}" target="_blank">查看</a></td>
                        <td>{y_data['VIX']['value']}<span class="trend">{y_data['VIX']['trend']}</span></td>
                        <td>{y_data['HYG']['value']}<span class="trend">{y_data['HYG']['trend']}</span></td>
                        <td><a href="{links['MMFI']}" target="_blank">查看</a></td>
                        <td>{btcd_display}</td>
                        <td><a href="{links['USDT_PREMIUM']}" target="_blank">查看</a></td>
                        <td>{stable_display}</td>
                        <td><a href="{links['NORTH_FUNDS']}" target="_blank">查看</a></td>
                        <td>{y_data['USDCNH']['value']}<span class="trend">{y_data['USDCNH']['trend']}</span></td>
                        <td>{y_data['AH_PREMIUM']['value']}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div style="text-align:center; margin-top:20px; color:#999; font-size:0.8em;">
            🔴 红色 = 上涨 | 🟢 绿色 = 下跌 (对于美债/VIX/DXY来说，红色往往是预警信号)
        </div>
    </body>
    </html>
    """
    return html

# === 主程序 ===
if __name__ == "__main__":
    print("正在挖掘数据...")
    y_data = get_yahoo_data()
    c_data = get_crypto_data()
    
    print("正在提炼金矿...")
    html = generate_html(y_data, c_data)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("金矿已生成！")
