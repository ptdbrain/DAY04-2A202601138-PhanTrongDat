---
doc_id: data-privacy-policy
policy_area: data_privacy
title: Data Privacy Policy For AI Tools
source: Company Research Policy Handbook v1
effective_date: 2026-06-01
tags: [privacy, confidential, customer data, PII, AI tools]
---

## Confidential data

- Do not paste confidential customer data, access tokens, unreleased financials, or private employee information into external AI tools.
- Redact personally identifiable information before using live web, model, or scraping tools.
- If the user asks to process confidential data, ask for a redacted version or use an approved internal workflow.

## API keys and credentials

- API keys must stay in `.env` or a secret manager.
- Never include API keys in prompts, transcripts, reports, screenshots, or git commits.
- If a key is exposed, rotate it before continuing the lab.

## Transcript handling

- Lab transcripts can be submitted only if they do not contain secrets or personal data.
- Tool results should be summarized with source links, not copied wholesale when sensitive content is present.
