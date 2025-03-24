from langchain_anthropic import ChatAnthropic
from langchain.schema.messages import AIMessage
from .tools import ToolsManager
from langchain.prompts import ChatPromptTemplate
from typing import List, Optional, Union
from typing_extensions import TypedDict
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

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
    next_steps: Optional[str] = None
    is_valid: bool
    chat_history: List[str]

# --- Agent Components ---
current_date = datetime.date.today().isoformat()

llm = ChatAnthropic(
    anthropic_api_key= os.environ.get("ANTHROPIC_API_KEY"),
    model_name="claude-3-7-sonnet-20250219",  
    temperature=0.7, 
    max_tokens=500, 
)
# 1. Input Validation Agent
validation_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a strict input validation agent for an investment research system. Your task is to determine whether the user's input is a valid investment research query. "
            "If the input is too vague, irrelevant, or off-topic, you must respond with an explanation and request a more specific query. "
            "If the input is valid, simply respond with 'valid'.\n"
            "Examples:\n"
            "- Input: 'Tell me a joke' → Response: 'Your query is not related to investment research. Please ask about a company, sector, or trend you want to analyze.'\n"
            "- Input: 'Is Tesla a good investment in 2025?' → Response: 'valid'\n"
            f"Current Date: {current_date}. You MUST use the provided current date above. Do NOT rely on any other date information."
            "If chat history is avaible, use it as context for the current input."
        ),
        ("human", "User Query: {input}, Chat History: {chat_history}"),
    ]
)

validation_agent = validation_prompt_template | llm

# 2. Information Gathering Agent
information_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert information retriever. Your goal is to gather the necessary information to answer the user's investment research query."
            "You have access to the following tools:\n{tool_descriptions}"
            f"Current Date: {current_date}. You MUST use the provided current date above. Do NOT rely on any other date information."
            "If chat history is avaible, use it as context for the current input."
        ),
        ("human", "{input}\n\nUse the available tools if necessary to find relevant information. Chat history: {chat_history}"),
    ]
)


information_prompt = information_prompt_template.partial(
    tool_descriptions="\n".join([f"- {tool.name}: {tool.description}" for tool in tools])
)

llm_with_tools = llm.bind_tools(tools)
information_agent = information_prompt | llm_with_tools

# 3. Investment Analyst Agent
analysis_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a seasoned investment analyst. You will receive information gathered by another agent. Your task is to analyze this information, synthesize insights, and provide a comprehensive answer to the user's initial investment research query. Be creative and think step-by-step in your analysis."
            f"Current Date: {current_date}. You MUST use the provided current date above. Do NOT rely on any other date information."
            "If chat history is avaible, use it as context for the current input."
        ),
        ("human", "Here is the information gathered: {information}\n\nBased on this, provide your analysis and insights regarding the original query: {original_query}. Chat history: {chat_history}"),
    ]
)

analysis_prompt = analysis_prompt_template

analysis_agent = analysis_prompt | llm

# 4. Evaluation Agent
evaluation_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an information evaluation agent. Your task if to determine if the provided information is sufficient to answer the user's query."
            f"Current Date: {current_date}. You MUST use the provided current date above. Do NOT rely on any other date information."
            "If chat history is avaible, use it as context for the current input."
        ),
        (
            "human",
            "User Query: {original_query}, Chat History: {chat_history}\n\nInformation Gathered: {information}\n\nIs the information sufficient to answer the user's query? Answer 'yes' or 'no'.",
        ),
    ]
)

evaluation_prompt = evaluation_prompt_template

evaluation_agent = evaluation_prompt | llm

# 5. Next Steps Suggestion Agent
next_steps_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant that helps users explore related investment research questions."
            "Based on the provided analysis, suggest follow-up questions or next steps the user can take."
            "Make sure the suggestions are actionable and relevant to the original query."
            "Return an array with each question as an element in the array. No other information is necessary"
            "Each question should be in markdown form so that it can be clearly rendered using React Markdown"
            f"Current Date: {current_date}. You MUST use the provided current date above. Do NOT rely on any other date information."
            "If chat history is avaible, use it as context for the current input."
        ),
        (
            "human",
            "Original Query: {original_query}, Chat History: {chat_history}\n\nAnalysis Result: {analysis_result}\n\n"
            "Based on this, suggest 3 related questions or next steps for further research.",
        ),
    ]
)

next_steps_prompt = next_steps_prompt_template
next_steps_agent = next_steps_prompt | llm

# --- Define the LangGraph Workflow ---
MAX_ITERATIONS = 1
WINDOW_SIZE = 3

def validate_input(state: AgentState):
    print("VS")
    print(type(state["chat_history"]))
    result = validation_agent.invoke({"input": state["input"], "chat_history": state["chat_history"]})

    if result.content.lower() != 'valid':
        print("Not valid")
        new_history = state["chat_history"] + [f"User: {state['input']}", f"Bot: {result.content}"]

        if len(new_history) > WINDOW_SIZE * 2: #2 messages per turn.
            new_history = new_history[-WINDOW_SIZE * 2:]
        return {"agent_outcome": result, "is_valid": False, "chat_history": new_history} 
    else:
        print("IS valid")
        return {"is_valid": True} 
    
def is_valid_input(state: AgentState):
    if state["is_valid"]: 
        return "valid"
    else:
        print("invalid")
        return "invalid"

def should_gather_information(state: AgentState):
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
    print("Analyze info")
    result = analysis_agent.invoke({"information": state["information"], "original_query": state["input"], "chat_history": state["chat_history"]})
    
    new_history = state["chat_history"] + [f"Bot: {result.content}"]

    if len(new_history) > WINDOW_SIZE * 2: #2 messages per turn.
        new_history = new_history[-WINDOW_SIZE * 2:]

    return {"agent_outcome": result, "chat_history": new_history}

def get_information(state: AgentState):
    print("Get information")
    result = information_agent.invoke({"input": state["input"], "chat_history": state["chat_history"]})
    
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

def suggest_next_steps(state: AgentState):
    print("Suggest next steps")
    result = next_steps_agent.invoke(
        {"original_query": state["input"], "analysis_result": state["agent_outcome"].content, "chat_history": state["chat_history"]}
    )
    print(type(result.content))
    return ({"next_steps": result.content})