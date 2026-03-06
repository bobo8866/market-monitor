import yfinance as yf
import pandas as pd
import requests
import re
import os
from datetime import datetime
import pytz

HISTORY_FILE = "history.csv"

# === 1. 获取所有数据 ===
def get_all_data():
    tickers = {
        "US10Y": "^TNX", "DXY": "DX-Y.NYB", "VIX": "^VIX", "HYG": "HYG",
        "USDCNH": "CNH=X", "GOLD": "GC=F", "SILVER": "SI=F", "COPPER": "HG=F"
    }
    raw_data = {}
    
    # A. Yahoo
    for name, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info['last_price']
            prev = stock.fast_info['previous_close']
            if name == "US10Y": val_str = f"{price:.2f}%"
            else: val_str = f"{price:.2f}"
            
            raw_data[name] = {
                "value": val_str,
                "trend": "🔴" if price > prev else "🟢" if price < prev else "⚪"
            }
        except: 
            raw_data[name] = {"value": "Link", "trend": "⚪"}

    # --- 新增：中国国债 (CNBC 爬虫) ---
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get("https://www.cnbc.com/quotes/CN10Y", headers=headers, timeout=5)
        # 正则找价格: "last":"2.123"
        match = re.search(r'"last":"(\d+\.\d+)"', r.text)
        if match:
            price = float(match.group(1))
            raw_data['CN10Y'] = f"{price:.3f}%"
        else:
            raw_data['CN10Y'] = "Link"
    except:
        raw_data['CN10Y'] = "Link"

    # B. FRED
    try:
        df = pd.read_csv("https://fred.stlouisfed.org/graph/fredgraph.csv?id=WTREGEN")
        raw_data['TGA'] = f"${df.iloc[-1, 1]:.0f}B"
    except: raw_data['TGA'] = "Link"

    try:
        df = pd.read_csv("https://fred.stlouisfed.org/graph/fredgraph.csv?id=RRPONTSYD")
        raw_data['RRP'] = f"${df.iloc[-1, 1]:.0f}B"
    except: raw_data['RRP'] = "Link"

    # C. Crypto
    try:
        r = requests.get("https://api.coingecko.com/api/v3/global", timeout=10)
        btc_d = r.json()['data']['market_cap_percentage']['btc']
        raw_data['BTC.D'] = f"{btc_d:.1f}%"
    except: raw_data['BTC.D'] = "N/A"

    try:
        r = requests.get("https://stablecoins.llama.fi/stablecoins?includePrices=true", timeout=10)
        assets = r.json()['peggedAssets']
        total = sum(a['circulating']['peggedUSD'] for a in assets if a['symbol'] in ['USDT','USDC','DAI','FDUSD'])
        raw_data['STABLE_CAP'] = f"${total/1e9:.1f}B"
    except: raw_data['STABLE_CAP'] = "N/A"
    
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=10)
        item = r.json()['data'][0]
        raw_data['FEAR'] = f"{item['value']}"
    except: raw_data['FEAR'] = "N/A"

    return raw_data

# === 2. 更新历史 ===
def update_history(data):
    today = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
    
    def get_val(key):
        if key not in data: return ""
        val = data[key]['value'] if isinstance(data[key], dict) else data[key]
        return val if val != "N/A" and val != "Link" else ""

    new_row = {
        "日期": today,
        "US10Y": get_val('US10Y'),
        "CN10Y": data.get('CN10Y', "") if data.get('CN10Y') != "Link" else "", # 存入历史
        "DXY": get_val('DXY'),
        "RRP": get_val('RRP'),
        "VIX": get_val('VIX'),
        "HYG": get_val('HYG'),
        "黄金": get_val('GOLD'),
        "白银": get_val('SILVER'),
        "铜": get_val('COPPER'),
        "BTC.D": data['BTC.D'],
        "稳定币": data['STABLE_CAP'],
        "TGA": data['TGA'],
        "恐慌": data['FEAR'],
        "汇率": get_val('USDCNH')
    }
    
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        # 自动添加新列
        for col in new_row.keys():
            if col not in df.columns: df[col] = ""
        df = df[df["日期"] != today]
    else:
        df = pd.DataFrame(columns=new_row.keys())
    
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)
    df = df.sort_values(by="日期", ascending=False)
    df.to_csv(HISTORY_FILE, index=False, encoding="utf-8-sig")
    return df

