import ccxt
import pandas as pd

# Configura tus credenciales de API de Binance
api_key = 'RzMWErwb1DjmfXHLeOWpy8ixU6jBqsq9dD7JQmtlMpRK2G7gbQMkUH5TWvmD65B4'
api_secret = 'wp5XjqPGxsaq0CwIB1fdACnmTIGVTrx9B4MBZjxfRSzXPBxe8oJZV8g1NbizEyXi'

# Crea una instancia del intercambio Binance
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})

# Define los pares de criptomonedas que deseas operar
symbols = ['BTC/USDT', 'BNB/USDT']

# Define la cantidad inicial de inversión en ARS
initial_ars_investment = 1000

# Define la cantidad máxima de inversión en cada par
max_investment_per_symbol = 500

# Función para obtener datos históricos
def fetch_historical_data(symbol, timeframe, limit):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

# Función para evaluar si el precio sube un cierto porcentaje en un día
def price_increase(df, percent_threshold):
    initial_price = df.iloc[0]['close']
    final_price = df.iloc[-1]['close']
    return (final_price - initial_price) / initial_price >= percent_threshold

# Función para vender criptomonedas y convertir a ARS
def sell_and_convert_to_ars(symbol, amount_to_sell):
    if amount_to_sell > 0:
        order = exchange.create_market_sell_order(symbol, amount_to_sell)
        print(f"Vendido {amount_to_sell} de {symbol} a precio de mercado.")

        # Calcula las ganancias en USDT y conviértelas a ARS
        usdt_balance = exchange.fetch_balance()['USDT']['total']
        ars_balance = usdt_balance * exchange.fetch_ticker('USDT/ARS')['last']
        print(f"Saldo en ARS: {ars_balance}")
        return ars_balance
    return 0

# Función para comprar criptomonedas con ARS
def buy_with_ars(symbol, amount_to_invest):
    if amount_to_invest > 0:
        order = exchange.create_market_buy_order(symbol, amount_to_invest)
        print(f"Comprado {amount_to_invest} de {symbol} a precio de mercado.")

# Loop para cada par de criptomonedas
for symbol in symbols:
    # Obtén datos históricos para el último día (ajusta el límite según tus necesidades)
    df = fetch_historical_data(symbol, '1d', limit=2)

    # Verifica si el precio subió un 10% en un día
    if price_increase(df, 0.10):
        # Vende criptomonedas y convierte a ARS
        balance = exchange.fetch_balance()
        amount_to_sell = min(balance[symbol.split('/')[0]]['total'], max_investment_per_symbol)
        ars_balance = sell_and_convert_to_ars(symbol, amount_to_sell)

        # Si se han obtenido ganancias en ARS, reinvierte en criptomonedas
        if ars_balance > 0:
            amount_to_invest = min(initial_ars_investment, ars_balance)
            buy_with_ars(symbol, amount_to_invest)
