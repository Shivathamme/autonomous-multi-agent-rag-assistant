# Import DuckDuckGo search tool (no API key needed)
# from duckduckgo_search import DDGS
from ddgs import DDGS
# Import time module to add delay
import time


# Function to perform web search
def web_search(query: str, max_results: int = 5) -> str:
    try:
        # 🔹 Create empty list to store formatted results
        results = []

        # 🔹 Start DuckDuckGo search session
        with DDGS() as ddgs:

            # 🔹 Small delay to avoid rate limiting / blocking
            time.sleep(1)

            # 🔹 Perform search and convert results to list
            data = list(ddgs.text(query, max_results=max_results))

        # 🔹 If no results found → return empty string
        if not data:
            return ""

        # 🔹 Loop through each search result
        for i, r in enumerate(data, 1):
            # Extract title (if missing → empty string)
            title = r.get("title", "")

            # Extract description/snippet
            body = r.get("body", "")

            # Extract link/source URL
            link = r.get("href", "")

            # 🔹 Format result in readable way and add to list
            results.append(f"{i}. {title}\n{body}\nSource: {link}")

        # 🔹 Combine all results into one string (separated by blank lines)
        return "\n\n".join(results)

    except Exception as e:
        # 🔴 If any error occurs → print error (for debugging)
        print("Web search error:", e)

        # 🔹 Return empty string to avoid breaking system
        return ""