from crewai import Agent, Task, Crew, Process
from tools import stock_tools, scrape_website

local_llm = "ollama/gemma4:e2b"

# ── STOCK ANALYSIS CREW ──────────────────────────────────────────────────────

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
    tools=[stock_tools[2]],
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

reporter = Agent(
    role='Stock Report Writer',
    goal='Combine numerical analysis, news, and chart confirmation into one clear analyst report.',
    backstory=(
        'You are a senior financial writer at a research firm. '
        'You receive raw data findings, a news update, and a chart status, '
        'then write a clean 1-page analyst report. '
        'Always include a disclaimer that this is a demo portfolio project, not real investment advice.'
    ),
    tools=[],
    llm=local_llm,
    verbose=True
)

# ── STANDALONE DEMO AGENT ────────────────────────────────────────────────────

resume_scraper = Agent(
    role='Content Storyteller',
    goal='Scrape a website and retell its content as an engaging short story.',
    backstory='You are a creative writer. When given a website, you scrape it and craft a flowing narrative that captures the essence of what you found, like a story telling.',
    tools=[scrape_website],
    llm=local_llm,
    verbose=True
)

# ── TASKS ────────────────────────────────────────────────────────────────────

math_task = Task(
    description="Find the average, highest, and lowest closing price of Tesla in this dataset.",
    expected_output="Three numerical values: average, highest, and lowest closing price with brief labels.",
    agent=researcher
)

news_task = Task(
    description="Search for the most recent Tesla news available. Pick the latest article you can find regardless of when it was published. Include the date and time of the article if available.",
    expected_output="The headline, publication date/time, source, and a 2-sentence summary of what happened.",
    agent=news_analyst
)

chart_task = Task(
    description="Generate a line chart of the Closing price trend.",
    expected_output="Confirmation that chart.png is saved.",
    agent=designer
)

report_task = Task(
    description=(
        "Using the outputs from the researcher, news analyst, and designer, "
        "write a concise 1-page Tesla stock analyst report. "
        "Structure it with sections: Summary, Key Numbers, Latest News, Chart, and Disclaimer."
    ),
    expected_output="A clean, structured 1-page analyst report in plain text.",
    agent=reporter,
    context=[math_task, news_task, chart_task]
)

resume_task = Task(
    description="Scrape the content at https://jujulka26.github.io/my-resume-angular/ and write a story that summarizes the content.",
    expected_output="A short story that captures the key points obtained in the scraped content, only in one paragraph.",
    agent=resume_scraper
)

# ── CREWS ────────────────────────────────────────────────────────────────────

stock_crew = Crew(
    agents=[researcher, news_analyst, designer, reporter],
    tasks=[math_task, news_task, chart_task, report_task],
    process=Process.sequential
)

resume_crew = Crew(
    agents=[resume_scraper],
    tasks=[resume_task],
)

if __name__ == "__main__":
    print("🚀 Running Tesla Stock Analysis...")
    result = stock_crew.kickoff()
    print("\n\n########################")
    print("## ANALYST REPORT ##")
    print(result)
