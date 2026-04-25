import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import pytz

# ==========================================
# 顶级宏观与微观流动性监控引擎 (GitHub Actions 战术大屏版 - 全火力满载+顶格防抽风版)
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
    
    # 1. 免密美联储 FRED 数据
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
        # --- 基础宏观 ---
        "RRP": "https://fred.stlouisfed.org/series/RRPONTSYD",
        "TGA": "https://fred.stlouisfed.org/series/WTREGEN",
        "HYG_SPREAD": "https://fred.stlouisfed.org/series/BAMLH0A0HYM2",
        "AH_LINK": "https://quote.eastmoney.com/gb/zsHSAHP.html",
        "CN10Y_YIELD": "https://cn.tradingview.com/symbols/TVC-CN10Y/",  
        
        # --- 加密基础 ---
        "BTC_D_LINK": "https://www.tradingview.com/chart/?symbol=CRYPTOCAP%3ABTC.D",
        "USDT_PREMIUM": "https://www.feixiaohao.com/data/stable.html",
        "FG": "https://www.coinglass.com/zh/pro/i/FearGreedIndex",
        "GAS": "https://etherscan.io/gastracker",
        "MMFI": "https://www.tradingview.com/symbols/MMFI/",
        "SOL_ETH_RATIO": "https://defillama.com/dexs/chains",
        
        # --- 估值与 ETF ---
        "CB_PREM": "https://www.coinglass.com/zh/pro/i/coinbase-bitcoin-premium-index",
        "FUNDING": "https://www.coinglass.com/zh/FundingRate",
        "BLK_BTC": "https://www.coinglass.com/zh/bitcoin-etf",
        "BLK_ETH": "https://www.coinglass.com/zh/eth-etf",
        "STH": "https://www.coinglass.com/zh/pro/i/short-term-holder-price",
        "MVRV": "https://www.bitcoinmagazinepro.com/charts/mvrv-zscore/",
        "AHR999": "https://9992100.xyz/",
        "PIZZA": "https://www.pizzint.watch/", 
        
        # --- 华尔街 RWA 与 东方流动性 ---
        "STABLE_LINK": "https://defillama.com/stablecoins",
        "USDT_FLOW": "https://defillama.com/stablecoin/tether", 
        "USDC_FLOW": "https://defillama.com/stablecoin/usd-coin",
        "SSR": "https://www.tradingview.com/chart/?symbol=CRYPTOCAP%3ABTC%2FCRYPTOCAP%3ASTABLE.C",
        "RWA_TOTAL_MCAP": "https://defillama.com/rwa", 
        "RWA_TOTAL_YIELD": "https://app.rwa.xyz/treasuries", 
        "HK_BTC_ETF": "https://cn.tradingview.com/symbols/HKEX-3042/",    
        "FDUSD_MCAP": "https://defillama.com/stablecoin/first-digital-usd", 
        "KIMCHI_PREM": "https://cryptoquant.com/asset/btc/chart/market-data/korea-premium-index?window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=line",  
        "USDe": "https://defillama.com/protocol/stablecoins/ethena",
        "sUSDe_YIELD": "https://defillama.com/yields?token=SUSDE",
        "PYUSD": "https://defillama.com/stablecoin/paypal-usd",
        "PYUSD_YIELD": "https://defillama.com/yields?token=PYUSD",
        "Ondo": "https://defillama.com/protocol/stablecoins/ondo-finance",
        "ONDO_YIELD": "https://defillama.com/protocol/yields/ondo-finance",
        "BUIDL": "https://defillama.com/rwa/asset/BUIDL",
        "BUIDL_YIELD": "https://defillama.com/yields?token=BUIDL",
        "BENJI": "https://defillama.com/rwa/asset/BENJI", 
        "BENJI_YIELD": "https://defillama.com/yields?token=BENJI",
        "USDM": "https://defillama.com/protocol/mountain-protocol",
        "USDM_YIELD": "https://defillama.com/yields?token=USDM",
        "USTB": "https://defillama.com/protocol/superstate",
        "USTB_YIELD": "https://defillama.com/yields?token=USTB",
        "USDS_MCAP": "https://defillama.com/stablecoin/dai",
        "USDS_YIELD": "https://defillama.com/yields?token=USDS",
        
        # --- 微观绞肉机 ---
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

