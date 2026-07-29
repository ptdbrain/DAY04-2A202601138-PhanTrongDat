from typing import Any
import os
import requests

def verify_claim(claim: str, **kwargs) -> dict[str, Any]:
    """Verify a claim by searching for fact-checks and authoritative sources via Tavily."""
    try:
        key = os.getenv("TAVILY_API_KEY")
        if not key:
            raise RuntimeError("Missing TAVILY_API_KEY")

        # Search for fact-checks about this claim
        queries = [
            f"fact check: {claim}",
            f"sự thật về: {claim}",
        ]
        all_results = []
        for query in queries:
            resp = requests.post(
                "https://api.tavily.com/search",
                json={"query": query, "topic": "news", "max_results": 3, "search_depth": "basic"},
                headers={"Authorization": f"Bearer {key}"},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            all_results.extend(data.get("results", []))

        # Deduplicate by URL
        seen = set()
        unique = []
        for r in all_results:
            url = r.get("url", "")
            if url not in seen:
                seen.add(url)
                unique.append({
                    "title":   r.get("title"),
                    "url":     url,
                    "summary": r.get("content", "")[:400],
                    "score":   r.get("score", 0),
                })

        # Determine status from result count and keywords
        content_blob = " ".join(r.get("summary", "") for r in unique).lower()
        if any(k in content_blob for k in ["false", "sai", "bác bỏ", "không có cơ sở", "tin giả", "misinformation"]):
            status = "FALSE"
        elif any(k in content_blob for k in ["true", "đúng", "xác nhận", "chính thức", "confirmed"]):
            status = "TRUE"
        elif unique:
            status = "PARTIALLY TRUE / UNVERIFIED"
        else:
            status = "UNVERIFIED — no sources found"

        return {
            "tool":    "fact_check_source",
            "claim":   claim,
            "status":  status,
            "sources": unique[:5],
        }

    except Exception as exc:
        return {
            "tool":   "fact_check_source",
            "claim":  claim,
            "status": "ERROR",
            "error":  str(exc),
        }
