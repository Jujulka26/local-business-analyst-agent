import pandas as pd
import matplotlib.pyplot as plt
from crewai.tools import tool

# Global data loading
df = pd.read_csv("tesla_stock_data.csv")
cols = df.columns.tolist()

@tool("analyze_data")
def analyze_data(python_code: str) -> str:
    """Executes a single line of Pandas code on 'df' for math/stats. Available columns: Date, Open, High, Low, Close, Volume."""
    try:
        code = str(python_code).replace("python", "").replace("```", "").strip()
        if code.startswith("print(") and code.endswith(")"):
            code = code[6:-1].strip()
        result = eval(code, {"df": df, "pd": pd})
        return f"Calculation Result: {result}"
    except Exception as e:
        return f"Math Error: {e}"

@tool("create_chart")
def create_chart(column_name: str) -> str:
    """Creates a line chart for a column in the Tesla stock dataset and saves it as chart.png. Pass the exact column name, e.g. 'Close'."""
    try:
        if column_name not in df.columns:
            return f"Column '{column_name}' not found. Available columns: {df.columns.tolist()}"
        plt.clf()
        plt.figure(figsize=(12, 5))
        plt.plot(df[column_name].values, color="blue")
        plt.title(f"{column_name} Price Trend")
        plt.xlabel("Day Index")
        plt.ylabel(column_name)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("chart.png")
        return "✅ Chart saved successfully as chart.png."
    except Exception as e:
        return f"Visual Error: {e}"
    
@tool("web_search")
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo for current news and information about a given query."""
    from langchain_community.tools import DuckDuckGoSearchRun
    return DuckDuckGoSearchRun().run(query)

@tool("scrape_website")
def scrape_website(url: str) -> str:
    """Scrapes and returns the visible text content from a given URL, including JavaScript-rendered content."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(3000)

            # Click each nav link, wait, then grab all text including hidden elements
            nav_links = page.query_selector_all("nav a, header a")
            all_text = ""
            visited = set()

            for i in range(len(nav_links)):
                try:
                    links = page.query_selector_all("nav a, header a")
                    label = links[i].inner_text().strip()
                    if not label or label in visited:
                        continue
                    visited.add(label)
                    links[i].click()
                    page.wait_for_timeout(2000)
                    # textContent gets ALL text including CSS-hidden elements
                    section_text = page.evaluate("document.body.textContent")
                    all_text += f"\n\n=== {label} ===\n{section_text.strip()}"
                except Exception:
                    continue

            browser.close()
            return all_text[:12000]
    except Exception as e:
        return f"Scrape Error: {e}"

stock_tools = [analyze_data, create_chart, web_search]