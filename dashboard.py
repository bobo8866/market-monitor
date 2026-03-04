import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz

# === 1. 获取基础金融数据 (Yahoo Finance) ===
def get_yahoo_data():
    tickers = {
        "US10Y": "^TNX",      
        "DXY": "DX-Y.NYB",    
        "VIX": "^VIX",        
        "HYG": "HYG",         
        "USDCNH": "CNH=X",    
        "AH_PREMIUM": "HSCAHPI.HK" 
    }
    
    data = {}
    for name, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info['last_price']
            prev_close = stock.fast_info['previous_close']
            
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

# === 2. 获取加密货币数据 ===
def get_crypto_data():
    data = {}
    
    # BTC.D
    try:
        url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            val = response.json()['data']['market_cap_percentage']['btc']
            data['BTC.D'] = f"{val:.1f}%"
        else:
            data['BTC.D'] = "Link"
    except:
        data['BTC.D'] = "Link"

    # 稳定币市值
    try:
        url = "https://stablecoins.llama.fi/stablecoins?includePrices=true"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            pegged_assets = response.json()['peggedAssets']
            total = sum(asset['circulating']['peggedUSD'] for asset in pegged_assets if asset['symbol'] in ['USDT', 'USDC', 'DAI', 'FDUSD'])
            data['STABLE_CAP'] = f"${total/1e9:.1f}B"
        else:
            data['STABLE_CAP'] = "Link"
    except:
        data['STABLE_CAP'] = "Link"
        
    return data

