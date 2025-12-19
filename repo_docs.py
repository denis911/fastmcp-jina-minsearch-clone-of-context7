import sys

# Redirect stdout to stderr BEFORE importing FastMCP
# This prevents the banner from contaminating the MCP protocol stream
_original_stdout = sys.stdout
sys.stdout = sys.stderr

from fastmcp import FastMCP

# Restore stdout after import for MCP protocol communication
sys.stdout = _original_stdout

mcp = FastMCP("Repo_docs")

def _scrape_web_page_logic(url: str) -> str:
    import requests
    jina_url = f"https://r.jina.ai/{url}"
    response = requests.get(jina_url)
    return response.text

@mcp.tool
def scrape_web_page(url: str) -> str:
    """
    Scrape the content of a web page and return it in Markdown format.
    
    Args:
        url: The URL of the web page to scrape.
    """
    return _scrape_web_page_logic(url)

if __name__ == "__main__":
    mcp.run()

    