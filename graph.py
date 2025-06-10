import os
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AnyMessage, RemoveMessage
from langchain_openai import AzureChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.prompts import PromptTemplate
from tools import search_movies_using_vector

tools = [
    search_movies_using_vector,
]

prompt = PromptTemplate.from_template("""You are a helpful assistant that can help find movies based on the descriptions provided by the user.
You should use the tools provided to search movies using the query provided by the user.
You should respond with the most relevant movie information based on the user's query and the tool results.
The tool results may not be accurate, so you should use your best judgment to provide the most relevant information.
User Query: {query}
""")

class State(TypedDict):
    """
    Represents the state of the agent.
    """
    messages: Annotated[list[AnyMessage], add_messages]
    
def clean_messages(state: State) -> State:
    """
    Cleans the messages in the state except for the last one.
    Args:
        state (State): The current state of the agent.
    Returns:
        state (State): The updated state with only the last message retained.
    """
    messages = state["messages"]
    last_message = messages[-1]
    rest_messages = messages[:-1] if len(messages) > 1 else []
    
    return {"messages": [RemoveMessage(id=m.id) for m in rest_messages] + [last_message]}

def chatbot(state: State) -> str:
    """
    Contacts LLM to get a response based on the current state.
    Args:
        state (State): The current state of the agent.
    Returns:
        state (State): The updated state with the response.
    """
    params = {
        "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
        "azure_deployment": os.getenv("AZURE_DEPLOYLMENT"),
        "api_version": os.getenv("MODEL_API_VERSION"),
        "api_key": os.getenv("AZURE_API_KEY"),
        "timeout": 60,
    }
    model = AzureChatOpenAI(**params)
    model_with_tools = model.bind_tools(tools)
    chain = {"query": RunnablePassthrough()} | prompt | model_with_tools
    
    messages = state["messages"]
    response = chain.invoke(messages)
    return { "messages": [response] }

builder = StateGraph(State)

builder.add_node('clean_messages', clean_messages)
builder.add_node('chatbot', chatbot)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, 'clean_messages')
builder.add_edge("clean_messages", "chatbot")
builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
builder.add_edge("tools", "chatbot")
builder.add_edge('chatbot', END)

graph = builder.compile()