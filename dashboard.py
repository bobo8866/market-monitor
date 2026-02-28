import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

# === 1. 定义获取数据的函数 ===
def get_data():
    tickers = {
        "US10Y": "^TNX",      # 10年期美债收益率
        "DXY": "DX-Y.NYB",    # 美元指数
        "BTC": "BTC-USD",     # 比特币价格
        "VIX": "^VIX",        # 恐慌指数
        "HYG": "HYG",         # 高收益债ETF
        "SPX": "^GSPC",       # 标普500
        "USDCNH": "CNH=X"     # 离岸人民币汇率
    }
    
    data = {}
    for name, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d") # 获取最近5天数据以计算趋势
            if not hist.empty:
                data[name] = {
                    "current": round(hist['Close'].iloc[-1], 2),
                    "prev": round(hist['Close'].iloc[-2], 2),
                    "ma5": round(hist['Close'].mean(), 2) # 简单趋势判断
                }
            else:
                data[name] = {"current": 0, "prev": 0, "ma5": 0}
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            data[name] = {"current": 0, "prev": 0}
    return data

# === 2. 分析师逻辑大脑 (自动生成结论) ===
def analyze_market(d):
    signals = []
    
    # 宏观信号
    if d['US10Y']['current'] > 4.3:
        signals.append("🔴 美债收益率过高，压制资产价格")
    elif d['US10Y']['current'] < 3.8:
        signals.append("🟢 资金成本下降，利好科技/BTC")
        
    # 避险信号
    if d['DXY']['current'] > 105:
        signals.append("🔴 美元过强，非美货币承压")
        
    # 恐慌信号
    if d['VIX']['current'] < 13:
        signals.append("⚠️ 市场极度贪婪，注意回调")
    elif d['VIX']['current'] > 30:
        signals.append("🟢 恐慌极值，那是黄金坑")
        
    # 信用市场信号 (HYG破位预警)
    # 简单逻辑：如果 HYG 今日跌幅超过 1% 且 标普500 没跌
    hyg_change = (d['HYG']['current'] - d['HYG']['prev']) / d['HYG']['prev']
    spx_change = (d['SPX']['current'] - d['SPX']['prev']) / d['SPX']['prev']
    
    if hyg_change < -0.01 and spx_change > -0.005:
        signals.append("☠️ HYG信用债异常大跌，美股崩盘前兆！")
    else:
        signals.append("⚪ 信用市场状态正常")

    # 汇率信号
    if d['USDCNH']['current'] > 7.3:
        signals.append("🔴 人民币贬值压力大，利空A股核心资产")
    elif d['USDCNH']['current'] < 7.1:
        signals.append("🟢 人民币升值，利好中国资产")

    return signals

# === 3. 生成 HTML 网页 ===
def generate_html(data, analysis):
    beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>金融核武库监控台</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f0f2f5; }}
            .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
            h1 {{ color: #1a1a1a; text-align: center; }}
            .time {{ text-align: center; color: #666; font-size: 0.9em; margin-bottom: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
            th {{ background-color: #fafafa; color: #666; }}
            .value {{ font-weight: bold; font-family: monospace; font-size: 1.1em; }}
            .signal-box {{ background: #fff3cd; color: #856404; padding: 15px; border-radius: 5px; border-left: 5px solid #ffc107; }}
            .footer {{ text-align: center; margin-top: 40px; color: #999; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <h1>🌩️ 全球宏观监测哨</h1>
        <div class="time">最后更新 (北京时间): {beijing_time}</div>

        <div class="card">
            <h3>📊 核心指标看板</h3>
            <table>
                <tr><th>指标</th><th>当前值</th><th>昨收</th><th>状态</th></tr>
                <tr><td>🇺🇸 10年美债 (US10Y)</td><td class="value">{data['US10Y']['current']}%</td><td>{data['US10Y']['prev']}%</td><td>{ "⬆️" if data['US10Y']['current'] > data['US10Y']['prev'] else "⬇️"}</td></tr>
                <tr><td>💵 美元指数 (DXY)</td><td class="value">{data['DXY']['current']}</td><td>{data['DXY']['prev']}</td><td>{ "⬆️" if data['DXY']['current'] > data['DXY']['prev'] else "⬇️"}</td></tr>
                <tr><td>😱 恐慌指数 (VIX)</td><td class="value">{data['VIX']['current']}</td><td>{data['VIX']['prev']}</td><td>{ "⬆️" if data['VIX']['current'] > data['VIX']['prev'] else "⬇️"}</td></tr>
                <tr><td>🏦 高收益债 (HYG)</td><td class="value">${data['HYG']['current']}</td><td>${data['HYG']['prev']}</td><td>{ "⬆️" if data['HYG']['current'] > data['HYG']['prev'] else "⬇️"}</td></tr>
                <tr><td>🇨🇳 离岸人民币 (CNH)</td><td class="value">{data['USDCNH']['current']}</td><td>{data['USDCNH']['prev']}</td><td>{ "⬆️" if data['USDCNH']['current'] > data['USDCNH']['prev'] else "⬇️"}</td></tr>
                <tr><td>🪙 比特币 (BTC)</td><td class="value">${data['BTC']['current']}</td><td>${data['BTC']['prev']}</td><td>{ "⬆️" if data['BTC']['current'] > data['BTC']['prev'] else "⬇️"}</td></tr>
            </table>
            <p style="font-size:0.8em; color:#666;">*注：RRP逆回购与USDT溢价需手动查询</p>
        </div>

        <div class="card">
            <h3>🧠 分析师自动推演</h3>
            <div class="signal-box">
                {'<br><br>'.join(analysis)}
            </div>
        </div>

        <div class="footer">
            Powered by GitHub Actions & Python | Data Source: Yahoo Finance
        </div>
    </body>
    </html>
    """
    return html_content

# === 主程序 ===
if __name__ == "__main__":
    print("开始获取数据...")
    market_data = get_data()
    print("数据获取完成，开始分析...")
    analysis_result = analyze_market(market_data)
    print("生成网页中...")
    html = generate_html(market_data, analysis_result)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("完成！")
