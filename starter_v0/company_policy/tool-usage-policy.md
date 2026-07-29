---
doc_id: tool-usage-policy
policy_area: tool_usage
title: AI Tool Usage Policy
source: Company Research Policy Handbook v1
effective_date: 2026-06-01
tags: [tool use, web search, firecrawl, twitter, arxiv, rate limit]
---

## Tool selection

- Use company policy search for internal rules.
- Use web search for current public news.
- Use URL reading for a specific link.
- Use Twitter/X tools for tweets and social signals.
- Use arXiv tools for academic papers and preprints.

## Rate limits

- arXiv requests should be spaced by at least 3 seconds.
- Free-tier APIs can rate-limit or fail; record provider errors in the run JSON instead of hiding them.

## Write actions

- Any tool that sends, posts, books, deletes, or changes external state requires explicit confirmation.
- If confirmation is missing, call `ask_user(response_type="yes_no")`.
