import argparse
import json
import os
import sys
import time
from typing import Literal
from pydantic import BaseModel
from google import genai
from google.genai import types

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


class InquiryResult(BaseModel):
    id: int
    text: str
    category: Literal["справка", "жалоба", "другое"]
    draft_reply: str


class BatchClassificationResult(BaseModel):
    inquiries: list[InquiryResult]


def load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        print(f"Error: Config '{config_path}' not found. Copy 'config.example.json' to it.", file=sys.stderr)
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    api_key = config.get("gemini_api_key", "").strip()
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        print(f"Error: Set a valid 'gemini_api_key' in '{config_path}'.", file=sys.stderr)
        sys.exit(1)

    return config


def load_messages(file_path: str) -> list[str]:
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        print(f"Error: No messages found in '{file_path}'.", file=sys.stderr)
        sys.exit(1)

    return messages


def classify_inquiries(messages: list[str], api_key: str, model_name: str) -> list[dict]:
    client = genai.Client(api_key=api_key)
    formatted = "\n".join(f"{i + 1}. {m}" for i, m in enumerate(messages))

    prompt = (
        "Ты — автоматический классификатор обращений службы поддержки.\n"
        "Для каждого обращения определи:\n"
        "1. Категорию строго из: 'справка', 'жалоба', 'другое'.\n"
        "2. Вежливый и лаконичный черновик ответа на русском языке.\n\n"
        f"Обращения:\n{formatted}"
    )

    max_retries = 3
    delay = 2

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=BatchClassificationResult,
                    temperature=0.2,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                ),
            )

            data = json.loads(response.text)
            if isinstance(data, dict) and "inquiries" in data:
                return data["inquiries"]
            return data if isinstance(data, list) else [data]

        except Exception as e:
            err = str(e)
            if ("503" in err or "429" in err or "UNAVAILABLE" in err) and attempt < max_retries:
                time.sleep(delay)
                delay *= 2
            else:
                print(f"Error during Gemini API call: {e}", file=sys.stderr)
                sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Classify inquiries and draft responses.")
    parser.add_argument("-f", "--file", default="messages.txt", help="Path to messages text file")
    parser.add_argument("-c", "--config", default="config.json", help="Path to config JSON file")
    parser.add_argument("-p", "--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    config = load_config(args.config)
    messages = load_messages(args.file)
    results = classify_inquiries(messages, config["gemini_api_key"], config.get("model", "gemini-3.6-flash"))

    if args.pretty:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(results, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
