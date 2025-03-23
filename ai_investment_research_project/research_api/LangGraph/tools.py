from langchain_core.tools import Tool, StructuredTool
from ..FinanceData.polygon_api import fetch_stock_data_polygon
from ..FinanceData.scraping import scrape_stock_data
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
            name="stock_data_tool",
            func=scrape_stock_data,
            description="Fetches most recent stock price, intraday market capitalization, and PE ratio (TTM) for a given ticker symbol."
        )
        self.price_data_tool = StructuredTool.from_function(
            name="stock_price_daterange",
            func=fetch_stock_data_polygon,
            description="Fetches stock price data for a given ticker symbol and date range. The date range must be within the provided current date and in %Y-%m-%d format."
        )

        self.web_query_tool = Tool(
            name="web_query_tool",
            func=web_query,
            description="Fetch real-time information from the web given a query."
        )
    
    def get_tools(self):
        return [self.stock_data_tool, self.price_data_tool, self.web_query_tool]    