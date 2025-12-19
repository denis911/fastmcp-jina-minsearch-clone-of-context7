import sys
import os
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
    if sys.platform == "win32":
        import msvcrt
        import io
        
        # Set stdin and stdout to binary mode to prevent shell transitions
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        
        # Wrap stdout to ensure UTF-8 encoding and LF newlines
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, 
            encoding='utf-8', 
            newline='\n', 
            write_through=True
        )
        sys.stdin = io.TextIOWrapper(
            sys.stdin.buffer, 
            encoding='utf-8', 
            newline='\n'
        )

    mcp.run(show_banner=False)

    