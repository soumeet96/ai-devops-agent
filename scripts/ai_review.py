#!/usr/bin/env python3
"""
AI PR Review Bot — powered by Groq (free tier)
Reads a git diff file and returns a structured code review using Llama 3.
"""

import json
import os
import sys
import urllib.request
import urllib.error

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"
MAX_DIFF_CHARS = 12000  # Keep within token limits


SYSTEM_PROMPT = """You are a senior DevOps and software engineer performing a code review.
Analyze the provided git diff and give a concise, actionable review covering:

1. **Security** — any secrets, vulnerabilities, or unsafe patterns
2. **DevOps / Infrastructure** — Dockerfile, CI/CD, config, or deployment concerns
3. **Code Quality** — logic errors, edge cases, or improvements
4. **Summary** — overall assessment (Approve / Request Changes / Needs Discussion)

Be specific. Reference file names and line numbers where possible.
Format your response as clean Markdown. Keep it under 400 words."""


def read_diff(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    if len(content) > MAX_DIFF_CHARS:
        content = content[:MAX_DIFF_CHARS] + "\n\n[diff truncated — too large]"
    return content


def call_groq(diff: str, api_key: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Please review this PR diff:\n\n```diff\n{diff}\n```"},
        ],
        "temperature": 0.3,
        "max_tokens": 1024,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        GROQ_API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ai-devops-agent/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"Groq API error {e.code}: {body}") from e


def main():
    if len(sys.argv) < 2:
        print("Usage: ai_review.py <diff_file>", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    diff_path = sys.argv[1]
    diff = read_diff(diff_path)

    if not diff.strip():
        print("## AI Review\n\nNo changes detected in this PR.")
        return

    review = call_groq(diff, api_key)

    header = "## 🤖 AI Code Review (powered by Groq + Llama 3.3)\n\n"
    footer = "\n\n---\n*Automated review by [ai-devops-agent](https://github.com/soumeet96/ai-devops-agent)*"
    print(header + review + footer)


if __name__ == "__main__":
    main()
