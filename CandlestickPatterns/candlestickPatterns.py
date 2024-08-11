import ccxt
import pandas as pd
import talib

# Set Pandas settings to display all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Connect to the Binance exchange
exchange = ccxt.binance()

# Specify the symbol and timeframe you want
symbol = 'LINK/USDT'
timeframe = '4h'  

# Fetch the last X candles (e.g., the last 100 candles)
limit = 100
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Adjust the time to UTC (which is the default, so no need to localize)
df['timestamp'] = df['timestamp'].dt.tz_localize('UTC')  # Ensure UTC timezone is set

# Select closed candles by taking all candles except the last one
df = df.iloc[:-1].reset_index(drop=True)  # Excluding the last candle

# Identify candlestick patterns using TA-Lib
patterns = {
    'hammer': talib.CDLHAMMER,
    'engulfing': talib.CDLENGULFING,
    'piercing': talib.CDLPIERCING,
    'shooting_star': talib.CDLSHOOTINGSTAR,
    'dark_cloud_cover': talib.CDLDARKCLOUDCOVER,
    'morning_star': talib.CDLMORNINGSTAR,
    'evening_star': talib.CDLEVENINGSTAR,
    'three_white_soldiers': talib.CDL3WHITESOLDIERS,
    'three_black_crows': talib.CDL3BLACKCROWS,
    'doji': talib.CDLDOJI,
    'harami': talib.CDLHARAMI,
    'harami_cross': talib.CDLHARAMICROSS,
    'abandoned_baby': talib.CDLABANDONEDBABY,
    'advanced_block': talib.CDLADVANCEBLOCK,
    'belt_hold': talib.CDLBELTHOLD,
    'breakaway': talib.CDLBREAKAWAY,
    'closing_marubozu': talib.CDLCLOSINGMARUBOZU,
    'conceal_baby_swallow': talib.CDLCONCEALBABYSWALL,
    'counterattack': talib.CDLCOUNTERATTACK,
    'dragonfly_doji': talib.CDLDRAGONFLYDOJI,
    'gap_sideside_white': talib.CDLGAPSIDESIDEWHITE,
    'gravestone_doji': talib.CDLGRAVESTONEDOJI,
    'hanging_man': talib.CDLHANGINGMAN,
    'high_wave': talib.CDLHIGHWAVE,
    'hikkake': talib.CDLHIKKAKE,
    'hikkake_mod': talib.CDLHIKKAKEMOD,
    'homing_pigeon': talib.CDLHOMINGPIGEON,
    'identical_three_crows': talib.CDLIDENTICAL3CROWS,
    'in_neck': talib.CDLINNECK,
    'inverted_hammer': talib.CDLINVERTEDHAMMER,
    'kicking': talib.CDLKICKING,
    'kicking_by_length': talib.CDLKICKINGBYLENGTH,
    'ladder_bottom': talib.CDLLADDERBOTTOM,
    'long_legged_doji': talib.CDLLONGLEGGEDDOJI,
    'long_line': talib.CDLLONGLINE,
    'marubozu': talib.CDLMARUBOZU,
    'matching_low': talib.CDLMATCHINGLOW,
    'math_hold': talib.CDLMATHOLD,
    'rikshaw_man': talib.CDLRICKSHAWMAN,
    'rise_fall_three': talib.CDLRISEFALL3METHODS,
    'separating_lines': talib.CDLSEPARATINGLINES,
    'shooting_star': talib.CDLSHOOTINGSTAR,
    'short_line': talib.CDLSHORTLINE,
    'spinning_top': talib.CDLSPINNINGTOP,
    'stalled_pattern': talib.CDLSTALLEDPATTERN,
    'stick_sandwich': talib.CDLSTICKSANDWICH,
    'takuri': talib.CDLTAKURI,
    'tasuki_gap': talib.CDLTASUKIGAP,
    'thrusting': talib.CDLTHRUSTING,
    'tristar': talib.CDLTRISTAR,
    'unique_three': talib.CDLUNIQUE3RIVER,
    'upside_gap_two_crows': talib.CDLUPSIDEGAP2CROWS,
    'upside_downside_gap_three': talib.CDLXSIDEGAP3METHODS
}

# Add candlestick patterns to the DataFrame
for pattern_name, pattern_func in patterns.items():
    df[pattern_name] = pattern_func(df['open'], df['high'], df['low'], df['close'])

# Analyze patterns and determine if the result is bullish or bearish
def analyze_candlestick(row):
    for pattern_name in patterns.keys():
        if row[pattern_name] > 0:
            return 'Bullish', pattern_name
        elif row[pattern_name] < 0:
            return 'Bearish', pattern_name
    return 'Neutral', None

df['signal'], df['pattern'] = zip(*df.apply(analyze_candlestick, axis=1))

# Drop unnecessary columns
df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume', 'signal', 'pattern']]

# Specifically analyze Doji candles
def refine_doji_signal(row):
    if row['pattern'] == 'doji':
        prev_close = df.loc[row.name - 1, 'close'] if row.name > 0 else None
        prev_open = df.loc[row.name - 1, 'open'] if row.name > 0 else None
        if prev_close and prev_open:
            if prev_close < prev_open:
                return 'Bullish'
            elif prev_close > prev_open:
                return 'Bearish'
    return row['signal']

df['signal'] = df.apply(refine_doji_signal, axis=1)

# Print the results
print(df)
