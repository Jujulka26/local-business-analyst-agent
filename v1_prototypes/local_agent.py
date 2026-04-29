import pandas as pd
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage

# --- 1. SETUP ---
CSV_FILENAME = "tesla_stock_data.csv"
df = pd.read_csv(CSV_FILENAME)
columns_list = df.columns.tolist()

# --- 2. THE TOOL ---
@tool
def analyze_data(python_code: str):
    """
    Executes a single line of Python/Pandas code on 'df'.
    Available Columns: {columns_list}
    Example: df['Close'].mean()
    """
    # Gemma 4 is much cleaner, but we keep a basic safety check
    code = python_code.replace("python", "").replace("```", "").strip()
    try:
        result = eval(code, {"df": df, "pd": pd})
        return f"Calculation Result: {result}"
    except Exception as e:
        return f"Error: {e}. Check if you used the correct columns: {columns_list}"

# --- 3. SWITCH TO GEMMA 4 E2B ---
# We use the 'gemma4:e2b' model here
llm = ChatOllama(model="gemma4:e2b", temperature=0)
llm_with_tools = llm.bind_tools([analyze_data])

# --- 4. EXECUTION ---
def run_analyst(question):
    print(f"\n🚀 Question: {question}")
    
    messages = [
        SystemMessage(content=(
            "You are a Senior Financial Analyst. Use the 'analyze_data' tool "
            "to answer questions by writing precise Pandas code. "
            f"The data in 'df' has these columns: {columns_list}. "
            "Respond ONLY with the tool call."
        )),
        HumanMessage(content=question)
    ]
    
    # Gemma 4 will "Think" internally before responding
    response = llm_with_tools.invoke(messages)

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        # Gemma 4 usually provides the argument directly
        code_input = tool_call['args'].get('python_code', '')
        print(f"🧐 Gemma Thinking... Code: {code_input}")
        
        observation = analyze_data.invoke(tool_call['args'])
        print(f"📊 {observation}")
    else:
        print(f"💬 Agent Response: {response.content}")

if __name__ == "__main__":
    run_analyst("What is the average closing price of Tesla?")
    run_analyst("Which day had the highest trading volume?")