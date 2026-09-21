import argparse
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def load_events(file_path: str) -> list[dict]:
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        print(f"Error: File '{file_path}' is empty.", file=sys.stderr)
        sys.exit(1)

    if content.startswith("[") and content.endswith("]"):
        try:
            parsed = json.loads(content)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            pass

    events = []
    for line in content.splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    return events


def filter_events(events: list[dict], target_level: str = "critical") -> list[dict]:
    target = target_level.strip().lower()
    return [e for e in events if str(e.get("level", "")).strip().lower() == target]


def main():
    parser = argparse.ArgumentParser(description="Filter events by severity level.")
    parser.add_argument("-f", "--file", default="events.json", help="Path to events file")
    parser.add_argument("-l", "--level", default="critical", help="Severity level to filter")
    args = parser.parse_args()

    events = load_events(args.file)
    filtered = filter_events(events, args.level)

    for event in filtered:
        print(json.dumps(event, ensure_ascii=False))

    if args.level.strip().lower() == "critical":
        print(f"критичных {len(filtered)}")
    else:
        print(f"{args.level} {len(filtered)}")


if __name__ == "__main__":
    main()
