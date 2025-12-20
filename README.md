# Repo Docs MCP: Secure & Flexible Documentation Search

**Repo Docs MCP** is a powerful tool designed to bridge the gap between large-scale AI models (like Antigravity) and technical documentation. It allows you to download, index, and search through any repository's documentation (Markdown/MDX files) using a minimalistic but highly efficient search engine.

## 🚀 Business Value & Use Cases

In modern AI-driven development, access to high-quality documentation is critical. While online services like Context7 are excellent for public projects, businesses often face challenges with:

1.  **Proprietary Documentation**: Internal company docs, private SDKs, and enterprise knowledge bases cannot be shared with public indexing services due to privacy and security policies.
2.  **Air-Gapped Environments**: Some development workflows require offline access to documentation.
3.  **Context Precision**: LLMs work best when provided with the *most relevant* snippets rather than overwhelming amounts of irrelevant text.

**Repo Docs MCP** solves these by providing:
- **Local Control**: You can run the indexing and search entirely on your own infrastructure.
- **Privacy First**: Support for local ZIP files ensures that sensitive project documentation never leaves your machine.
- **Fast Iteration**: In-memory caching ensures that repetitive queries across a repository are instantaneous.

## 🛠️ Key Components

### 1. `repo_docs.py` (The MCP Server)
The primary interface for AI agents like Antigravity. It exposes the `search_repo_docs` tool, which can download a repository ZIP from GitHub (or any URL), index its documentation, and return the most relevant snippets based on a query.

### 2. `search.py` (The Standalone Script)
A flexible script for local usage. It's ideal for:
- Manual testing of the search engine.
- Searching through documentation on your local PC.
- Integrating with custom workflows where a full MCP server isn't required.

## 🔧 Practical Installation

### Prerequisites
- [Python 3.13+](https://www.python.org/)
- [`uv`](https://github.com/astral-sh/uv) (recommended package manager)

### Setup
Clone the repository and install dependencies:
```bash
uv sync
```

### Running the MCP Tool
To use it with Antigravity or other MCP-compatible clients:
```bash
uv run repo_docs.py
```

### Running the Standalone Search
To test indexing and searching locally:
```bash
uv run search.py
```

## 🤖 Usage with Antigravity

Update your Antigravity config in the `mcp_config.json` file:
```json
{
    "mcpServers":  {
                       "repo_docs":  {
                                         "args":  [
                                                      "run",
                                                      "-q",
                                                      "--directory",
                                                      "C:\\tmp\\fastmcp-jina-minsearch-clone-of-context7",
                                                      "repo_docs.py"
                                                  ],
                                         "env":  {
                                                     "PYTHONUNBUFFERED":  "1"
                                                 },
                                         "command":  "C:\\Users\\d_local\\.local\\bin\\uv.exe"
                                     }
                    }
}
```

Later when working with Antigravity, you can simply ask:
> "Search the FastMCP documentation for 'how to implement a tool' using the Repo Docs MCP."

The agent will then:
1.  Identify the repository ZIP URL.
2.  Use the `search_repo_docs` tool to index the files.
3.  Retrieve the top 5 most relevant Markdown snippets.
4.  Use that context to provide an accurate, document-backed response.

## 🔒 Security & Privacy Notice
Unlike cloud-based documentation searchers, Repo Docs MCP performs all indexing **in memory**. This makes it an ideal choice for enterprises that need to maintain strict data residency while still empowering their developers with AI-assisted coding.
