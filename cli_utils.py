from typing import List, Dict, Any, Optional
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from cf_api import Problem

def get_user_filters(unique_tags: List[str]) -> Dict[str, Any]:
    """Interactively asks for problem filters and export formats."""
    
    def validate_rating(val: str) -> bool:
        if val == "": return True
        try:
            num = int(val)
            return 0 <= num <= 3500
        except ValueError:
            return False

    def validate_limit(val: str) -> bool:
        try:
            num = int(val)
            return num > 0
        except ValueError:
            return False

    # 1. Rating Range
    min_rating_str = inquirer.text(
        message="Minimum Rating (Enter for none):",
        validate=validate_rating,
        invalid_message="Rating must be between 0 and 3500",
    ).execute()
    min_rating = int(min_rating_str) if min_rating_str else None

    max_rating_str = inquirer.text(
        message="Maximum Rating (Enter for none):",
        validate=lambda val: validate_rating(val) and (not val or not min_rating or int(val) >= min_rating),
        invalid_message=f"Rating must be between {min_rating or 0} and 3500",
    ).execute()
    max_rating = int(max_rating_str) if max_rating_str else None

    # 2. Tags
    # Add an "All Tags" toggle or just select none for all
    selected_tags = inquirer.checkbox(
        message="Select Tags (Space to toggle, Enter to confirm, leave empty for ALL):",
        choices=[Choice(tag, name=tag) for tag in unique_tags],
    ).execute()

    # 3. Problem Limit
    limit_str = inquirer.text(
        message="Problem Limit:",
        default="50",
        validate=validate_limit,
        invalid_message="Limit must be a positive integer",
    ).execute()
    limit = int(limit_str)

    # 4. Export Formats (Checkbox for multiple selection)
    export_formats = inquirer.checkbox(
        message="Select Export Formats (Space to toggle):",
        choices=[
            Choice("txt", name="Text (.txt)", enabled=True),
            Choice("md", name="Markdown (.md)"),
            Choice("pdf", name="PDF (.pdf)"),
            Choice("html", name="HTML (.html)")
        ],
        validate=lambda result: len(result) >= 1,
        invalid_message="Select at least one format",
    ).execute()

    return {
        "min_rating": min_rating,
        "max_rating": max_rating,
        "selected_tags": selected_tags,
        "limit": limit,
        "formats": export_formats
    }
