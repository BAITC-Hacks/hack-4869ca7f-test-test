# Hackathon Prototype Solutions

A collection of lightweight Python automation tools built for hackathon evaluation:
- **Case 1**: Inquiry classification and Russian response drafting via Gemini API.
- **Case 2**: Operational event noise filtering using standard Python libraries.

## Case 1: Inquiry Classifier & Response Drafter

A CLI tool to automatically classify customer/student inquiries into predefined categories and draft polite Russian responses using Gemini models.

### Features
- **Automated Classification**: Categorizes inquiries strictly into `справка`, `жалоба`, or `другое`.
- **Draft Generation**: Automatically generates a polite, constructive response in Russian.
- **Batch Processing**: Sends all inquiries in a single API call with structured JSON schema.
- **Secure Configuration**: Reads API keys from `config.json` (git-ignored, template in `config.example.json`).
- **Flexible CLI**: Supports custom files, config paths, and compact or pretty-printed JSON.

### Dependencies & Tech Stack
- **Python**: 3.10+ (tested on Python 3.14)
- **Root Package**: `google-genai`
- **Pinned Versions**: See `requirements.txt` (`pip freeze`)

### Setup & Installation

#### 1. Create and Activate Virtual Environment
```bash
# Windows (PowerShell)
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1

# Or in Windows CMD:
# .\venv\Scripts\activate.bat

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

> **Tip (Windows)**: You can run directly without activating: `.\venv\Scripts\python classifier.py --pretty`

#### 2. Install Dependencies
```bash
# With venv activated:
pip install -r requirements.txt

# Or without activating (Windows):
.\venv\Scripts\pip install -r requirements.txt
```

#### 3. Configure API Key
1. Copy the sample config:
   ```bash
   copy config.example.json config.json   # Windows
   cp config.example.json config.json     # Linux / macOS
   ```
2. Put your Google AI Studio API key into `config.json`:
   ```json
   {
     "gemini_api_key": "AIzaSy...",
     "model": "gemini-3.6-flash"
   }
   ```
   *(Note: `gemini-3.6-flash` is eligible for Google AI Studio's free tier).*

### Usage

#### Default Run (`messages.txt`)
Outputs compact JSON to `stdout`:
```bash
python classifier.py
```

#### Pretty-Printed JSON Output
```bash
python classifier.py --pretty
```

#### Extended Test Cases (20 Inquiries)
```bash
python classifier.py --file additional_messages.txt --pretty
```

### CLI Reference

| Flag | Short | Default | Description |
|---|---|---|---|
| `--file` | `-f` | `messages.txt` | Path to text file with inquiries (one per line) |
| `--config` | `-c` | `config.json` | Path to JSON config file with API key |
| `--pretty` | `-p` | `False` | Pretty-print output JSON with 2-space indentation |

### Sample Output

Running `python classifier.py --pretty`:

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

## Case 2: Alert Filter

A zero-dependency Python script to filter operational event streams, eliminate noise (`info`, `warn`), and isolate critical events with an aggregated summary count.

### Features
- **Noise Filtering**: Extracts events matching target severity (default: `critical`).
- **Standard Library Only**: Pure Python (`json`, `argparse`, `sys`) — no external packages, APIs, or AI models.
- **NDJSON Support**: Reads line-delimited JSON (`events.json`), with fallback for standard JSON arrays.
- **CLI Options**: Configurable file path (`--file`) and severity level (`--level`).
- **Cross-Platform UTF-8**: Automatically reconfigures stdout encoding for Windows console compatibility.

### Usage

#### Default Run (`events.json`)
```bash
python filter_alerts.py
```
*(Or on Windows without activating venv: `.\venv\Scripts\python filter_alerts.py`)*

#### Extended Test Cases (20 Events)
```bash
python filter_alerts.py --file additional_events.json
```

#### Filter by Other Severity Levels
```bash
python filter_alerts.py --level warn
```

### CLI Reference

| Flag | Short | Default | Description |
|---|---|---|---|
| `--file` | `-f` | `events.json` | Path to event file (NDJSON format) |
| `--level` | `-l` | `critical` | Severity level to filter (case-insensitive) |

### Sample Output

Running `python filter_alerts.py`:

```
{"event": "disk 90%", "level": "critical"}
{"event": "payment failed", "level": "critical"}
{"event": "db timeout", "level": "critical"}
критичных 3
```
