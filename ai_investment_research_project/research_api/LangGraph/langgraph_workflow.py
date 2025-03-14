from langgraph.graph import StateGraph, END, START
from .agents import data_retrieval_agent, analysis_agent,decide_next_step, AgentState
from IPython.display import Image, display

# Build LangGraph state graph
workflow = StateGraph(AgentState)

# Add nodes (agents)
workflow.add_node("data_retrieval", data_retrieval_agent)
workflow.add_node("analysis", analysis_agent)

# Set edges (flow of execution)
workflow.add_edge(START, "data_retrieval")
workflow.set_entry_point("data_retrieval")
workflow.add_conditional_edges( 
    "data_retrieval",
    decide_next_step,
    {
        "analysis": "analysis",
        END: END
    }
)
workflow.add_edge("analysis", END)

# Compile the graph to create the runnable workflow
basic_research_workflow = workflow.compile()