import yfinance as yf
import pandas as pd
import requests
import io
from datetime import datetime
import pytz

# === 1. 获取基础金融数据 ===
def get_yahoo_data():
    tickers = {
        "US10Y": "^TNX",      
        "DXY": "DX-Y.NYB",    
        "VIX": "^VIX",        
        "HYG": "HYG",         
        "USDCNH": "CNH=X",
        "GOLD": "GC=F",       
        "SILVER": "SI=F",     
        "COPPER": "HG=F",     
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

# === 2. 获取战术数据 ===
def get_tactical_data():
    data = {}
    
    # BTC.D
    try:
        url = "https://api.coingecko.com/api/v3/global"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            val = r.json()['data']['market_cap_percentage']['btc']
            data['BTC.D'] = f"{val:.1f}%"
        else: data['BTC.D'] = "Link"
    except: data['BTC.D'] = "Link"

    # 稳定币市值
    try:
        url = "https://stablecoins.llama.fi/stablecoins?includePrices=true"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            assets = r.json()['peggedAssets']
            total = sum(a['circulating']['peggedUSD'] for a in assets if a['symbol'] in ['USDT','USDC','DAI','FDUSD'])
            data['STABLE_CAP'] = f"${total/1e9:.1f}B"
        else: data['STABLE_CAP'] = "Link"
    except: data['STABLE_CAP'] = "Link"

    # 贪婪恐慌
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=10)
        if r.status_code == 200:
            item = r.json()['data'][0]
            data['FEAR_GREED'] = f"{item['value']} ({item['value_classification']})"
        else: data['FEAR_GREED'] = "Link"
    except: data['FEAR_GREED'] = "Link"

    # ETH Gas
    try:
        r = requests.get("https://beaconcha.in/api/v1/execution/gasnow", timeout=10)
        if r.status_code == 200:
            rapid = r.json()['data']['rapid']
            gas_val = int(rapid / 1000000000)
            data['GAS'] = f"{gas_val} Gwei"
        else: data['GAS'] = "Link"
    except: data['GAS'] = "Link"

    # TGA
    try:
        csv_url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=WTREGEN"
        df = pd.read_csv(csv_url)
        last_val = df.iloc[-1, 1]
        data['TGA'] = f"${last_val:.0f}B"
    except: data['TGA'] = "Link"

    return data

