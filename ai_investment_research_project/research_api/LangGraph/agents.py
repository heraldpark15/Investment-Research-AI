from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage
from ..FinanceData.scraping import scrape_stock_data
from typing_extensions import TypedDict
from ..models import StockResearchData
from langgraph.graph import MessagesState
from .tools import ToolsManager

tools_manager = ToolsManager()
tools = tools_manager.get_tools()

class AgentState(TypedDict):
    ticker_symbol: str
    stock_price: float
    market_cap: str
    pe_ratio: float
    summary: str

def llm_call_agent(state: MessagesState):
    llm = ChatOpenAI(
            openai_api_key="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",
            openai_api_base="https://openrouter.ai/api/v1",
            model_name="deepseek/deepseek-r1:free",
        )

    if not llm.openai_api_key:
        return {"summary": "LLM API key not configured. Please set your OpenAI key to continue."}
    
    prompt = f'''
    You are a sophisticated agent that helps in investment research. Your task is to help the user find relevant information for investment opportunities, 
    including stocks and markets. The information that you should seek to supply includes but is not limited to:
    - stock price data
    - market sentiment
    - news and investor relations material
    - quantitative analysis 
    - qualitatitve analysi
    - government filings (e.g. SEC reports)
    
    Do not include disclaimers about your results not being financial advice; the user is already aware of that and just wants to 
    see your output for education purposes. '''

    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"summary": response.content}


def data_retrieval_agent(state: AgentState):
    ticker = state["ticker_symbol"]
    stock_data = scrape_stock_data(ticker)
    
    if stock_data:
        stock, created = StockResearchData.objects.update_or_create(
            ticker_symbol = ticker,
            defaults = stock_data
        )

        stock_price = stock_data['stock_price']
        market_cap = stock_data['market_cap']
        pe_ratio = stock_data['pe_ratio']

        return {
            "stock_price": stock_price, 
            "market_cap": market_cap, 
            "pe_ratio": pe_ratio
        }
    
    else: 
        return {
            "stock_price": None,
            "market_cap": None,
            "pe_ratio": None
        }
    

def analysis_agent(state: AgentState):
    llm = ChatOpenAI(
        openai_api_key="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",
        openai_api_base="https://openrouter.ai/api/v1",
        model_name="deepseek/deepseek-r1:free",
    )

    if not llm.openai_api_key:
        return {"summary": "LLM API key not configured. Please set your OpenAI key to continue."}
    
    ticker = state["ticker_symbol"]
    price = state["stock_price"]
    market_cap = state["market_cap"]
    pe_ratio = state["pe_ratio"]

    if not all([price, market_cap, pe_ratio]):
        return {"summary": "Error: could not retrive all financial data. Please check ticker symbol and data sources."}
    
    prompt = f'''
    Provide a very brief summary of the financial data for {ticker}. Current stock price: {price}, Market Cap: {market_cap}, P/E Ratio: {pe_ratio}.
    To the best of your ability, provide an analysis of what this data could mean. 
    Do not include any reasoning thoughts or other processing steps that are not relevant to the user'''

    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"summary": response.content}

def decide_next_step(state: AgentState):
    return "analysis"