import os
import requests
import zipfile
import io
import minsearch

def download_docs(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {url}...")
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"{filename} already exists, skipping download.")

def extract_docs(zip_filename):
    documents = []
    with zipfile.ZipFile(zip_filename, 'r') as zf:
        for file_info in zf.infolist():
            if file_info.filename.endswith(('.md', '.mdx')):
                # Remove the first part of the path
                # e.g., "fastmcp-main/docs/getting-started/welcome.mdx" -> "docs/getting-started/welcome.mdx"
                parts = file_info.filename.split('/')
                if len(parts) > 1:
                    clean_filename = '/'.join(parts[1:])
                else:
                    clean_filename = file_info.filename
                
                with zf.open(file_info) as f:
                    content = f.read().decode('utf-8')
                    documents.append({
                        'filename': clean_filename,
                        'content': content
                    })
    return documents

def build_index(documents):
    index = minsearch.Index(
        text_fields=['content'],
        keyword_fields=['filename']
    )
    index.fit(documents)
    return index

def main():
    url = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
    zip_filename = "fastmcp-main.zip"
    
    download_docs(url, zip_filename)
    documents = extract_docs(zip_filename)
    
    index = build_index(documents)
    
    def search(query):
        return index.search(
            query=query,
            num_results=5
        )

    # Test the search
    query = "How to get started with FastMCP?"
    print(f"\nSearching for: '{query}'")
    results = search(query)
    
    print(f"\nFound {len(results)} results:")
    for doc in results:
        print(f"--- {doc['filename']} ---")
        print(doc['content'][:200] + "...")
        print()

if __name__ == "__main__":
    main()