# === 3. 生成 HTML ===
def generate_html(y_data, t_data):
    beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
    
    links = {
        "RRP": "https://www.newyorkfed.org/markets/desk-operations/reverse-repo",
        "MMFI": "https://www.tradingview.com/symbols/MMFI/",
        "USDT": "https://www.feixiaohao.com/data/stable",
        "NORTH": "https://data.eastmoney.com/hsgt/index.html",
        "BTC_D_LINK": "https://www.tradingview.com/symbols/BTC.D/",
        "STABLE_LINK": "https://defillama.com/stablecoins",
        "AH_LINK": "https://quote.eastmoney.com/gb/zsHSAHP.html",
        
        "STH": "https://www.coinglass.com/pro/i/short-term-holder-price",
        "BLK_BTC": "https://www.coinglass.com/zh/bitcoin-etf",
        "BLK_ETH": "https://www.coinglass.com/zh/eth-etf",
        "GAS": "https://mct.xyz/gasnow",
        "STABLE_FLOW": "https://cryptoquant.com/asset/stablecoin/chart/exchange-flows/exchange-netflow-total?exchange=all_exchange&window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=column",
        "FG": "https://www.coinglass.com/zh/pro/i/FearGreedIndex",
        "TGA": "https://fred.stlouisfed.org/series/WTREGEN",
        "MVRV": "https://www.bitcoinmagazinepro.com/charts/mvrv-zscore/",
        "AHR999": "https://9992100.xyz/",
        "PIZZA": "https://www.pizzint.watch/",
        "FUNDING": "https://www.coinglass.com/zh/FundingRate",
        "CB_PREM": "https://www.coinglass.com/zh/pro/i/CoinbasePremiumIndex", # <--- Coinbase 溢价
        "CME_OI": "https://www.coinglass.com/zh/BitcoinOpenInterest"        # <--- CME 持仓
    }

    def cell(val, link, label="查看"):
        if val == "Link" or val == "N/A":
            return f"<a href='{link}' target='_blank' class='btn'>{label}</a>"
        else:
            return f"<a href='{link}' target='_blank' class='val-link'>{val}</a>"

    ah_val = y_data['AH_PREMIUM']['value']
    ah_cell = cell(ah_val, links['AH_LINK']) if ah_val != "N/A" else cell("Link", links['AH_LINK'])

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>金融核武库</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: -apple-system, system-ui, sans-serif; margin: 0; padding: 15px; background: #f0f2f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            h1 {{ text-align: center; color: #1a1a1a; margin-bottom: 5px; }}
            .time {{ text-align: center; color: #888; font-size: 0.85em; margin-bottom: 20px; }}
            .card {{ background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px; }}
            h2 {{ font-size: 1.1em; color: #444; border-left: 4px solid #0066cc; padding-left: 10px; margin: 0 0 15px 0; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th {{ font-size: 0.85em; color: #666; font-weight: normal; padding: 8px 5px; border-bottom: 1px solid #eee; }}
            td {{ padding: 10px 5px; text-align: center; border-bottom: 1px solid #f5f5f5; font-size: 1em; font-weight: 500; }}
            .trend {{ font-size: 0.7em; margin-left: 3px; }}
            .btn {{ display: inline-block; background: #f0f7ff; color: #0066cc; padding: 4px 10px; border-radius: 4px; text-decoration: none; font-size: 0.9em; border: 1px solid #cce5ff; }}
            .btn:hover {{ background: #0066cc; color: white; }}
            .val-link {{ color: #333; text-decoration: none; border-bottom: 1px dotted #ccc; }}
            .val-link:hover {{ color: #0066cc; border-bottom: 1px solid #0066cc; }}
            .grid-box {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; }}
            .grid-item {{ background: #fafafa; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #eee; }}
            .grid-label {{ display: block; font-size: 0.8em; color: #888; margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>☢️ 金融核武库</h1>
            <div class="time">更新时间: {beijing_time}</div>
            
            <div class="card">
                <h2>⛏️ 极简金矿 (宏观定调)</h2>
                <div style="overflow-x: auto;">
                    <table style="min-width: 800px;">
                        <thead>
                            <tr>
                                <th>US10Y<br>美债</th>
                                <th>DXY<br>美元</th>
                                <th>RRP<br>逆回购</th>
                                <th>VIX<br>恐慌</th>
                                <th>HYG<br>垃圾债</th>
                                <th>黄金<br>避险</th>
                                <th>白银<br>投机</th>
                                <th>铜<br>复苏</th>
                                <th>BTC.D<br>市占率</th>
                                <th>USDT溢价<br>场外</th>
                                <th>USD/CNH<br>汇率</th>
                                <th>AH溢价<br>估值</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{y_data['US10Y']['value']}<span class="trend">{y_data['US10Y']['trend']}</span></td>
                                <td>{y_data['DXY']['value']}<span class="trend">{y_data['DXY']['trend']}</span></td>
                                <td>{cell("Link", links['RRP'])}</td>
                                <td>{y_data['VIX']['value']}<span class="trend">{y_data['VIX']['trend']}</span></td>
                                <td>{y_data['HYG']['value']}<span class="trend">{y_data['HYG']['trend']}</span></td>
                                <td>{y_data['GOLD']['value']}<span class="trend">{y_data['GOLD']['trend']}</span></td>
                                <td>{y_data['SILVER']['value']}<span class="trend">{y_data['SILVER']['trend']}</span></td>
                                <td>{y_data['COPPER']['value']}<span class="trend">{y_data['COPPER']['trend']}</span></td>
                                <td>{cell(t_data['BTC.D'], links['BTC_D_LINK'])}</td>
                                <td>{cell("Link", links['USDT_PREMIUM'])}</td>
                                <td>{y_data['USDCNH']['value']}<span class="trend">{y_data['USDCNH']['trend']}</span></td>
                                <td>{ah_cell}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="card">
                <h2>⚔️ 战术数据 (实战信号)</h2>
                <div class="grid-box">
                    <div class="grid-item">
                        <span class="grid-label">稳定币市值</span>
                        {cell(t_data['STABLE_CAP'], links['STABLE_LINK'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">TGA 余额</span>
                        {cell(t_data['TGA'], links['TGA'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">贪婪恐慌</span>
                        {cell(t_data['FEAR_GREED'], links['FG'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">ETH Gas</span>
                        {cell(t_data['GAS'], links['GAS'])}
                    </div>
                    
                    <!-- 新增 -->
                    <div class="grid-item">
                        <span class="grid-label">Coinbase溢价</span>
                        {cell("Link", links['CB_PREM'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">CME持仓</span>
                        {cell("Link", links['CME_OI'])}
                    </div>
                    
                    <div class="grid-item">
                        <span class="grid-label">资金费率</span>
                        {cell("Link", links['FUNDING'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">北向资金</span>
                        {cell("Link", links['NORTH_FUNDS'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">贝莱德 BTC</span>
                        {cell("Link", links['BLK_BTC'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">贝莱德 ETH</span>
                        {cell("Link", links['BLK_ETH'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">短手成本</span>
                        {cell("Link", links['STH'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">稳定币流向</span>
                        {cell("Link", links['STABLE_FLOW'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">MMFI 宽度</span>
                        {cell("Link", links['MMFI'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">MVRV 逃顶</span>
                        {cell("Link", links['MVRV'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">Ahr999 抄底</span>
                        {cell("Link", links['AHR999'])}
                    </div>
                    <div class="grid-item">
                        <span class="grid-label">披萨指数</span>
                        {cell("Link", links['PIZZA'])}
                    </div>
                </div>
            </div>
            
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    print("开始任务...")
    y_data = get_yahoo_data()
    t_data = get_tactical_data()
    html = generate_html(y_data, t_data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("任务完成")
