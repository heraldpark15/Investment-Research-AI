from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .FinanceData.scraping import scrape_stock_price, scrape_market_cap, scrape_pe_ratio
from .FinanceData.polygon_api import fetch_historical_stock_data_polygon
from .LangGraph.langgraph_workflow import investment_research_workflow, AgentState
from datetime import datetime, timedelta
import uuid

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


@api_view(['POST'])
def run_basic_research_workflow_view(request):
    message_list = request.GET.getlist('message') #get a list of all message parameters.
    conversation_id_list = request.GET.getlist('conversationId') #get a list of all conversationId parameters.

    if not message_list:
        return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    message = message_list[0] #get the first message from the list.
    conversation_id = conversation_id_list[0] if conversation_id_list else str(uuid.uuid4()) #get the first conversationId from the list or generate a new one.

    initial_state: AgentState = {
        "input": message,
        "information": None,
        "agent_outcome": None,
        "original_query": message,
        "conversation_id": conversation_id,
        "iteration_count": 0,
    }

    try:    
        final_state = investment_research_workflow.invoke(initial_state)
        agent_outcome = final_state.get('agent_outcome')
                
        if agent_outcome is None:
            llm_response = "No response from LLM."
        else:
            # Handle AIMessage object
            if isinstance(agent_outcome.content, list):
                # Extract text content from structured content
                llm_response = ""
                for item in agent_outcome.content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        llm_response += item.get("text", "")
            else:
                # Direct content access for string content
                llm_response = agent_outcome.content
        
        return Response({
            "text": llm_response,
            "charts": [],
            "links": [],
            "conversationId": conversation_id,
        })

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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