import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz

# ==========================================
# 顶级宏观与微观流动性监控引擎 (GitHub Actions 战术大屏版)
# ==========================================

def get_yahoo_data():
    tickers = {
        "BTC_PRICE": "BTC-USD",
        "US10Y": "^TNX",      
        "DXY": "DX-Y.NYB",    
        "VIX": "^VIX",        
        "HYG": "HYG",         
        "USDCNH": "CNH=X",
        "GOLD": "GC=F",       
        "SILVER": "SI=F",     
        "COPPER": "HG=F"      
        # 注：雅虎财经的 AH 股数据已失效，从这里彻底踢出，防止报错污染日志。
    }
    
    data = {}
    for name, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            price = stock.fast_info['last_price']
            prev_close = stock.fast_info.get('previous_close', price)
            
            if name == "US10Y":
                fmt_price = f"{price:.2f}%"
            elif name == "BTC_PRICE":
                fmt_price = f"${price:,.2f}"
            else:
                fmt_price = f"{price:.2f}"
                
            data[name] = {
                "value": fmt_price,
                "trend": "🔴" if price > prev_close else "🟢" if price < prev_close else "⚪"
            }
        except:
            data[name] = {"value": "N/A", "trend": "⚪"}
    return data

def get_tactical_data():
    data = {}
    
    # 1. 免密白嫖美联储 FRED 数据
    fred_series = {
        "TGA": "WTREGEN",
        "RRP": "RRPONTSYD",
        "HYG_SPREAD": "BAMLH0A0HYM2"
    }
    for name, series_id in fred_series.items():
        try:
            csv_url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
            df = pd.read_csv(csv_url)
            last_val = float(df.iloc[-1, 1])
            if name in ["TGA", "RRP"]:
                data[name] = f"${last_val:.0f}B"
            else:
                data[name] = f"{last_val:.2f}%"
        except: data[name] = "Link"

    # 2. BTC.D
    try:
        url = "https://api.coingecko.com/api/v3/global"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            val = r.json()['data']['market_cap_percentage']['btc']
            data['BTC.D'] = f"{val:.1f}%"
        else: data['BTC.D'] = "Link"
    except: data['BTC.D'] = "Link"

    # 3. 贪婪恐慌
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=10)
        if r.status_code == 200:
            item = r.json()['data'][0]
            data['FEAR_GREED'] = f"{item['value']} ({item['value_classification']})"
        else: data['FEAR_GREED'] = "Link"
    except: data['FEAR_GREED'] = "Link"

    # 4. ETH Gas
    try:
        r = requests.get("https://beaconcha.in/api/v1/execution/gasnow", timeout=10)
        if r.status_code == 200:
            rapid = r.json()['data']['rapid']
            gas_val = int(rapid / 1000000000)
            data['GAS'] = f"{gas_val} Gwei"
        else: data['GAS'] = "Link"
    except: data['GAS'] = "Link"

    return data