# === 3. 生成 HTML (含武器库) ===
def generate_html(y_data, c_data):
    beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
    
    # --- 核心指标链接 ---
    links = {
        "RRP": "https://www.newyorkfed.org/markets/desk-operations/reverse-repo",
        "MMFI": "https://www.tradingview.com/symbols/MMFI/",
        "USDT_PREMIUM": "import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz

# === 1. 获取基础金融数据 (Yahoo Finance) ===
def get_yahoo_data():
    tickers = {
        "US10Y": "^TNX",      
        "DXY": "DX-Y.NYB",    
        "VIX": "^VIX",        
        "HYG": "HYG",         
        "USDCNH": "CNH=X",    
        "AH_PREMIUM": "HSCAHPI.HK" 
    }
    
    data = {}
    for name, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info['last_price']
            prev_close = stock.fast_info['previous_close']
            
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

# === 2. 获取加密货币数据 ===
def get_crypto_data():
    data = {}
    
    # BTC.D
    try:
        url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            val = response.json()['data']['market_cap_percentage']['btc']
            data['BTC.D'] = f"{val:.1f}%"
        else:
            data['BTC.D'] = "Link"
    except:
        data['BTC.D'] = "Link"

    # 稳定币市值
    try:
        url = "https://stablecoins.llama.fi/stablecoins?includePrices=true"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            pegged_assets = response.json()['peggedAssets']
            total = sum(asset['circulating']['peggedUSD'] for asset in pegged_assets if asset['symbol'] in ['USDT', 'USDC', 'DAI', 'FDUSD'])
            data['STABLE_CAP'] = f"${total/1e9:.1f}B"
        else:
            data['STABLE_CAP'] = "Link"
    except:
        data['STABLE_CAP'] = "Link"
        
    return data

# === 3. 生成 HTML (含武器库) ===
def generate_html(y_data, c_data):
    beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
    
    # --- 核心指标链接 ---
    links = {
        "RRP": "https://www.newyorkfed.org/markets/desk-operations/reverse-repo",
        "MMFI": "https://www.tradingview.com/symbols/MMFI/",
        "USDT_PREMIUM": "import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz

# === 1. 获取基础金融数据 (Yahoo Finance) ===
def get_yahoo_data():
    tickers = {
        "US10Y": "^TNX",      
        "DXY": "DX-Y.NYB",    
        "VIX": "^VIX",        
        "HYG": "HYG",         
        "USDCNH": "CNH=X",    
        "AH_PREMIUM": "HSCAHPI.HK" 
    }
    
    data = {}
    for name, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info['last_price']
            prev_close = stock.fast_info['previous_close']
            
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

# === 2. 获取加密货币数据 ===
def get_crypto_data():
    data = {}
    
    # BTC.D
    try:
        url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            val = response.json()['data']['market_cap_percentage']['btc']
            data['BTC.D'] = f"{val:.1f}%"
        else:
            data['BTC.D'] = "Link"
    except:
        data['BTC.D'] = "Link"

    # 稳定币市值
    try:
        url = "https://stablecoins.llama.fi/stablecoins?includePrices=true"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            pegged_assets = response.json()['peggedAssets']
            total = sum(asset['circulating']['peggedUSD'] for asset in pegged_assets if asset['symbol'] in ['USDT', 'USDC', 'DAI', 'FDUSD'])
            data['STABLE_CAP'] = f"${total/1e9:.1f}B"
        else:
            data['STABLE_CAP'] = "Link"
    except:
        data['STABLE_CAP'] = "Link"
        
    return data

# === 3. 生成 HTML (含武器库) ===
def generate_html(y_data, c_data):
    beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
    
    # --- 核心指标链接 ---
    links = {
        "RRP": "https://www.newyorkfed.org/markets/desk-operations/reverse-repo",
        "MMFI": "https://www.tradingview.com/symbols/MMFI/",
        "USDT_PREMIUM": "https://www.feixiaohao.com/data/stable", 
        "NORTH_FUNDS": "https://data.eastmoney.com/hsgt/index.html",
        "BTC_D_LINK": "https://www.tradingview.com/symbols/BTC.D/",
        "STABLE_LINK": "https://defillama.com/stablecoins",
        "AH_LINK": "https://quote.eastmoney.com/gb/zsHSAHP.html"
    }

    # --- 你的私人武器库 (Arsenal) ---
    arsenal = {
        "📊 短手成本 (STH)": "https://www.coinglass.com/pro/i/short-term-holder-price",
        "🇺🇸 贝莱德 BTC": "https://www.coinglass.com/zh/bitcoin-etf",
        "🔷 贝莱德 ETH": "https://www.coinglass.com/zh/eth-etf",
        "⛽ Gas 费率": "https://mct.xyz/gasnow",
        "🌊 稳定币流向": "https://cryptoquant.com/asset/stablecoin/chart/exchange-flows/exchange-netflow-total?exchange=all_exchange&window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=column",
        "📥 稳定币流入": "https://cryptoquant.com/asset/stablecoin/chart/exchange-flows/exchange-inflow-total?exchange=all_exchange&window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=column",
        "😨 贪婪恐惧": "https://www.coinglass.com/zh/pro/i/FearGreedIndex",
        "🏦 TGA 余额": "https://fred.stlouisfed.org/series/WTREGEN",
        "📈 MVRV 逃顶": "https://www.bitcoinmagazinepro.com/charts/mvrv-zscore/",
        "🎯 Ahr999 抄底": "https://9992100.xyz/",
        "🍕 披萨指数": "https://www.pizzint.watch/"
    }

    # 处理显示逻辑
    btcd_val = c_data.get('BTC.D', 'Link')
    btcd_display = f"<a href='{links['BTC_D_LINK']}' target='_blank'>查看</a>" if btcd_val == "Link" else btcd_val

    stable_val = c_data.get('STABLE_CAP', 'Link')
    stable_display = f"<a href='{links['STABLE_LINK']}' target='_blank'>查看</a>" if stable_val == "Link" else stable_val

    ah_display = f"<a href='{links['AH_LINK']}' target='_blank'>点击查看</a>"

    # 生成武器库按钮 HTML
    arsenal_html = ""
    for name, url in arsenal.items():
        arsenal_html += f"""<a href="{url}" target="_blank" class="arsenal-btn">{name}</a>"""

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>金融核武库</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: -apple-system, system-ui, sans-serif; margin: 0; padding: 20px; background: #f0f2f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            
            /* 卡片样式 */
            .card {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }}
            
            h1 {{ text-align: center; margin-bottom: 5px; color: #1a1a1a; }}
            h2 {{ font-size: 1.2em; color: #444; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 0; }}
            .time {{ text-align: center; color: #888; font-size: 0.9em; margin-bottom: 20px; }}
            
            /* 表格样式 */
            .table-box {{ overflow-x: auto; }}
            table {{ width: 100%; border-collapse: collapse; min-width: 1000px; }}
            th {{ background: #f8f9fa; color: #444; font-weight: 600; padding: 15px 10px; border-bottom: 2px solid #eee; text-align: center; font-size: 0.9em; }}
            td {{ padding: 15px 10px; text-align: center; border-bottom: 1px solid #eee; font-size: 1.1em; font-weight: 500; }}
            .trend {{ font-size: 0.8em; margin-left: 5px; }}
            
            /* 链接按钮 */
            .link-btn {{ color: #0066cc; text-decoration: none; font-weight: bold; font-size: 0.9em; border: 1px solid #cce5ff; padding: 4px 8px; border-radius: 4px; background: #f0f7ff; }}
            .link-btn:hover {{ background: #e0efff; }}

            /* 武器库网格 */
            .arsenal-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; margin-top: 15px; }}
            .arsenal-btn {{ 
                display: block; text-align: center; text-decoration: none; 
                background: #333; color: white; padding: 12px 5px; border-radius: 8px; 
                font-size: 0.9em; transition: transform 0.2s; 
            }}
            .arsenal-btn:hover {{ transform: translateY(-2px); background: #000; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>☢️ 金融核武库</h1>
            <div class="time">更新时间: {beijing_time}</div>
            
            <!-- 核心数据看板 -->
            <div class="card">
                <h2>📊 核心宏观指标</h2>
                <div class="table-box">
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
                                <td><a href="{links['RRP']}" target="_blank" class="link-btn">查看</a></td>
                                <td>{y_data['VIX']['value']}<span class="trend">{y_data['VIX']['trend']}</span></td>
                                <td>{y_data['HYG']['value']}<span class="trend">{y_data['HYG']['trend']}</span></td>
                                <td><a href="{links['MMFI']}" target="_blank" class="link-btn">查看</a></td>
                                <td>{btcd_display}</td>
                                <td><a href="{links['USDT_PREMIUM']}" target="_blank" class="link-btn">查看</a></td>
                                <td>{stable_display}</td>
                                <td><a href="{links['NORTH_FUNDS']}" target="_blank" class="link-btn">查看</a></td>
                                <td>{y_data['USDCNH']['value']}<span class="trend">{y_data['USDCNH']['trend']}</span></td>
                                <td>{ah_display}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 深度分析工具箱 -->
            <div class="card">
                <h2>🛠️ 深度战术工具箱</h2>
                <div class="arsenal-grid">
                    {arsenal_html}
                </div>
            </div>
            
            <div style="text-align:center; color:#999; font-size:0.8em; margin-bottom:20px;">
                Designed for Alpha Hunters
            </div>
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
    html = generate_html(y_data, c_data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("更新完成")", 
        "NORTH_FUNDS": "https://data.eastmoney.com/hsgt/index.html",
        "BTC_D_LINK": "https://www.tradingview.com/symbols/BTC.D/",
        "STABLE_LINK": "https://defillama.com/stablecoins",
        "AH_LINK": "https://quote.eastmoney.com/gb/zsHSAHP.html"
    }

    # --- 你的私人武器库 (Arsenal) ---
    arsenal = {
        "📊 短手成本 (STH)": "https://www.coinglass.com/pro/i/short-term-holder-price",
        "🇺🇸 贝莱德 BTC": "https://www.coinglass.com/zh/bitcoin-etf",
        "🔷 贝莱德 ETH": "https://www.coinglass.com/zh/eth-etf",
        "⛽ Gas 费率": "https://mct.xyz/gasnow",
        "🌊 稳定币流向": "https://cryptoquant.com/asset/stablecoin/chart/exchange-flows/exchange-netflow-total?exchange=all_exchange&window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=column",
        "📥 稳定币流入": "https://cryptoquant.com/asset/stablecoin/chart/exchange-flows/exchange-inflow-total?exchange=all_exchange&window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=column",
        "😨 贪婪恐惧": "https://www.coinglass.com/zh/pro/i/FearGreedIndex",
        "🏦 TGA 余额": "https://fred.stlouisfed.org/series/WTREGEN",
        "📈 MVRV 逃顶": "https://www.bitcoinmagazinepro.com/charts/mvrv-zscore/",
        "🎯 Ahr999 抄底": "https://9992100.xyz/",
        "🍕 披萨指数": "https://www.pizzint.watch/"
    }

    # 处理显示逻辑
    btcd_val = c_data.get('BTC.D', 'Link')
    btcd_display = f"<a href='{links['BTC_D_LINK']}' target='_blank'>查看</a>" if btcd_val == "Link" else btcd_val

    stable_val = c_data.get('STABLE_CAP', 'Link')
    stable_display = f"<a href='{links['STABLE_LINK']}' target='_blank'>查看</a>" if stable_val == "Link" else stable_val

    ah_display = f"<a href='{links['AH_LINK']}' target='_blank'>点击查看</a>"

    # 生成武器库按钮 HTML
    arsenal_html = ""
    for name, url in arsenal.items():
        arsenal_html += f"""<a href="{url}" target="_blank" class="arsenal-btn">{name}</a>"""

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>金融核武库</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: -apple-system, system-ui, sans-serif; margin: 0; padding: 20px; background: #f0f2f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            
            /* 卡片样式 */
            .card {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }}
            
            h1 {{ text-align: center; margin-bottom: 5px; color: #1a1a1a; }}
            h2 {{ font-size: 1.2em; color: #444; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 0; }}
            .time {{ text-align: center; color: #888; font-size: 0.9em; margin-bottom: 20px; }}
            
            /* 表格样式 */
            .table-box {{ overflow-x: auto; }}
            table {{ width: 100%; border-collapse: collapse; min-width: 1000px; }}
            th {{ background: #f8f9fa; color: #444; font-weight: 600; padding: 15px 10px; border-bottom: 2px solid #eee; text-align: center; font-size: 0.9em; }}
            td {{ padding: 15px 10px; text-align: center; border-bottom: 1px solid #eee; font-size: 1.1em; font-weight: 500; }}
            .trend {{ font-size: 0.8em; margin-left: 5px; }}
            
            /* 链接按钮 */
            .link-btn {{ color: #0066cc; text-decoration: none; font-weight: bold; font-size: 0.9em; border: 1px solid #cce5ff; padding: 4px 8px; border-radius: 4px; background: #f0f7ff; }}
            .link-btn:hover {{ background: #e0efff; }}

            /* 武器库网格 */
            .arsenal-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; margin-top: 15px; }}
            .arsenal-btn {{ 
                display: block; text-align: center; text-decoration: none; 
                background: #333; color: white; padding: 12px 5px; border-radius: 8px; 
                font-size: 0.9em; transition: transform 0.2s; 
            }}
            .arsenal-btn:hover {{ transform: translateY(-2px); background: #000; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>☢️ 金融核武库</h1>
            <div class="time">更新时间: {beijing_time}</div>
            
            <!-- 核心数据看板 -->
            <div class="card">
                <h2>📊 核心宏观指标</h2>
                <div class="table-box">
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
                                <td><a href="{links['RRP']}" target="_blank" class="link-btn">查看</a></td>
                                <td>{y_data['VIX']['value']}<span class="trend">{y_data['VIX']['trend']}</span></td>
                                <td>{y_data['HYG']['value']}<span class="trend">{y_data['HYG']['trend']}</span></td>
                                <td><a href="{links['MMFI']}" target="_blank" class="link-btn">查看</a></td>
                                <td>{btcd_display}</td>
                                <td><a href="{links['USDT_PREMIUM']}" target="_blank" class="link-btn">查看</a></td>
                                <td>{stable_display}</td>
                                <td><a href="{links['NORTH_FUNDS']}" target="_blank" class="link-btn">查看</a></td>
                                <td>{y_data['USDCNH']['value']}<span class="trend">{y_data['USDCNH']['trend']}</span></td>
                                <td>{ah_display}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 深度分析工具箱 -->
            <div class="card">
                <h2>🛠️ 深度战术工具箱</h2>
                <div class="arsenal-grid">
                    {arsenal_html}
                </div>
            </div>
            
            <div style="text-align:center; color:#999; font-size:0.8em; margin-bottom:20px;">
                Designed for Alpha Hunters
            </div>
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
    html = generate_html(y_data, c_data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("更新完成")", 
        "NORTH_FUNDS": "https://data.eastmoney.com/hsgt/index.html",
        "BTC_D_LINK": "https://www.tradingview.com/symbols/BTC.D/",
        "STABLE_LINK": "https://defillama.com/stablecoins",
        "AH_LINK": "https://quote.eastmoney.com/gb/zsHSAHP.html"
    }

    # --- 你的私人武器库 (Arsenal) ---
    arsenal = {
        "📊 短手成本 (STH)": "https://www.coinglass.com/pro/i/short-term-holder-price",
        "🇺🇸 贝莱德 BTC": "https://www.coinglass.com/zh/bitcoin-etf",
        "🔷 贝莱德 ETH": "https://www.coinglass.com/zh/eth-etf",
        "⛽ Gas 费率": "https://mct.xyz/gasnow",
        "🌊 稳定币流向": "https://cryptoquant.com/asset/stablecoin/chart/exchange-flows/exchange-netflow-total?exchange=all_exchange&window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=column",
        "📥 稳定币流入": "https://cryptoquant.com/asset/stablecoin/chart/exchange-flows/exchange-inflow-total?exchange=all_exchange&window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=column",
        "😨 贪婪恐惧": "https://www.coinglass.com/zh/pro/i/FearGreedIndex",
        "🏦 TGA 余额": "https://fred.stlouisfed.org/series/WTREGEN",
        "📈 MVRV 逃顶": "https://www.bitcoinmagazinepro.com/charts/mvrv-zscore/",
        "🎯 Ahr999 抄底": "https://9992100.xyz/",
        "🍕 披萨指数": "https://www.pizzint.watch/"
    }

    # 处理显示逻辑
    btcd_val = c_data.get('BTC.D', 'Link')
    btcd_display = f"<a href='{links['BTC_D_LINK']}' target='_blank'>查看</a>" if btcd_val == "Link" else btcd_val

    stable_val = c_data.get('STABLE_CAP', 'Link')
    stable_display = f"<a href='{links['STABLE_LINK']}' target='_blank'>查看</a>" if stable_val == "Link" else stable_val

    ah_display = f"<a href='{links['AH_LINK']}' target='_blank'>点击查看</a>"

    # 生成武器库按钮 HTML
    arsenal_html = ""
    for name, url in arsenal.items():
        arsenal_html += f"""<a href="{url}" target="_blank" class="arsenal-btn">{name}</a>"""

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>金融核武库</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: -apple-system, system-ui, sans-serif; margin: 0; padding: 20px; background: #f0f2f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            
            /* 卡片样式 */
            .card {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }}
            
            h1 {{ text-align: center; margin-bottom: 5px; color: #1a1a1a; }}
            h2 {{ font-size: 1.2em; color: #444; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 0; }}
            .time {{ text-align: center; color: #888; font-size: 0.9em; margin-bottom: 20px; }}
            
            /* 表格样式 */
            .table-box {{ overflow-x: auto; }}
            table {{ width: 100%; border-collapse: collapse; min-width: 1000px; }}
            th {{ background: #f8f9fa; color: #444; font-weight: 600; padding: 15px 10px; border-bottom: 2px solid #eee; text-align: center; font-size: 0.9em; }}
            td {{ padding: 15px 10px; text-align: center; border-bottom: 1px solid #eee; font-size: 1.1em; font-weight: 500; }}
            .trend {{ font-size: 0.8em; margin-left: 5px; }}
            
            /* 链接按钮 */
            .link-btn {{ color: #0066cc; text-decoration: none; font-weight: bold; font-size: 0.9em; border: 1px solid #cce5ff; padding: 4px 8px; border-radius: 4px; background: #f0f7ff; }}
            .link-btn:hover {{ background: #e0efff; }}

            /* 武器库网格 */
            .arsenal-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; margin-top: 15px; }}
            .arsenal-btn {{ 
                display: block; text-align: center; text-decoration: none; 
                background: #333; color: white; padding: 12px 5px; border-radius: 8px; 
                font-size: 0.9em; transition: transform 0.2s; 
            }}
            .arsenal-btn:hover {{ transform: translateY(-2px); background: #000; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>☢️ 金融核武库</h1>
            <div class="time">更新时间: {beijing_time}</div>
            
            <!-- 核心数据看板 -->
            <div class="card">
                <h2>📊 核心宏观指标</h2>
                <div class="table-box">
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
                                <td><a href="{links['RRP']}" target="_blank" class="link-btn">查看</a></td>
                                <td>{y_data['VIX']['value']}<span class="trend">{y_data['VIX']['trend']}</span></td>
                                <td>{y_data['HYG']['value']}<span class="trend">{y_data['HYG']['trend']}</span></td>
                                <td><a href="{links['MMFI']}" target="_blank" class="link-btn">查看</a></td>
                                <td>{btcd_display}</td>
                                <td><a href="{links['USDT_PREMIUM']}" target="_blank" class="link-btn">查看</a></td>
                                <td>{stable_display}</td>
                                <td><a href="{links['NORTH_FUNDS']}" target="_blank" class="link-btn">查看</a></td>
                                <td>{y_data['USDCNH']['value']}<span class="trend">{y_data['USDCNH']['trend']}</span></td>
                                <td>{ah_display}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 深度分析工具箱 -->
            <div class="card">
                <h2>🛠️ 深度战术工具箱</h2>
                <div class="arsenal-grid">
                    {arsenal_html}
                </div>
            </div>
            
            <div style="text-align:center; color:#999; font-size:0.8em; margin-bottom:20px;">
                Designed for Alpha Hunters
            </div>
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
    html = generate_html(y_data, c_data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("更新完成")
