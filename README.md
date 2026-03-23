# cf-lense v1.1.0

A modular CLI tool to filter and export Codeforces problems into multiple formats.

**Author:** @rmia46 (Roman Mia)  
**GitHub:** [https://github.com/rmia46/cf-lense](https://github.com/rmia46/cf-lense)

## Features
- Interactive CLI for rating and tag filtering
- Exports to .txt, .md, and .html formats
- Modern, colorful HTML design optimized for printing to PDF
- Organized exports with incremental IDs (e.g., `03_23_0001_50`)
- No random UUIDs; sequential tracking for easy management

## Quick Start (Binary)
Download the latest pre-built binary for your system from the [Releases](https://github.com/rmia46/cf-lense/releases) page.
```bash
chmod +x cf-lense-linux
./cf-lense-linux
```

## Setup (Source)
1. Clone and enter the repo:
```bash
git clone https://github.com/rmia46/cf-lense.git && cd cf-lense
```
2. Setup environment and install dependencies:
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```
3. Run the tool:
```bash
python3 main.py
```

## Usage
- **Rating**: Enter a range (e.g., 1000 to 1500) or leave blank for any.
- **Tags**: Use `Space` to toggle specific tags. Leave empty to search all (CF default).
- **Export**: Toggle multiple formats with `Space`.
- **Output**: Files are saved in `export/MM_DD_ID_COUNT/`.

## Dependencies
- requests
- InquirerPy
