from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .FinanceData.scraping import scrape_stock_price, scrape_market_cap, scrape_pe_ratio
from .FinanceData.polygon_api import fetch_stock_data_polygon
from .LangGraph.langgraph_workflow import investment_research_workflow, AgentState
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

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
    data = request.data
    
    message = data.get('message')
    conversation_id = data.get('conversationId')
    
    if not message:
        return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

    initial_state: AgentState = {
        "input": message,
        "information": None,
        "agent_outcome": None,
        "original_query": message,
        "conversation_id": conversation_id,
        "iteration_count": 0,
        "chat_history": []
    }
    try:    
        final_state = investment_research_workflow.invoke(initial_state)
        agent_outcome = final_state.get('agent_outcome')
                
        if agent_outcome is None:
            llm_response = "No response from LLM."
        else:
            if isinstance(agent_outcome.content, list):
                llm_response = ""
                for item in agent_outcome.content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        llm_response += item.get("text", "")
            else:
                llm_response = agent_outcome.content
        
        next_steps = final_state.get('next_steps')
        related_questions = "No response from LLM"
        
        if next_steps:
            # Handle both string and AIMessage cases
            if isinstance(next_steps, str):
                related_questions = next_steps  
            elif hasattr(next_steps, "content"):  
                related_questions = next_steps.content
            else:
                logger.warning(f"Unexpected next_steps format: {next_steps}")
                
        return Response({
            "text": llm_response,
            "charts": [],
            "links": [],
            "conversationId": conversation_id,
            "related_questions": related_questions
        })
#         return Response({
#             "text": '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse blandit tristique tempor. Fusce molestie, augue et tincidunt vestibulum, libero metus porta enim, nec vehicula risus risus in neque. Duis quis posuere dolor. Aliquam eu metus aliquet, ullamcorper enim a, fermentum diam. Maecenas semper nec arcu a sagittis. Quisque elementum mauris nibh. Proin posuere, ligula nec pharetra dapibus, nulla metus ullamcorper lacus, a volutpat ante metus eget sem.

# Suspendisse interdum lectus non arcu porta, vel dapibus nisl consequat. Aliquam erat volutpat. Suspendisse massa sapien, mollis vitae arcu eu, consectetur gravida libero. Vestibulum condimentum et risus vitae lacinia. Donec a elementum purus. Praesent ultricies, felis vitae porta imperdiet, turpis velit efficitur tortor, eu scelerisque velit massa vitae turpis. Suspendisse volutpat congue felis. Proin odio ante, tincidunt non est ac, pretium fermentum quam. Proin at lacinia justo. Duis metus metus, tincidunt et metus eget, pellentesque pharetra justo. Curabitur tristique sodales nisi, rutrum ultricies ipsum. Quisque sed nibh id ex accumsan euismod vitae ut nisl.

# Praesent eleifend augue in aliquam laoreet. Morbi sit amet justo at est vulputate facilisis. Pellentesque molestie ante at efficitur ullamcorper. In ut odio velit. Praesent tincidunt quam non risus mollis fermentum. Suspendisse purus nisi, eleifend ut volutpat eget, eleifend id purus. Donec eget neque justo. Aenean sodales efficitur urna. Integer non libero eu augue viverra semper non et mi. Quisque vulputate et mauris sagittis laoreet. Donec quis urna volutpat magna fermentum efficitur. Sed at venenatis enim, non feugiat risus. Vestibulum lobortis accumsan mi, non mattis sapien viverra consectetur. Sed eget vulputate purus, a porttitor magna. Cras porttitor pretium lacinia.

# Maecenas pellentesque aliquet fermentum. Sed quam purus, varius eget tristique a, fermentum non odio. Duis ac pulvinar est. Donec et tortor luctus felis congue finibus. Nunc vehicula libero ac magna suscipit, sit amet elementum nibh rutrum. Morbi turpis eros, eleifend quis euismod in, posuere eget diam. Praesent lobortis lacinia eros fermentum feugiat. Cras id varius arcu. Morbi felis risus, laoreet faucibus elementum eu, suscipit eget arcu.

# Cras sagittis diam non augue fermentum, sed porttitor justo sollicitudin. Cras fermentum velit eu justo ultricies luctus. Quisque vitae pretium est, sed sollicitudin metus. Phasellus ut enim et ipsum iaculis interdum. Praesent viverra turpis quis justo scelerisque hendrerit. Nullam enim lectus, placerat eu ligula id, mollis luctus velit. Cras eu nisl quis odio molestie volutpat eu et nibh. Vestibulum libero turpis, rutrum vitae maximus nec, malesuada in urna. Aenean sed pretium mauris.''',
#             "charts": [],
#             "links": [],
#             "conversationId": "some number",
#             "related_questions": ["## How does Amazon's AWS division currently contribute to its overall revenue and profitability, and what is the growth outlook for this segment?","## What are the key competitors to watch in Amazon's various business segments (e-commerce, cloud, advertising) and how might they impact Amazon's market position?","## How might current regulatory challenges across global markets potentially impact Amazon's growth strategy and valuation over the next 2-3 years?"]
#         })

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

    historical_data = fetch_stock_data_polygon(ticker, start_date_str, end_date_str)
    if "error" in historical_data:
        return Response(historical_data, status=500)
    return Response({"ticker": ticker, "historical_data": historical_data})