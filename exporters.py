import os
from typing import List, Dict, Any
import datetime
from cf_api import Problem

# Global Metadata
SCRIPT_TITLE = "cf-lense"
VERSION = "v1.1.0"
AUTHOR = "@rmia46 (Roman Mia)"
GITHUB_LINK = "https://github.com/rmia46/cf-lense"

class Exporter:
    def __init__(self, problems: List[Problem], filters: Dict[str, Any]):
        self.problems = problems
        self.filters = filters
        self.timestamp_raw = datetime.datetime.now()
        self.timestamp_str = self.timestamp_raw.strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate next incremental ID by scanning export folder
        self.inc_id = self._get_next_id()
        self.count = len(problems)
        
        # Compact naming: MM_DD_[ID]_[COUNT]
        month_day = self.timestamp_raw.strftime("%m_%d")
        self.base_identifier = f"{month_day}_{self.inc_id}_{self.count}"
        
        # Create folder: export/MM_DD_ID_COUNT/
        self.output_dir = os.path.join("export", self.base_identifier)
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_next_id(self) -> str:
        """Finds the highest existing incremental ID in the export directory and returns the next one."""
        export_path = "export"
        if not os.path.exists(export_path):
            return "0001"
        
        max_id = 0
        # Expected folder pattern: MM_DD_NNNN_COUNT
        for folder_name in os.listdir(export_path):
            if os.path.isdir(os.path.join(export_path, folder_name)):
                parts = folder_name.split('_')
                if len(parts) >= 3:
                    try:
                        # parts[2] should be the NNNN (incremental ID)
                        current_id = int(parts[2])
                        if current_id > max_id:
                            max_id = current_id
                    except ValueError:
                        continue
        
        return f"{max_id + 1:04d}"

    def _get_filename(self, extension: str) -> str:
        return os.path.join(self.output_dir, f"cf_lense_{self.base_identifier}.{extension}")

    def _get_filter_str(self) -> str:
        min_r = self.filters["min_rating"] or "Any"
        max_r = self.filters["max_rating"] or "Any"
        tags = ", ".join(self.filters["selected_tags"]) if self.filters["selected_tags"] else "Any (CF scope)"
        return f"Rating: [{min_r}-{max_r}] | Tags: {tags}"

    def _get_header_info(self) -> List[str]:
        return [
            f"{SCRIPT_TITLE} {VERSION}",
            f"Author: {AUTHOR}",
            f"GitHub: {GITHUB_LINK}",
            f"Generated on: {self.timestamp_str}",
            f"Filters: {self._get_filter_str()}",
            f"Total Problems: {self.count}",
            "=" * 80
        ]

    def export_to_txt(self) -> str:
        filename = self._get_filename("txt")
        with open(filename, "w", encoding="utf-8") as f:
            for line in self._get_header_info():
                f.write(line + "\n")
            f.write("\n")
            for p in self.problems:
                f.write(f"[{p.full_id}] {p.name}\n")
                f.write(f"Rating: {p.rating or 'N/A'}\n")
                f.write(f"Topics: {', '.join(p.tags)}\n")
                f.write(f"URL   : {p.link}\n")
                f.write("-" * 40 + "\n")
        return filename

    def export_to_md(self) -> str:
        filename = self._get_filename("md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {SCRIPT_TITLE} {VERSION}\n\n")
            f.write(f"```text\n")
            f.write(f"Author: {AUTHOR}\n")
            f.write(f"GitHub: {GITHUB_LINK}\n")
            f.write(f"Generated on: {self.timestamp_str}\n")
            f.write(f"Filters: {self._get_filter_str()}\n")
            f.write(f"Total Problems: {self.count}\n")
            f.write(f"```\n\n")
            f.write("| ID | Problem Name | Rating | Topics | Link |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for p in self.problems:
                tags = ", ".join([f"`{t}`" for t in p.tags])
                f.write(f"| `{p.full_id}` | **{p.name}** | {p.rating or 'N/A'} | {tags} | [Open]({p.link}) |\n")
        return filename

    def export_to_html(self) -> str:
        filename = self._get_filename("html")
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{SCRIPT_TITLE} - {self.inc_id}</title>
            <style>
                :root {{
                    --bg: #ffffff;
                    --text: #2d3436;
                    --primary: #0984e3;
                    --secondary: #6c5ce7;
                    --accent: #00cec9;
                    --border: #dfe6e9;
                    --tag-bg: #f1f2f6;
                    --tag-text: #2f3542;
                    --header-bg: #f8f9fa;
                }}
                body {{ 
                    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; 
                    line-height: 1.6; 
                    color: var(--text); 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    padding: 40px 20px;
                    background: var(--bg);
                }}
                .header {{ 
                    border-left: 5px solid var(--primary); 
                    background: var(--header-bg);
                    margin-bottom: 30px; 
                    padding: 20px;
                    border-radius: 0 8px 8px 0;
                }}
                h1 {{ 
                    margin: 0; 
                    font-size: 28px; 
                    color: var(--primary);
                    font-weight: 900;
                    text-transform: lowercase;
                }}
                .meta-info {{ font-size: 13px; color: #636e72; margin-top: 10px; }}
                .meta-info a {{ color: var(--secondary); text-decoration: none; }}
                .filters {{ 
                    background: #eef2f7; 
                    padding: 15px; 
                    border-radius: 6px;
                    font-size: 13px;
                    margin: 25px 0;
                    border-left: 5px solid var(--accent);
                }}
                table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    margin-top: 20px;
                }}
                th, td {{ 
                    padding: 14px; 
                    text-align: left; 
                    border-bottom: 1px solid var(--border);
                    font-size: 14px;
                }}
                th {{ 
                    background: var(--primary);
                    color: white;
                    font-weight: bold;
                    text-transform: uppercase;
                    font-size: 12px;
                    letter-spacing: 1px;
                }}
                tr:nth-child(even) {{ background: #fdfdfd; }}
                tr:hover {{ background: #f1f2f6; transition: 0.2s; }}
                
                .tag {{ 
                    background: var(--tag-bg); 
                    padding: 3px 8px; 
                    border-radius: 4px; 
                    font-size: 11px; 
                    margin: 2px;
                    display: inline-block;
                    color: var(--tag-text);
                    border: 1px solid #dcdde1;
                    font-weight: 600;
                }}
                .rating-badge {{
                    font-weight: bold;
                    color: var(--primary);
                }}
                .prob-id {{ color: var(--secondary); font-weight: bold; }}
                
                .btn-link {{ 
                    color: white; 
                    background: var(--primary);
                    padding: 4px 10px;
                    border-radius: 4px;
                    text-decoration: none; 
                    font-size: 12px;
                    font-weight: bold;
                }}
                .btn-link:hover {{ background: var(--secondary); }}
                
                @media print {{
                    body {{ padding: 0; }}
                    .no-print {{ display: none; }}
                    .header {{ border: 1px solid #eee; background: white; }}
                    th {{ background: #eee !important; color: black !important; }}
                    .tag {{ border: 1px solid #ddd; background: white; }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{SCRIPT_TITLE} <span style="font-size: 14px; color: #888;">{VERSION}</span></h1>
                <div class="meta-info">
                    Author: <strong>{AUTHOR}</strong> | GitHub: <a href="{GITHUB_LINK}">{GITHUB_LINK}</a><br>
                    Generated: {self.timestamp_str} | ID: <span class="prob-id">{self.inc_id}</span>
                </div>
            </div>

            <div class="filters">
                <strong style="color: var(--primary);">FILTERS:</strong> {self._get_filter_str()}<br>
                <strong style="color: var(--primary);">COUNT:</strong> {self.count} problems
            </div>

            <table>
                <thead>
                    <tr>
                        <th style="width: 80px;">ID</th>
                        <th>Problem Name</th>
                        <th style="width: 80px;">Rating</th>
                        <th>Topics</th>
                        <th class="no-print" style="width: 80px;">Action</th>
                    </tr>
                </thead>
                <tbody>
        """
        for p in self.problems:
            tags_html = "".join([f'<span class="tag">{t}</span>' for t in p.tags])
            html_content += f"""
                <tr>
                    <td><code class="prob-id">{p.full_id}</code></td>
                    <td><strong>{p.name}</strong></td>
                    <td><span class="rating-badge">{p.rating or 'N/A'}</span></td>
                    <td>{tags_html}</td>
                    <td class="no-print"><a href="{p.link}" target="_blank" class="btn-link">OPEN</a></td>
                </tr>
            """
        
        html_content += """
                </tbody>
            </table>
            <p style="text-align: center; margin-top: 50px; font-size: 11px; color: #b2bec3; border-top: 1px solid #eee; padding-top: 20px;">
                Generated via <strong>cf-lense</strong> CLI tool.
            </p>
        </body>
        </html>
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        return filename
