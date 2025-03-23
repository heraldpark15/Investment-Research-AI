from langgraph.graph import StateGraph, END, START
from .agents import get_information, analyze_information, should_gather_information, is_valid_input, suggest_next_steps, validate_input, AgentState
from IPython.display import Image, display

# Create the LangGraph builder
builder = StateGraph(AgentState)

# Add nodes
builder.add_node("validate_input", validate_input)
builder.add_node("gather_information", get_information)
builder.add_node("analyze", analyze_information)
builder.add_node("suggest_next_steps", suggest_next_steps)

# Add edges
builder.set_entry_point("validate_input")
builder.add_conditional_edges(
    "validate_input",
    is_valid_input,
    {"valid": "gather_information", "invalid": END}
)
builder.add_conditional_edges(
    "gather_information",
    should_gather_information,
    {"gather_information": "gather_information", "analyze": "analyze"},
)
builder.add_edge("analyze", "suggest_next_steps")
builder.add_edge("suggest_next_steps", END)

# Compile the graph
investment_research_workflow = builder.compile()