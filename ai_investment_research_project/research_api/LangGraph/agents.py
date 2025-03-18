# agents.py
from langchain_anthropic import ChatAnthropic
from langchain.schema.messages import HumanMessage, AIMessage
from langgraph.graph import MessagesState
from .tools import ToolsManager
from langchain.prompts import ChatPromptTemplate
from typing import Dict, List, Optional, Union
from typing_extensions import TypedDict

tools_manager = ToolsManager()
tools = tools_manager.get_tools()

class AgentState(TypedDict):
    input: str
    intermediate_steps: List[tuple[str, str]] = []
    agent_outcome: Union[AIMessage, None] = None
    information: Optional[str] = None
    original_query: str
    conversation_id: Optional[str] = None
    iteration_count: int = 0

# --- Agent Components ---

# 1. Information Gathering Agent
information_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert information retriever. Your goal is to gather the necessary information to answer the user's investment research query."
            "You have access to the following tools:\n{tool_descriptions}",
        ),
        ("human", "{input}\n\nUse the available tools if necessary to find relevant information."),
    ]
)

llm = ChatAnthropic(
    anthropic_api_key="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",  
    model_name="claude-3-7-sonnet-20250219",  
    temperature=0.7, 
    max_tokens=1000, 
)

information_prompt = information_prompt_template.partial(
    tool_descriptions="\n".join([f"- {tool.name}: {tool.description}" for tool in tools])
)

llm_with_tools = llm.bind_tools(tools)
information_agent = information_prompt | llm_with_tools

# 2. Investment Analyst Agent
analysis_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a seasoned investment analyst. You will receive information gathered by another agent. Your task is to analyze this information, synthesize insights, and provide a comprehensive answer to the user's initial investment research query. Be creative and think step-by-step in your analysis.",
        ),
        ("human", "Here is the information gathered: {information}\n\nBased on this, provide your analysis and insights regarding the original query: {original_query}"),
    ]
)

analysis_prompt = analysis_prompt_template

analysis_agent = analysis_prompt | llm

# 3. Evaluation Agent
evaluation_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an information evaluation agent. Your task if to determine if the provided information is sufficient to answer the user's query.",
        ),
        (
            "human",
            "User Query: {original_query}\n\nInformation Gathered: {information}\n\nIs the information sufficient to answer the user's query? Answer 'yes' or 'no'.",
        ),
    ]
)

evaluation_prompt = evaluation_prompt_template

evaluation_agent = evaluation_prompt | llm

# --- Define the LangGraph Workflow ---
MAX_ITERATIONS = 1

def should_gather_information(state: AgentState):
    """Decide whether to gather more information or proceed to analysis."""
    if state["iteration_count"] >= MAX_ITERATIONS:
        return "analyze"  # Reached iteration limit, proceed to analysis

    evaluation_result = evaluation_agent.invoke(
        {"original_query": state["input"], "information": state["information"]}
    )
    if "yes" in evaluation_result.content.lower():
        return "analyze"
    else:
        return "gather_information"
    
def analyze_information(state: AgentState):
    """Analyzes the gathered information."""
    result = analysis_agent.invoke({"information": state["information"], "original_query": state["input"]})
    return {"agent_outcome": result}

def get_information(state: AgentState):
    """Gathers information using the information gathering agent."""
    result = information_agent.invoke({"input": state["input"]})
    
    # Extract text content and tool calls
    text_content = ""
    tool_calls = []
    
    if isinstance(result, AIMessage):
        if isinstance(result.content, list):
            for item in result.content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        text_content += item.get("text", "")
                    elif item.get("type") == "tool_use":
                        tool_calls.append(item)
        else:
            text_content = result.content
        
        # Also check for tool_calls attribute
        if hasattr(result, 'tool_calls') and result.tool_calls:
            tool_calls.extend(result.tool_calls)
    else:
        text_content = str(result)
    
    # Process tool calls if any
    tool_results = []
    for tool_call in tool_calls:
        tool_name = tool_call.get('name')
        tool_args = tool_call.get('args', {})
        
        # Find the matching tool
        tool = next((t for t in tools if t.name == tool_name), None)
        if tool:
            try:
                # Execute the tool
                tool_result = tool.invoke(tool_args)
                tool_results.append(f"Tool '{tool_name}' result: {tool_result}")
            except Exception as e:
                tool_results.append(f"Tool '{tool_name}' error: {str(e)}")
    
    # Combine text content and tool results
    combined_info = text_content + "\n\n" + "\n".join(tool_results) if tool_results else text_content
    
    return {"information": combined_info, "iteration_count": state["iteration_count"] + 1}