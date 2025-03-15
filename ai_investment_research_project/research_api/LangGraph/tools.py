from langchain_core.tools import Tool
from FinanceData.polygon_api import fetch_historical_stock_data_polygon
from FinanceData.scraping import scrape_stock_data
from FinanceData.polygon_api import fetch_historical_stock_data_polygon
from tavily import TavilyClient


def web_query(query):
    query = query.strip('"')
    
    try:
        client = TavilyClient(api_key="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")

        response = client.search(
            query=query,
            search_depth="basic",
            max_results=5
        )
        return response
    except Exception as e:
        return f"Error during web query: {e}"
    
class ToolsManager:
    def __init__(self):
        self.stock_data_tool = Tool(
            name="Stock Data Tool",
            func=scrape_stock_data,
            description="Fetches most recent stock price, intraday market capitalization, and PE ratio (TTM) for a given ticker symbol."
        )
        self.historical_data_tool = Tool(
            name="30 Day Stock Price Data Tool",
            func=fetch_historical_stock_data_polygon,
            description="Fetches historial stock price data for a given ticker symbol and date range."
        )

        self.web_query_tool = Tool(
            name="Web Query Tool",
            func=web_query,
            description="Fetch real-time information from the web given a query."
        )
    
    def get_tools(self):
        return [self.stock_data_tool, self.historical_data_tool, self.web_query_tool]    