from rest_framework.decorators import api_view
from rest_framework.response import Response
from .FinanceData.scraping import scrape_stock_price, scrape_market_cap, scrape_pe_ratio
from .FinanceData.polygon_api import fetch_historical_stock_data_polygon
from .LangGraph.langgraph_workflow import basic_research_workflow, AgentState
from datetime import datetime, timedelta

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
    start_date_str = request.query_params.get('start_date')
    end_date_str = request.query_params.get('end_date')

    # If start_date and end_date are not provided, default to the last 30 days
    if not start_date_str or not end_date_str:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
    else:
        try:
            datetime.strptime(start_date_str, '%Y-%m-%d')
            datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    historical_data = fetch_historical_stock_data_polygon(ticker, start_date_str, end_date_str)
    if "error" in historical_data:
        return Response(historical_data, status=500)

    initial_state: AgentState = {
        "ticker_symbol": ticker,
        "stock_price": None,  
        "market_cap": None,
        "pe_ratio": None,
        "summary": None
    }

    try:
        final_state = basic_research_workflow.invoke(initial_state)

        response_data = {
            "ticker": ticker,
            "stock_price": final_state.get("stock_price") if final_state else None,
            "market_cap": final_state.get("market_cap") if final_state else None,
            "pe_ratio": final_state.get("pe_ratio") if final_state else None,
            "summary": final_state.get("summary"),
        }
        return Response(response_data)

    except Exception as e:
        # Handle any exceptions that might occur during the workflow
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)
    

@api_view(['GET'])
def get_historical_data(request):
    ticker = request.query_params.get('ticker', 'AAPL')  # Default to AAPL
    start_date_str = request.query_params.get('start_date')
    end_date_str = request.query_params.get('end_date')

    # If start_date and end_date are not provided, default to the last 30 days
    if not start_date_str or not end_date_str:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
    else:
        try:
            datetime.strptime(start_date_str, '%Y-%m-%d')
            datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    historical_data = fetch_historical_stock_data_polygon(ticker, start_date_str, end_date_str)
    if "error" in historical_data:
        return Response(historical_data, status=500)
    return Response({"ticker": ticker, "historical_data": historical_data})