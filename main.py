import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

if not os.environ.get("GROQ_API_KEY"):
    raise ValueError(
        "GROQ_API_KEY is missing! Please set it in your environment variables "
        "or create a .env file in this directory with GROQ_API_KEY=your_key"
    )

# 1. Define Custom Tools using @tool decorator
@tool
def calculate_shipping_cost(weight_kg: float, distance_km: float) -> str:
    """Calculate the shipping cost based on package weight in kg and distance in km."""
    base_rate = 5.0
    cost = base_rate + (weight_kg * 1.5) + (distance_km * 0.05)
    return f"The estimated shipping cost is ${cost:.2f}"

@tool
def get_product_stock(product_name: str) -> str:
    """Check the inventory stock level for a given product name."""
    inventory = {
        "sony wh-1000xm5": "In Stock (15 units available)",
        "logitech mx master 3s": "Low Stock (3 units available)",
        "mechanical keyboard": "Out of Stock"
    }
    
    clean_name = product_name.lower().strip()
    for item, status in inventory.items():
        if item in clean_name:
            return f"Stock status for '{product_name}': {status}"
    
    return f"Product '{product_name}' was not found in the inventory database."

tools = [calculate_shipping_cost, get_product_stock]
tools_map = {tool.name: tool for tool in tools}


# 2. Autonomous Agent Execution Loop
def run_autonomous_agent(query: str):
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.0,
        groq_api_key=os.environ.get("GROQ_API_KEY")
    )

    llm_with_tools = llm.bind_tools(tools)
    messages = [HumanMessage(content=query)]
    
    response = llm_with_tools.invoke(messages)
    messages.append(response)
    
    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]
            
            print(f"\n[Autonomous Agent calling tool -> '{tool_name}' with args: {tool_args}]")
            
            selected_tool = tools_map[tool_name]
            tool_result = selected_tool.invoke(tool_args)
            messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_id))
        
        final_response = llm_with_tools.invoke(messages)
        return final_response.content
    else:
        return response.content

if __name__ == "__main__":
    print("--- Autonomous Agent Initialized ---")

    query_1 = "Can you check if the Logitech MX Master 3S is currently in stock?"
    print(f"\nUser Query: {query_1}")
    output_1 = run_autonomous_agent(query_1)
    print(f"Agent Response:\n{output_1}")

    query_2 = "How much will it cost to ship a 2.5 kg package across a distance of 450 km?"
    print(f"\nUser Query: {query_2}")
    output_2 = run_autonomous_agent(query_2)
    print(f"Agent Response:\n{output_2}")