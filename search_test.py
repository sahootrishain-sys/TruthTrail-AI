from search import search_web

results = search_web("OpenAI")

for result in results:
    print("-" * 50)
    print("Title:", result["title"])
    print("URL:", result["href"])
    print("Summary:", result["body"])