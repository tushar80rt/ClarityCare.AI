from camel.toolkits.arxiv_toolkit import ArxivToolkit

arxiv_tool = ArxivToolkit()

def get_mental_health_papers():
    try:
        results = arxiv_tool.search_papers("mental health OR mindfulness", max_results=3)

        if not results:
            raise ValueError("No papers returned")

        papers = []
        for paper in results:
            title = getattr(paper, "title", None) or paper.get("title", "Untitled")
            entry_id = getattr(paper, "entry_id", None) or paper.get("entry_id", "#")
            papers.append({
                "title": title,
                "entry_id": entry_id
            })

        return papers

    except Exception as e:
        print(f"[ERROR] Failed to fetch papers: {e}")
        return [{"title": "❗ Could not load some research papers.", "entry_id": "#"} for _ in range(3)]
