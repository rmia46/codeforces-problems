# cf-lense v1.0.0

A powerful and modular Python CLI tool to filter and export Codeforces problems into multiple formats (.txt, .md, .pdf, .html).

**Author:** @rmia46 (Roman Mia)  
**GitHub:** [https://github.com/rmia46/cf-lense](https://github.com/rmia46/cf-lense)

## Features

- **Interactive CLI**: Fast and easy-to-use prompts with `InquirerPy`.
- **Advanced Filtering**: Filter by rating range, specific tags (OR logic), and problem limit.
- **Smart Tags**: If no tags are selected, it searches across all available tags (Codeforces default).
- **Multiple Export Formats (Toggleable)**:
  - **Text (.txt)**: Plain text with detailed headers.
  - **Markdown (.md)**: Formatted table, perfect for GitHub.
  - **PDF (.pdf)**: Professional document with clickable links.
  - **HTML (.html)**: Modern, responsive table with styled tags.
- **Organized Exports**: Every export is saved in a unique timestamped folder within `export/` to prevent overwrites.
- **Type Safety**: Built with Python dataclasses and type hinting.

## Prerequisites

- Python 3.7 or higher

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rmia46/cf-lense.git
   cd cf-lense
   ```

2. **Setup environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the tool**:
   ```bash
   python3 main.py
   ```

## Usage

Follow the interactive prompts to set your criteria. You can toggle multiple export formats using the `Space` bar. 

Exports will be located in:
`export/YYYYMMDD_HHMMSS_UUID/`

## Project Structure

- `main.py`: CLI entry point and orchestration.
- `cf_api.py`: Codeforces API integration and data models.
- `cli_utils.py`: Interactive prompt logic and validation.
- `filters.py`: Problem filtering engine.
- `exporters.py`: multi-format generation logic.
