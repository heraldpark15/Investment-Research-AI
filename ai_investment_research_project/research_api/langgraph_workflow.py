from langgraph.graph import StateGraph, MessageGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage
from research_api.scraping import scrape_market_cap, scrape_pe_ratio, scrape_stock_price
from typing_extensions import TypedDict

class AgentState(TypedDict):
    ticker_symbol: str
    stock_price: float
    market_cap: str
    pe_ratio: float
    summary: str
    
def data_retrieval_agent(state: AgentState):
    ticker = state["ticker_symbol"]
    stock_price = scrape_stock_price(ticker)
    market_cap = scrape_market_cap(ticker)
    pe_ratio = scrape_pe_ratio(ticker)

    return {
        "stock_price": stock_price, 
        "market_cap": market_cap, 
        "pe_ratio": pe_ratio
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
    
    prompt = f"Provide a very brief summary of the financial data for {ticker}. Current stock price: {price}, Market Cap: {market_cap}, P/E Ratio: {pe_ratio}."
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"summary": response.content}

def decide_next_step(state: AgentState):
    return "analysis"
    

# Build LangGraph state graph
workflow = StateGraph(AgentState)

# Add nodes (agents)
workflow.add_node("data_retrieval", data_retrieval_agent)
workflow.add_node("analysis", analysis_agent)

# Set edges (flow of execution)
workflow.set_entry_point("data_retrieval")
workflow.add_conditional_edges( 
    "data_retrieval",
    decide_next_step,
    {
        "analysis": "analysis" 
    }
)
workflow.add_edge("analysis", END)

# Compile the graph to create the runnable workflow
basic_research_workflow = workflow.compile()