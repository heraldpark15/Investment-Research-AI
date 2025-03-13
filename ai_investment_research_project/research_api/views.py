from rest_framework.decorators import api_view
from rest_framework.response import Response
from .scraping import scrape_stock_price, scrape_market_cap, scrape_pe_ratio
from .langgraph_workflow import basic_research_workflow, AgentState
from .models import StockResearchData

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, world!"})

@api_view(['GET'])
def get_stock_price_view(request):
    ticker = request.GET.get('ticker', 'AAPL')
    price = scrape_stock_price(ticker)

    if price:
        return Response({"ticker": ticker, "price": price})
    else:
        return Response({"error": "Could not retrieve stock price"}, status=400)

@api_view(['GET'])
def get_market_cap_view(request):
    ticker = request.GET.get('ticker', 'AAPL')
    market_cap = scrape_market_cap(ticker)

    if market_cap:
        return Response({"ticker": ticker, "Market Cap (intraday)": market_cap})
    else:
        return Response({"error": "Could not retrieve market capitalization"}, status=400)

@api_view(['GET'])
def get_pe_ratio_view(request):
    ticker = request.GET.get('ticker', 'AAPL')
    pe_ratio = scrape_pe_ratio(ticker)

    if pe_ratio:
        return Response({"ticker": ticker, "PE Ratio (TTM)": pe_ratio})
    else: 
        return Response({"error": "Could not retrieve PE ratio"}, status=400)


@api_view(['GET'])
def run_basic_research_workflow_view(request):
    ticker = request.GET.get('ticker', 'AAPL')

    initial_state: AgentState = {
        "ticker_symbol": ticker,
        "stock_price": None,  
        "market_cap": None,
        "pe_ratio": None,
        "summary": None
    }
    results = basic_research_workflow.invoke(initial_state)
    final_state = results

    response_data = {
        "ticker": final_state["ticker_symbol"],
        "stock_price": final_state["stock_price"],
        "market_cap": final_state["market_cap"],
        "pe_ratio": final_state["pe_ratio"],
        "summary": final_state["summary"],
    }

    return Response(response_data)

