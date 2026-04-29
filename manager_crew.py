from crewai import Agent, Task, Crew, Process
from tools import stock_tools

# 1. THE BRAIN (Modern 2026 Way)
# By using the string "ollama/gemma4:e2b", you avoid the Pydantic validation error!
local_llm = "ollama/gemma4:e2b"

# 2. THE AGENTS
researcher = Agent(
    role='Financial Researcher',
    goal='Provide accurate numerical analysis of Tesla stock.',
    backstory='You are a mathematical genius focused on data precision.',
    tools=stock_tools,
    llm=local_llm,
    verbose=True
)

news_analyst = Agent(
    role='Market News Analyst',
    goal='Find the latest real-world news affecting Tesla.',
    backstory='You are a sharp financial journalist who uses the web to find breaking news.',
    tools=[stock_tools[2]], # search_tool (DuckDuckGo)
    llm=local_llm,
    verbose=True
)

designer = Agent(
    role='Graphic Designer',
    goal='Create visual representations of stock trends.',
    backstory='You translate raw numbers into clear, professional PNG charts.',
    tools=stock_tools,
    llm=local_llm,
    verbose=True
)

# 3. THE TASKS (Same as before)
math_task = Task(
    description="What is the average closing price of Tesla in this dataset?",
    expected_output="A single numerical value with a short explanation.",
    agent=researcher
)

news_task = Task(
    description="Use the DuckDuckGo search tool to find one recent news headline about Tesla today.",
    expected_output="A short paragraph containing the live news headline and a brief summary.",
    agent=news_analyst
)

chart_task = Task(
    description="Generate a line chart of the Closing price trend.",
    expected_output="Confirmation that chart.png is saved.",
    agent=designer
)

# 4. THE CREW
manager_crew = Crew(
    agents=[researcher, news_analyst, designer],
    tasks=[math_task, news_task, chart_task],
    process=Process.sequential 
)

if __name__ == "__main__":
    print("🚀 Crew is starting work with Gemma 4 e2b...")
    result = manager_crew.kickoff()
    print("\n\n########################")
    print("## FINAL REPORT ##")
    print(result)