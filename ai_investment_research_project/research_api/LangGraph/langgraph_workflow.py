from langgraph.graph import StateGraph, END, START
from .agents import get_information, analyze_information, should_gather_information, AgentState
from IPython.display import Image, display

# Create the LangGraph builder
builder = StateGraph(AgentState)

# Add nodes
builder.add_node("gather_information", get_information)
builder.add_node("analyze", analyze_information)

# Add edges
builder.set_entry_point("gather_information")
builder.add_conditional_edges(
    "gather_information",
    should_gather_information,
    {"gather_information": "gather_information", "analyze": "analyze"},
)
builder.add_edge("analyze", END)

# Compile the graph
investment_research_workflow = builder.compile()