def generate_html(y_data, t_data):
    beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')
    
    links = {
        "RRP": "https://fred.stlouisfed.org/series/RRPONTSYD",
        "TGA": "https://fred.stlouisfed.org/series/WTREGEN",
        "HYG_SPREAD": "https://fred.stlouisfed.org/series/BAMLH0A0HYM2",
        "AH_LINK": "https://quote.eastmoney.com/gb/zsHSAHP.html",
        "BTC_D_LINK": "https://www.tradingview.com/chart/?symbol=CRYPTOCAP%3ABTC.D",
        "USDT_PREMIUM": "https://www.feixiaohao.com/data/stable.html",
        "FG": "https://www.coinglass.com/zh/pro/i/FearGreedIndex",
        "GAS": "https://etherscan.io/gastracker",
        "MMFI": "https://www.tradingview.com/symbols/MMFI/",
        "CB_PREM": "https://www.coinglass.com/zh/pro/i/coinbase-bitcoin-premium-index",
        "FUNDING": "https://www.coinglass.com/zh/FundingRate",
        "BLK_BTC": "https://www.coinglass.com/zh/bitcoin-etf",
        "BLK_ETH": "https://www.coinglass.com/zh/eth-etf",
        "STH": "https://www.coinglass.com/zh/pro/i/short-term-holder-price",
        "MVRV": "https://www.bitcoinmagazinepro.com/charts/mvrv-zscore/",
        "AHR999": "https://9992100.xyz/",
        "STABLE_LINK": "https://defillama.com/stablecoins",
        "STABLE_FLOW": "https://defillama.com/stablecoins",
        "SSR": "https://www.tradingview.com/chart/?symbol=CRYPTOCAP%3ABTC%2FCRYPTOCAP%3ASTABLE.C",
        "USDe": "https://defillama.com/protocol/stablecoins/ethena",
        "PYUSD": "https://defillama.com/stablecoin/paypal-usd",
        "Ondo": "https://defillama.com/protocol/stablecoins/ondo-finance",
        "BUIDL": "https://defillama.com/rwa/asset/BUIDL",
        "BENJI": "https://defillama.com/rwa/asset/BENJI", 
        "USDM": "https://defillama.com/protocol/mountain-protocol",
        "USTB": "https://defillama.com/protocol/superstate",
        "CME_OI": "https://www.coinglass.com/zh/BitcoinOpenInterest",
        "LS_RATIO": "https://www.coinglass.com/zh/LongShortRatio",
        "DEX_VOL": "https://defillama.com/dexs",
        "MINER": "https://www.theblock.co/data/on-chain-metrics/bitcoin/bitcoin-miner-revenue-daily",
        "DVOL": "https://www.deribit.com/statistics/BTC/volatility" 
    }
    
    def cell(val, link, label="👁️ 查看"):
        if val == "Link" or val == "N/A" or val == "---":
            return f"<a href='{link}' target='_blank' class='btn'>{label}</a>"
        else:
            return f"<span class='val-text'>{val}</span>"

    # 前端保留 AH 溢价查看入口，但不依赖雅虎抓取数据，避免崩溃
    ah_cell = cell("Link", links['AH_LINK'])

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Project Trident: 全域金融监控雷达</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            :root {{
                --bg-color: #0d1117;
                --panel-bg: #161b22;
                --text-main: #c9d1d9;
                --text-muted: #8b949e;
                --border-color: #30363d;
                --accent-blue: #58a6ff;
                --accent-green: #3fb950;
                --accent-red: #ff7b72;
                --accent-yellow: #d29922;
            }}
            body {{ font-family: 'Courier New', Courier, monospace; margin: 0; padding: 15px; background: var(--bg-color); color: var(--text-main); }}
            .container {{ max-width: 1300px; margin: 0 auto; }}
            h1 {{ text-align: center; color: var(--accent-green); margin-bottom: 5px; text-transform: uppercase; text-shadow: 0 0 10px rgba(63, 185, 80, 0.3); }}
            .time {{ text-align: center; color: var(--text-muted); font-size: 0.85em; margin-bottom: 25px; }}
            .card {{ background: var(--panel-bg); padding: 20px; border-radius: 6px; border: 1px solid var(--border-color); margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
            h2 {{ font-size: 1.1em; color: var(--accent-blue); border-left: 4px solid var(--accent-blue); padding-left: 10px; margin: 0 0 20px 0; text-transform: uppercase; }}
            
            /* Table Styling */
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
            th {{ font-size: 0.85em; color: var(--text-muted); padding: 10px 5px; border-bottom: 1px dashed var(--border-color); font-weight: normal; }}
            td {{ padding: 12px 5px; text-align: center; border-bottom: 1px solid #1f242c; font-size: 1.05em; font-weight: bold; color: #fff; }}
            .trend {{ font-size: 0.7em; margin-left: 4px; }}
            
            /* Grid Box Styling */
            .grid-box {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; }}
            .grid-item {{ background: #010409; padding: 15px 10px; border-radius: 4px; text-align: center; border: 1px solid var(--border-color); transition: all 0.2s; }}
            .grid-item:hover {{ border-color: var(--accent-blue); transform: translateY(-2px); }}
            .grid-label {{ display: block; font-size: 0.8em; color: var(--text-muted); margin-bottom: 8px; text-transform: uppercase; }}
            
            /* Links & Values */
            .btn {{ display: inline-block; background: transparent; color: var(--accent-yellow); padding: 4px 12px; border-radius: 3px; text-decoration: none; font-size: 0.9em; border: 1px solid var(--accent-yellow); transition: all 0.2s; }}
            .btn:hover {{ background: var(--accent-yellow); color: #000; }}
            .val-text {{ color: #fff; font-weight: bold; letter-spacing: 0.5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📡 Project Trident: 终极绞肉机雷达</h1>
            <div class="time">>>> SYSTEM ALIVE | LAST SYNC: {beijing_time} (BJT)</div>
            
            <div class="card">
                <h2>🌍 Tier 1: 宏观重力与天候 (Macro)</h2>
                <div style="overflow-x: auto;">
                    <table style="min-width: 900px;">
                        <thead>
                            <tr>
                                <th>10Y美债<br>成本引擎</th>
                                <th>DXY美元<br>全球水管</th>
                                <th>RRP逆回购<br>隔夜冗余</th>
                                <th>TGA余额<br>财政核弹</th>
                                <th>VIX恐慌<br>风暴眼</th>
                                <th>HYG价格<br>垃圾债</th>
                                <th>违约利差<br>信贷冰山</th>
                                <th>黄金<br>避险</th>
                                <th>白银<br>投机</th>
                                <th>铜<br>复苏</th>
                                <th>USD/CNH<br>离岸汇率</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{y_data.get('US10Y', {{}}).get('value', 'N/A')}<span class="trend">{y_data.get('US10Y', {{}}).get('trend', '⚪')}</span></td>
                                <td>{y_data.get('DXY', {{}}).get('value', 'N/A')}<span class="trend">{y_data.get('DXY', {{}}).get('trend', '⚪')}</span></td>
                                <td>{cell(t_data.get('RRP', 'Link'), links['RRP'])}</td>
                                <td>{cell(t_data.get('TGA', 'Link'), links['TGA'])}</td>
                                <td>{y_data.get('VIX', {{}}).get('value', 'N/A')}<span class="trend">{y_data.get('VIX', {{}}).get('trend', '⚪')}</span></td>
                                <td>{y_data.get('HYG', {{}}).get('value', 'N/A')}<span class="trend">{y_data.get('HYG', {{}}).get('trend', '⚪')}</span></td>
                                <td>{cell(t_data.get('HYG_SPREAD', 'Link'), links['HYG_SPREAD'])}</td>
                                <td>{y_data.get('GOLD', {{}}).get('value', 'N/A')}<span class="trend">{y_data.get('GOLD', {{}}).get('trend', '⚪')}</span></td>
                                <td>{y_data.get('SILVER', {{}}).get('value', 'N/A')}<span class="trend">{y_data.get('SILVER', {{}}).get('trend', '⚪')}</span></td>
                                <td>{y_data.get('COPPER', {{}}).get('value', 'N/A')}<span class="trend">{y_data.get('COPPER', {{}}).get('trend', '⚪')}</span></td>
                                <td>{y_data.get('USDCNH', {{}}).get('value', 'N/A')}<span class="trend">{y_data.get('USDCNH', {{}}).get('trend', '⚪')}</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="card">
                <h2>📈 Tier 2: 加密基石与估值生死线 (Valuation)</h2>
                <div class="grid-box">
                    <div class="grid-item"><span class="grid-label">BTC 现价</span><span class="val-text" style="color:var(--accent-green);font-size:1.2em;">{y_data.get('BTC_PRICE', {{}}).get('value', 'N/A')}</span></div>
                    <div class="grid-item"><span class="grid-label">BTC 市占率</span>{cell(t_data.get('BTC.D', 'Link'), links['BTC_D_LINK'])}</div>
                    <div class="grid-item"><span class="grid-label">USDT场外溢价</span>{cell("Link", links['USDT_PREMIUM'])}</div>
                    <div class="grid-item"><span class="grid-label">贪婪恐慌指数</span>{cell(t_data.get('FEAR_GREED', 'Link'), links['FG'])}</div>
                    <div class="grid-item"><span class="grid-label">以太坊 Gas</span>{cell(t_data.get('GAS', 'Link'), links['GAS'])}</div>
                    <div class="grid-item"><span class="grid-label">MMFI 宽度</span>{cell("Link", links['MMFI'])}</div>
                    <div class="grid-item"><span class="grid-label">Coinbase 溢价</span>{cell("Link", links['CB_PREM'])}</div>
                    <div class="grid-item"><span class="grid-label">贝莱德 IBIT</span>{cell("Link", links['BLK_BTC'])}</div>
                    <div class="grid-item"><span class="grid-label">贝莱德 ETHA</span>{cell("Link", links['BLK_ETH'])}</div>
                    <div class="grid-item"><span class="grid-label">STH 散户成本</span>{cell("Link", links['STH'])}</div>
                    <div class="grid-item"><span class="grid-label">MVRV 逃顶线</span>{cell("Link", links['MVRV'])}</div>
                    <div class="grid-item"><span class="grid-label">AHR999 抄底</span>{cell("Link", links['AHR999'])}</div>
                </div>
            </div>

            <div class="card">
                <h2>🏛️ Tier 3: 华尔街老钱与深层流向 (TradFi & Flow)</h2>
                <div class="grid-box">
                    <div class="grid-item"><span class="grid-label" style="color:var(--accent-red);">稳定币总市值</span>{cell(t_data.get('STABLE_CAP', 'Link'), links['STABLE_LINK'])}</div>
                    <div class="grid-item"><span class="grid-label" style="color:var(--accent-red);">7日净流向/铸币</span>{cell("Link", links['STABLE_FLOW'], "🔥 监控")}</div>
                    <div class="grid-item"><span class="grid-label">SSR 购买力</span>{cell("Link", links['SSR'])}</div>
                    <div class="grid-item"><span class="grid-label">USDe (Ethena)</span>{cell("Link", links['USDe'])}</div>
                    <div class="grid-item"><span class="grid-label">PYUSD (PayPal)</span>{cell("Link", links['PYUSD'])}</div>
                    <div class="grid-item"><span class="grid-label">Ondo Finance</span>{cell("Link", links['Ondo'])}</div>
                    <div class="grid-item"><span class="grid-label">BUIDL (贝莱德)</span>{cell("Link", links['BUIDL'])}</div>
                    <div class="grid-item"><span class="grid-label">BENJI (富兰克林)</span>{cell("Link", links['BENJI'])}</div>
                    <div class="grid-item"><span class="grid-label">USDM (Mountain)</span>{cell("Link", links['USDM'])}</div>
                    <div class="grid-item"><span class="grid-label">USTB (Superstate)</span>{cell("Link", links['USTB'])}</div>
                    <div class="grid-item"><span class="grid-label">北向资金(A股)</span>{ah_cell}</div>
                </div>
            </div>

            <div class="card">
                <h2>🩸 Tier 4: 微观绞肉机与上帝底牌 (Microstructure)</h2>
                <div class="grid-box">
                    <div class="grid-item"><span class="grid-label">合约资金费率</span>{cell("Link", links['FUNDING'], "🗡️ 查费率")}</div>
                    <div class="grid-item"><span class="grid-label">合约持仓当量(OI)</span>{cell("Link", links['CME_OI'])}</div>
                    <div class="grid-item"><span class="grid-label">筹码多空比背离</span>{cell("Link", links['LS_RATIO'], "⚔️ 查背离")}</div>
                    <div class="grid-item"><span class="grid-label">DEX 狂热交易量</span>{cell("Link", links['DEX_VOL'], "⚡ 查链上")}</div>
                    <div class="grid-item"><span class="grid-label">矿工物理抛压</span>{cell("Link", links['MINER'], "⛏️ 查矿工")}</div>
                    <div class="grid-item"><span class="grid-label">Deribit 灾难保险</span>{cell("Link", links['DVOL'], "🛡️ 查DVOL")}</div>
                </div>
            </div>
            
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    print("[SYSTEM] 启动 Project Trident 全域扫描...")
    y_data = get_yahoo_data()
    t_data = get_tactical_data()
    html = generate_html(y_data, t_data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[SYSTEM] HTML 构建完成。前哨雷达部署完毕。")
