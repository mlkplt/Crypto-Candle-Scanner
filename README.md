# Features:

**Data Retrieval:** Fetches OHLCV (Open, High, Low, Close, Volume) data for a specified trading pair using the Binance API.

**Candlestick Pattern Detection:** Uses TA-Lib to identify various candlestick patterns such as Hammer, Engulfing, Doji, Shooting Star, and many others.

**Signal Generation:** Generates "Bullish" or "Bearish" signals based on the detected patterns.

**Doji Analysis:** Specifically refines the analysis of Doji patterns by considering the previous candle's close and open values.

# Usage:
This script is ideal for traders looking to perform technical analysis on cryptocurrency markets and develop trading strategies based on specific candlestick patterns. The generated signals can help in identifying potential buy or sell opportunities based on historical price data.

# Requirements:
> ccxt (for connecting to cryptocurrency exchanges)

> pandas (for data manipulation)

> talib (for technical analysis)

This script provides a solid foundation for enhancing your technical analysis and trading strategies.
