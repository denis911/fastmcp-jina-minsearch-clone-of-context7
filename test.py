import requests
import re
from repo_docs import _scrape_web_page_logic as scrape_web_page

def count_data(text):
    """Count occurrences of 'data' case-insensitively."""
    return len(re.findall(r'data', text, re.IGNORECASE))

def run_test():
    url = "https://datatalks.club/"
    print(f"Target URL: {url}\n")

    # Run 1: Standard Python download (using requests directly)
    print("--- Run 1: Python download (requests) ---")
    try:
        # Use the same jina wrapper for consistency or just requests?
        # The user said "download it and count all words 'data' using python"
        # and "use mcp server ... count it from your mcp download".
        # To make them "the same", they should probably both use the same source (jina).
        jina_url = f"https://r.jina.ai/{url}"
        resp = requests.get(jina_url)
        resp.raise_for_status()
        python_content = resp.text
        python_count = count_data(python_content)
        print(f"Content length: {len(python_content)}")
        print(f"Count of 'data': {python_count}")
    except Exception as e:
        print(f"Error in Run 1: {e}")
        python_count = None

    # Run 2: Using the logic intended for the MCP server
    print("\n--- Run 2: MCP Logic download ---")
    try:
        mcp_content = scrape_web_page(url)
        mcp_count = count_data(mcp_content)
        print(f"Content length: {len(mcp_content)}")
        print(f"Count of 'data': {mcp_count}")
    except Exception as e:
        print(f"Error in Run 2: {e}")
        mcp_count = None

    print("\n--- Comparison ---")
    if python_count is not None and mcp_count is not None:
        if python_count == mcp_count:
            print(f"SUCCESS: Both counts are the same ({python_count}).")
        else:
            print(f"DIFFERENCE: Python count is {python_count}, MCP Logic count is {mcp_count}.")
    else:
        print("Comparison failed due to errors.")

if __name__ == "__main__":
    run_test()