# ！！！警告：下面的 HTML 代码故意没有缩进，全靠最左边！
# ！！！这是为了防止 Github Pages 把网页当成 Markdown 代码块渲染！千万别在这个区块里加空格！
    html = f"""<!DOCTYPE html>
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
table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
th {{ font-size: 0.85em; color: var(--text-muted); padding: 10px 5px; border-bottom: 1px dashed var(--border-color); font-weight: normal; }}
td {{ padding: 12px 5px; text-align: center; border-bottom: 1px solid #1f242c; font-size: 1.05em; font-weight: bold; color: #fff; }}
.trend {{ font-size: 0.7em; margin-left: 4px; }}
.grid-box {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; }}
.grid-item {{ background: #010409; padding: 15px 10px; border-radius: 4px; text-align: center; border: 1px solid var(--border-color); transition: all 0.2s; }}
.grid-item:hover {{ border-color: var(--accent-blue); transform: translateY(-2px); }}
.grid-label {{ display: block; font-size: 0.8em; color: var(--text-muted); margin-bottom: 8px; text-transform: uppercase; }}
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
<td>{y_data.get('US10Y', dict()).get('value', 'N/A')}<span class="trend">{y_data.get('US10Y', dict()).get('trend', '⚪')}</span></td>
<td>{y_data.get('DXY', dict()).get('value', 'N/A')}<span class="trend">{y_data.get('DXY', dict()).get('trend', '⚪')}</span></td>
<td>{cell(t_data.get('RRP', 'Link'), links['RRP'])}</td>
<td>{cell(t_data.get('TGA', 'Link'), links['TGA'])}</td>
<td>{y_data.get('VIX', dict()).get('value', 'N/A')}<span class="trend">{y_data.get('VIX', dict()).get('trend', '⚪')}</span></td>
<td>{y_data.get('HYG', dict()).get('value', 'N/A')}<span class="trend">{y_data.get('HYG', dict()).get('trend', '⚪')}</span></td>
<td>{cell(t_data.get('HYG_SPREAD', 'Link'), links['HYG_SPREAD'])}</td>
<td>{y_data.get('GOLD', dict()).get('value', 'N/A')}<span class="trend">{y_data.get('GOLD', dict()).get('trend', '⚪')}</span></td>
<td>{y_data.get('SILVER', dict()).get('value', 'N/A')}<span class="trend">{y_data.get('SILVER', dict()).get('trend', '⚪')}</span></td>
<td>{y_data.get('COPPER', dict()).get('value', 'N/A')}<span class="trend">{y_data.get('COPPER', dict()).get('trend', '⚪')}</span></td>
<td>{y_data.get('USDCNH', dict()).get('value', 'N/A')}<span class="trend">{y_data.get('USDCNH', dict()).get('trend', '⚪')}</span></td>
</tr>
</tbody>
</table>
</div>
</div>

<div class="card">
<h2>📈 Tier 2: 加密基石与估值生死线 (Valuation)</h2>
<div class="grid-box">
<div class="grid-item"><span class="grid-label">BTC 现价</span><span class="val-text" style="color:var(--accent-green);font-size:1.2em;">{y_data.get('BTC_PRICE', dict()).get('value', 'N/A')}</span></div>
<div class="grid-item"><span class="grid-label">BTC 市占率</span>{cell(t_data.get('BTC.D', 'Link'), links['BTC_D_LINK'])}</div>
<div class="grid-item"><span class="grid-label">SOL/ETH 狂热比率</span>{cell("Link", links['SOL_ETH_RATIO'], "🔥 查比率")}</div>
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
<div class="grid-item"><span class="grid-label">PIZZA 周期底线</span>{cell("Link", links['PIZZA'])}</div>
</div>
</div>

<div class="card">
<h2>🏛️ Tier 3: 华尔街老钱与深层流向 (TradFi & Flow)</h2>
<div class="grid-box">
<div class="grid-item"><span class="grid-label" style="color:var(--accent-red);">稳定币总市值</span>{cell(t_data.get('STABLE_CAP', 'Link'), links['STABLE_LINK'])}</div>
<div class="grid-item"><span class="grid-label" style="color:var(--accent-red);">USDT 净流入</span>{cell("Link", links['USDT_FLOW'], "🔥 监控")}</div>
<div class="grid-item"><span class="grid-label" style="color:var(--accent-red);">USDC 净流入</span>{cell("Link", links['USDC_FLOW'], "🔥 监控")}</div>
<div class="grid-item"><span class="grid-label">SSR 购买力</span>{cell("Link", links['SSR'])}</div>
<div class="grid-item"><span class="grid-label">全网 RWA 总规模</span>{cell("Link", links['RWA_TOTAL_MCAP'], "👁️ 查看")}</div>
<div class="grid-item"><span class="grid-label" style="color:var(--accent-yellow);">全网 RWA 收益率</span>{cell("Link", links['RWA_TOTAL_YIELD'], "👁️ 查看")}</div>
<div class="grid-item"><span class="grid-label">香港 BTC ETF</span>{cell("Link", links['HK_BTC_ETF'], "🇨🇳 东方主力")}</div>
<div class="grid-item"><span class="grid-label">FDUSD 东方钱袋</span>{cell("Link", links['FDUSD_MCAP'], "🇨🇳 离岸水管")}</div>
<div class="grid-item"><span class="grid-label">泡菜溢价 (韩国)</span>{cell("Link", links['KIMCHI_PREM'], "🇰🇷 亚洲狂热")}</div>
<div class="grid-item"><span class="grid-label">中国 10Y 国债</span>{cell("Link", links['CN10Y_YIELD'], "🇨🇳 放水总阀")}</div>
<div class="grid-item"><span class="grid-label">AH股溢价 / 北向</span>{cell("Link", links['AH_LINK'], "👁️ 查看")}</div>
<div class="grid-item"><span class="grid-label">USDe 规模</span>{cell("Link", links['USDe'])}</div>
<div class="grid-item"><span class="grid-label">sUSDe 收益率</span>{cell("Link", links['sUSDe_YIELD'])}</div>
<div class="grid-item"><span class="grid-label">PYUSD 规模</span>{cell("Link", links['PYUSD'])}</div>
<div class="grid-item"><span class="grid-label">PYUSD 收益率</span>{cell("Link", links['PYUSD_YIELD'])}</div>
<div class="grid-item"><span class="grid-label">Ondo 规模</span>{cell("Link", links['Ondo'])}</div>
<div class="grid-item"><span class="grid-label">Ondo 收益率</span>{cell("Link", links['ONDO_YIELD'])}</div>
<div class="grid-item"><span class="grid-label">BUIDL 规模</span>{cell("Link", links['BUIDL'])}</div>
<div class="grid-item"><span class="grid-label">BUIDL 收益率</span>{cell("Link", links['BUIDL_YIELD'])}</div>
<div class="grid-item"><span class="grid-label">BENJI 规模</span>{cell("Link", links['BENJI'])}</div>
<div class="grid-item"><span class="grid-label">BENJI 收益率</span>{cell("Link", links['BENJI_YIELD'])}</div>
<div class="grid-item"><span class="grid-label">USDM 规模</span>{cell("Link", links['USDM'])}</div>
<div class="grid-item"><span class="grid-label">USDM 收益率</span>{cell("Link", links['USDM_YIELD'])}</div>
<div class="grid-item"><span class="grid-label">USTB 规模</span>{cell("Link", links['USTB'])}</div>
<div class="grid-item"><span class="grid-label">USTB 收益率</span>{cell("Link", links['USTB_YIELD'])}</div>
<div class="grid-item"><span class="grid-label">USDS 规模</span>{cell("Link", links['USDS_MCAP'])}</div>
<div class="grid-item"><span class="grid-label">USDS 收益率</span>{cell("Link", links['USDS_YIELD'])}</div>
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
</html>"""
    return html

if __name__ == "__main__":
    print("[SYSTEM] 启动 Project Trident 全域扫描...")
    y_data = get_yahoo_data()
    t_data = get_tactical_data()
    html = generate_html(y_data, t_data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[SYSTEM] HTML 构建完成。前哨雷达部署完毕。")
