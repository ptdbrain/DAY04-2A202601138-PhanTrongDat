from typing import Any
import os
import requests

def get_viral_claims(keyword: str, **kwargs) -> dict[str, Any]:
    """Search for viral claims and rumors related to a keyword using Tavily news search."""
    try:
        key = os.getenv("TAVILY_API_KEY")
        if not key:
            raise RuntimeError("Missing TAVILY_API_KEY")

        query = f"tin đồn viral {keyword} OR rumor {keyword} OR hoax {keyword}"
        resp = requests.post(
            "https://api.tavily.com/search",
            json={"query": query, "topic": "news", "max_results": 5, "search_depth": "basic"},
            headers={"Authorization": f"Bearer {key}"},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        claims = [{
            "title":   r.get("title"),
            "url":     r.get("url"),
            "summary": r.get("content", "")[:300],
            "source":  r.get("url", "").split("/")[2] if r.get("url") else "",
        } for r in data.get("results", [])]

        return {"tool": "find_viral_claims", "keyword": keyword, "viral_claims": claims}

    except Exception as exc:
        return {"tool": "find_viral_claims", "keyword": keyword, "error": str(exc)}
