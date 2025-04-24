# research_api/scraping.py
from polygon import RESTClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_stock_data_polygon(ticker_symbol: str, start_date: str, end_date: str):
    """Fetches daily OHLCV data for a given ticker from Polygon API."""
    api_key = os.environ.get("POLYGON_API_KEY")  
    if not api_key:
        return {"error": "Polygon API key not found. Please set the POLYGON_API_KEY environment variable."}

    client = RESTClient(api_key=api_key)

    try:
        # Convert date strings to datetime objects if they are strings
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        data = client.get_aggs(
            ticker=ticker_symbol,
            multiplier=1,
            timespan="day",
            from_=start_date,
            to=end_date,
        )

        historical_data = []

        if isinstance(data, list):
            for result in data:
                timestamp = datetime.fromtimestamp(result.timestamp / 1000).strftime('%Y-%m-%d')  # Convert ms to datetime
                historical_data.append({
                    "timestamp": timestamp,
                    "open": result.open,
                    "high": result.high,
                    "low": result.low,
                    "close": result.close,
                    "volume": result.volume,
                })
        else:
            return {"error": f"Unexpected response structure from Polygon API: {data}"}

        return historical_data
    except Exception as e:
        return {"error": f"Error fetching historical data from Polygon API: {e}"}
