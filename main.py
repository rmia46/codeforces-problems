import os
from cf_api import fetch_problems
from cli_utils import get_user_filters
from filters import filter_problems
from exporters import Exporter

# Colors for terminal
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def main():
    print(f"{BLUE}{BOLD}--- cf-lense v1.1.0 ---{RESET}")
    print(f"{CYAN}Fetching latest problems from CF...{RESET}")
    
    all_problems = fetch_problems()
    if not all_problems:
        print(f"Failed to fetch problems. Please check your internet connection.")
        return

    # Extract unique tags for the checkbox
    unique_tags = sorted(list(set(tag for p in all_problems for tag in p.tags)))

    # Get user criteria
    filters = get_user_filters(unique_tags)

    # Filter problems
    filtered = filter_problems(all_problems, filters)

    if not filtered:
        print(f"\nNo problems found matching your criteria.")
        return

    # Export
    exporter = Exporter(filtered, filters)
    formats = filters["formats"]
    
    print(f"\n{BOLD}Exporting problems to {BLUE}{exporter.output_dir}{RESET}...")
    
    for fmt in formats:
        if fmt == "txt":
            exported_file = exporter.export_to_txt()
        elif fmt == "md":
            exported_file = exporter.export_to_md()
        elif fmt == "html":
            exported_file = exporter.export_to_html()
        
        print(f"  - {GREEN}Successfully exported: {os.path.basename(exported_file)}{RESET}")

    print(f"\n{BOLD}{GREEN}Done! Processed {len(filtered)} problems.{RESET}")

if __name__ == "__main__":
    main()
