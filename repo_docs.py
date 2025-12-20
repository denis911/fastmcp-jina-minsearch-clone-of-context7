import sys
import os
import requests
import zipfile
import io
import minsearch
from typing import List, Dict, Optional

# Ensure no binary mode issues on Windows without corrupting the stream
if sys.platform == "win32":
    import msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

from fastmcp import FastMCP

mcp = FastMCP("Repo_docs")

# In-memory cache for indices
# Key: ZIP URL, Value: minsearch.Index
_repo_indices: Dict[str, minsearch.Index] = {}

def _get_index_for_repo(url: str) -> minsearch.Index:
    """Download, extract, and index a repository if not already cached."""
    if url in _repo_indices:
        return _repo_indices[url]

    response = requests.get(url)
    response.raise_for_status()
    
    documents = []
    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        for file_info in zf.infolist():
            if file_info.filename.endswith(('.md', '.mdx')):
                # Remove the first part of the path (root dir in GitHub ZIPs)
                parts = file_info.filename.split('/')
                clean_filename = '/'.join(parts[1:]) if len(parts) > 1 else file_info.filename
                
                with zf.open(file_info) as f:
                    try:
                        content = f.read().decode('utf-8')
                        documents.append({
                            'filename': clean_filename,
                            'content': content
                        })
                    except UnicodeDecodeError:
                        continue # Skip non-unicode files

    index = minsearch.Index(
        text_fields=['content'],
        keyword_fields=['filename']
    )
    index.fit(documents)
    _repo_indices[url] = index
    return index

def _scrape_web_page_logic(url: str) -> str:
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

@mcp.tool
def search_repo_docs(url: str, query: str, num_results: int = 5) -> List[Dict]:
    """
    Search for information within a repository's documentation (Markdown files).
    The tool downloads the repository ZIP, indexes its .md/.mdx files, and searches them.
    
    Args:
        url: The direct download URL for the repository's ZIP file (e.g., from GitHub).
        query: The search query.
        num_results: Number of results to return (default 5).
    """
    index = _get_index_for_repo(url)
    results = index.search(query=query, num_results=num_results)
    return results

if __name__ == "__main__":
    mcp.run(show_banner=False)

    