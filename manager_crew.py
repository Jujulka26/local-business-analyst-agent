from crewai import Agent, Task, Crew, Process
from tools import stock_tools, scrape_website

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

resume_scraper = Agent(
    role='Content Storyteller',
    goal='Scrape a website and retell its content as an engaging short story.',
    backstory='You are a creative writer. When given a website, you scrape it and craft a flowing narrative that captures the essence of what you found, like a story telling.',
    tools=[scrape_website],
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

resume_task = Task(
    description="Scrape the content at https://jujulka26.github.io/my-resume-angular/ and write a story that summarizes the content.",
    expected_output="A short story that captures the key points obtained in the scraped content, only in one paragraph.",
    agent=resume_scraper
)

# 4. THE CREW
manager_crew = Crew(
    agents=[resume_scraper, researcher, news_analyst, designer],
    tasks=[resume_task, math_task, news_task, chart_task],
    process=Process.sequential
)

if __name__ == "__main__":
    test_crew = Crew(
    agents=[resume_scraper],
    tasks=[resume_task],
    )
    print("🚀 Crew is starting work with Gemma 4 e2b...")
    result = test_crew.kickoff()
    print("\n\n########################")
    print("## FINAL REPORT ##")
    print(result)