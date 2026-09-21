# Inquiry Classifier & Response Drafter (Case 1)

A lightweight CLI tool built for the hackathon rehearsal to automatically process incoming customer and student inquiries, classify them into predefined categories, and draft initial polite responses in Russian using Google's Gemini models.

## Features

- **Automated Classification**: Categorizes each inquiry into strictly one of three categories:
  - `справка` (Inquiry / Information request)
  - `жалоба` (Complaint / Service issue)
  - `другое` (Other / Miscellaneous)
- **Draft Generation**: Automatically drafts a polite, concise, and constructive Russian response for each inquiry.
- **Batch Processing**: Sends all inquiries in a single API call with a structured JSON schema to optimize execution speed and preserve free-tier quotas.
- **Secure Secrets Management**: Reads the Gemini API key directly from `config.json` without extra third-party dotenv dependencies; `config.json` is strictly excluded from version control via `.gitignore`.
- **Flexible CLI**: Powered by `argparse`, supporting custom input files, alternative configuration paths, and optional pretty-printed JSON formatting.

---

## Dependencies & Technology Stack

- **Python**: 3.10+ (tested on Python 3.14)
- **Root Package**: `google-genai` (official Google GenAI SDK for Gemini models)
- **Pinned Dependencies**: See [`requirements.txt`](file:///requirements.txt) for exact frozen versions (`pip freeze`).

---

## Setup & Installation

### 1. Create and Activate a Virtual Environment

```bash
# Windows (PowerShell)
python -m venv venv

# If PowerShell blocks script execution, enable it for current session:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1

# Or in Windows Command Prompt (cmd):
# .\venv\Scripts\activate.bat

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

> **Tip (Windows)**: You can also run the script directly using the environment's Python binary without activating:
> ```powershell
> .\venv\Scripts\python classifier.py --pretty
> ```

### 2. Install Pinned Dependencies

```bash
# With venv activated:
pip install -r requirements.txt

# Or without activating (Windows):
.\venv\Scripts\pip install -r requirements.txt
```

### 3. Configure API Key

1. Copy the sample configuration file:
   ```bash
   # Windows
   copy config.example.json config.json

   # Linux / macOS
   cp config.example.json config.json
   ```

2. Obtain a free API key from [Google AI Studio](https://aistudio.google.com/).
3. Open `config.json` and replace `YOUR_GEMINI_API_KEY_HERE` with your key:
   ```json
   {
     "gemini_api_key": "AIzaSy...",
     "model": "gemini-3.6-flash"
   }
   ```
   *(Note: `gemini-3.6-flash` is eligible for Google AI Studio's free tier).*

---

## Usage

### Run on Default Inquiries (`messages.txt`)

By default, the script reads `messages.txt` and outputs compact JSON to `stdout`:

```bash
python classifier.py
```

### Pretty-Print JSON Output

To display indented, human-readable JSON output:

```bash
python classifier.py --pretty
```

### Run on Extended Test Cases (20 Inquiries)

We provide an extended set of 20 realistic test inquiries in `additional_messages.txt`:

```bash
python classifier.py --file additional_messages.txt --pretty
```

### CLI Reference

| Flag | Short | Default | Description |
|---|---|---|---|
| `--file` | `-f` | `messages.txt` | Path to the text file containing messages (one per line) |
| `--config` | `-c` | `config.json` | Path to JSON config file containing the API key |
| `--pretty` | `-p` | `False` | Pretty-print output JSON with 2-space indentation |

---

## Sample Output

When executing `python classifier.py --pretty`, the script produces structured JSON:

```json
[
  {
    "id": 1,
    "text": "Как получить справку о месте учёбы?",
    "category": "справка",
    "draft_reply": "Здравствуйте! Справку о месте учёбы вы можете заказать онлайн через личный кабинет студента либо обратиться лично в деканат вашего факультета."
  },
  {
    "id": 2,
    "text": "В столовой очередь, еда холодная.",
    "category": "жалоба",
    "draft_reply": "Здравствуйте! Приносим извинения за неудобства. Ваше обращение передано администрации комбината питания для проверки работы линии раздачи и контроля температуры блюд."
  },
  {
    "id": 3,
    "text": "Хочу записаться на консультацию завтра.",
    "category": "справка",
    "draft_reply": "Здравствуйте! Записаться на консультацию можно в системе электронного расписания или обратившись к преподавателю в приёмные часы."
  },
  {
    "id": 4,
    "text": "Пропал Wi‑Fi в корпусе B.",
    "category": "жалоба",
    "draft_reply": "Здравствуйте! Информация о сбое Wi-Fi в корпусе B передана в службу технической поддержки. Ведутся восстановительные работы."
  },
  {
    "id": 5,
    "text": "Где парковка для гостей?",
    "category": "справка",
    "draft_reply": "Здравствуйте! Гостевая парковка расположена справа от главного КПП (въезд со стороны Северного проезда)."
  }
]
```

---

# Alert Filter (Case 2)

A lightweight, zero-dependency Python script to filter operational event streams, eliminate background noise (`info`, `warn`), and isolate critical events with an aggregated summary count.

## Features

- **Noise Filtering**: Scans events and extracts only those matching the target severity (default: `critical`).
- **Standard Library Only**: Pure Python (`json`, `argparse`, `sys`) — no external packages, APIs, or AI models required.
- **NDJSON Support**: Reads line-delimited JSON (`events.json`), with fallback support for standard JSON arrays.
- **CLI Options**: Configurable input file path (`--file`) and severity level (`--level`).
- **Cross-Platform UTF-8**: Automatically handles terminal character encoding to display Cyrillic summary text (`критичных N`) correctly on Windows and Unix systems.

---

## Usage

### Run on Default Events (`events.json`)

```bash
python filter_alerts.py
```
*(Or on Windows without activating venv: `.\venv\Scripts\python filter_alerts.py`)*

### Run on Extended Test Cases (20 Events)

We provide an extended set of 20 realistic operational events in `additional_events.json`:

```bash
python filter_alerts.py --file additional_events.json
```

### Filter by Other Severity Levels

You can filter for other levels such as `warn` or `info`:

```bash
python filter_alerts.py --level warn
```

### CLI Reference

| Flag | Short | Default | Description |
|---|---|---|---|
| `--file` | `-f` | `events.json` | Path to event file (NDJSON format) |
| `--level` | `-l` | `critical` | Severity level to filter (case-insensitive) |

---

## Sample Output

When executing `python filter_alerts.py`:

```
{"event": "disk 90%", "level": "critical"}
{"event": "payment failed", "level": "critical"}
{"event": "db timeout", "level": "critical"}
критичных 3
```