# === 3. 生成 HTML ===
def generate_html(current_data, history_df):
    beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
    history_html = history_df.head(60).to_html(index=False, classes="history-table", border=0)
    
    links = {
        "CN10Y": "https://cn.investing.com/rates-bonds/china-10-year-bond-yield",
        "RRP": "https://www.newyorkfed.org/markets/desk-operations/reverse-repo",
        "TGA": "https://fred.stlouisfed.org/series/WTREGEN",
        "USDT": "https://www.feixiaohao.com/data/stable"
    }

    def cell(val, link=None, label="查看"):
        if isinstance(val, dict): val = val['value']
        if val == "N/A" or val == "Link" or val == "": 
            target = link if link else "#"
            return f"<a href='{target}' target='_blank' class='btn'>{label}</a>"
        return f"<a href='{link if link else '#'}' target='_blank' class='val-link'>{val}</a>"

    # CN10Y 显示逻辑
    cn10y_val = current_data.get('CN10Y', "Link")
    cn10y_cell = cell(cn10y_val, links['CN10Y'])

    # RRP 显示逻辑
    rrp_val = current_data.get('RRP', 'Link')
    rrp_cell = cell(rrp_val, links['RRP'])

    # TGA 显示逻辑
    tga_val = current_data.get('TGA', 'Link')
    tga_cell = cell(tga_val, links['TGA'])

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>秘密档案馆</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; margin:0; padding:15px; background:#f0f2f5; }}
            .container {{ max-width: 1200px; margin:0 auto; }}
            h1 {{ text-align:center; color:#333; margin-bottom:5px; }}
            .time {{ text-align:center; color:#888; font-size:0.9em; margin-bottom:20px; }}
            .card {{ background:white; padding:15px; border-radius:10px; margin-bottom:20px; box-shadow:0 2px 5px rgba(0,0,0,0.05); }}
            
            table {{ width:100%; border-collapse:collapse; min-width:900px; white-space:nowrap; }}
            th {{ background:#333; color:white; padding:10px; text-align:center; font-size:0.9em; }}
            td {{ padding:10px; text-align:center; font-weight:bold; border-bottom:1px solid #eee; }}
            tr:nth-child(even) {{ background-color:#f9f9f9; }}
            
            .trend {{ font-size:0.7em; margin-left:3px; }}
            .btn {{ background:#eef; color:#0066cc; padding:2px 8px; border-radius:4px; text-decoration:none; font-size:0.9em; border:1px solid #cce5ff; }}
            .val-link {{ color:#333; text-decoration:none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📂 每日金融档案</h1>
            <div class="time">更新时间: {beijing_time}</div>
            
            <div class="card">
                <h2>⚡ 实时快照</h2>
                <div style="overflow-x:auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>US10Y<br>美债</th>
                                <th>CN10Y<br>中债</th>
                                <th>DXY<br>美元</th>
                                <th>RRP<br>逆回购</th>
                                <th>VIX<br>恐慌</th>
                                <th>HYG<br>垃圾债</th>
                                <th>黄金</th><th>白银</th><th>铜</th>
                                <th>BTC.D</th><th>稳定币</th><th>TGA</th><th>恐慌</th><th>汇率</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{current_data['US10Y']['value']}<span class="trend">{current_data['US10Y']['trend']}</span></td>
                                <td>{cn10y_cell}</td>
                                <td>{current_data['DXY']['value']}<span class="trend">{current_data['DXY']['trend']}</span></td>
                                <td>{rrp_cell}</td>
                                <td>{current_data['VIX']['value']}<span class="trend">{current_data['VIX']['trend']}</span></td>
                                <td>{current_data['HYG']['value']}<span class="trend">{current_data['HYG']['trend']}</span></td>
                                <td>{current_data['GOLD']['value']}<span class="trend">{current_data['GOLD']['trend']}</span></td>
                                <td>{current_data['SILVER']['value']}<span class="trend">{current_data['SILVER']['trend']}</span></td>
                                <td>{current_data['COPPER']['value']}<span class="trend">{current_data['COPPER']['trend']}</span></td>
                                <td>{current_data['BTC.D']}</td>
                                <td>{current_data['STABLE_CAP']}</td>
                                <td>{tga_cell}</td>
                                <td>{current_data['FEAR']}</td>
                                <td>{current_data['USDCNH']['value']}<span class="trend">{current_data['USDCNH']['trend']}</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="card">
                <h2>📜 历史数据</h2>
                <div style="overflow-x:auto;">
                    {history_html}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    print("开始归档...")
    data = get_all_data()
    df = update_history(data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generate_html(data, df))
    print("完成")
