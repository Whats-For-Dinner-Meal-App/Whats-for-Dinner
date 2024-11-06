from typing import Annotated, Literal, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
# Langgraph imports
from langgraph.prebuilt import create_react_agent, ToolNode
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get tavily search api key
if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

## Build the Agents tools
@tool
def searchWeb(query: str): # Travily Search
    '''Search the web for the query'''
    search = TavilySearchResults(max_results=3)
    return search.invoke(query)

@tool
def query_database(): # Database Search
    '''Query database for recipes the human already has'''
    return {'name': 'Creamy Tuscan Chicken', 'ingredients': 'chicken, garlic, spinach, sun-dried tomatoes, heavy cream, parmesan cheese', 'instructions': '1. Season the chicken with salt and pepper. 2. Heat the oil in a large skillet over medium-high heat. 3. Add the chicken and cook until golden brown on both sides. 4. Remove the chicken from the skillet and set aside. 5. Add the garlic to the skillet and cook until fragrant. 6. Add the spinach and sun-dried tomatoes and cook until the spinach is wilted. 7. Add the heavy cream and parmesan cheese and bring to a simmer. 8. Return the chicken to the skillet and cook until the sauce has thickened. 9. Serve the chicken with the sauce.'}

@tool
def query_pantry(): # Pantry Search
    '''Query pantry for ingredients the human already has'''
    return ['chicken', 'garlic', 'spinach', 'sun-dried tomatoes', 'heavy cream', 'parmesan cheese']

tools = [searchWeb, query_database]
tool_node = ToolNode(tools)

model = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("GPT_API_KEY")).bind_tools(tools)

# Define the function that determines whether to continue or not
def should_continue(state: MessagesState) -> Literal["tools", END]: # type: ignore
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END


# Define the function that calls the model
def call_model(state: MessagesState):
    messages = state['messages']
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

def ceate_agent():
    # Define a new graph
    workflow = StateGraph(MessagesState)
    # Add the nodes
    workflow.add_node('agent', call_model)
    workflow.add_node('tools', tool_node)

    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.add_edge(START, 'agent')

    # We now add a conditional edge
    workflow.add_conditional_edges(
        # First, we define the start node. We use `agent`.
        # This means these are the edges taken after the `agent` node is called.
        "agent",
        # Next, we pass in the function that will determine which node is called next.
        should_continue,
    )

    # We now add a normal edge from `tools` to `agent`.
    # This means that after `tools` is called, `agent` node is called next.
    workflow.add_edge("tools", 'agent')

    # Initialize memory to persist state between graph runs
    checkpointer = MemorySaver()

    # Finally, we compile it!
    # This compiles it into a LangChain Runnable,
    # meaning you can use it as you would any other runnable.
    # Note that we're (optionally) passing the memory when compiling the graph
    sousChef = workflow.compile(checkpointer=checkpointer)
    return sousChef

def main():
    sousChef = ceate_agent()
    while True:
        print('Enter "q" to quit.')
        query = input("Sous-Chef here! What can I help you with today? ")
        if query == 'q':
            break
        # Use the Runnable
        final_state = sousChef.invoke(
            {"messages": [HumanMessage(content=query)]},
            config={"configurable": {"thread_id": 42}}
        )
        print(final_state["messages"][-1].content)

if __name__ == "__main__":
    main()