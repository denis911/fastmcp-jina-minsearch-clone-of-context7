from fastmcp import FastMCP

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
