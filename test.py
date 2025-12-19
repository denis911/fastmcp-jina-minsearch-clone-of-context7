from repo_docs import _scrape_web_page_logic as scrape_web_page

def test_scrape():
    url = "https://datatalks.club" # Example from task description
    print(f"Testing scraping for: {url}")
    try:
        content = scrape_web_page(url)
        print("Success! Content preview:")
        print(content[:500]) # Print first 500 chars
        if "DataTalks.Club" in content or "DataTalks" in content:
             print("\nVerification Passed: Content seems relevant.")
        else:
             print("\nVerification Warning: Content might not be what expected.")
    except Exception as e:
        print(f"Error scraping: {e}")



def test_github_scrape():
    url = "https://github.com/alexeygrigorev/minsearch"
    print(f"\nTesting scraping for: {url}")
    try:
        content = scrape_web_page(url)
        char_count = len(content)
        print("Success!")
        print(f"Character count: {char_count}")
        print("-" * 20)
    except Exception as e:
        print(f"Error scraping: {e}")

if __name__ == "__main__":
    test_scrape()
    test_github_scrape()
