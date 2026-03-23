import os
import uuid
from typing import List, Dict, Any
from fpdf import FPDF
import datetime
from cf_api import Problem

# Global Metadata
SCRIPT_TITLE = "cf-lense"
VERSION = "v1.0.0"
AUTHOR = "@rmia46 (Roman Mia)"
GITHUB_LINK = "https://github.com/rmia46/cf-lense"

class Exporter:
    def __init__(self, problems: List[Problem], filters: Dict[str, Any]):
        self.problems = problems
        self.filters = filters
        self.timestamp_raw = datetime.datetime.now()
        self.timestamp_str = self.timestamp_raw.strftime("%Y-%m-%d %H:%M:%S")
        self.unique_id = str(uuid.uuid4())[:8]
        
        # Create folder structure: export/YYYYMMDD_HHMMSS_ID/
        folder_name = f"{self.timestamp_raw.strftime('%Y%m%d_%H%M%S')}_{self.unique_id}"
        self.output_dir = os.path.join("export", folder_name)
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_filename(self, extension: str) -> str:
        base_name = f"problems_{self.timestamp_raw.strftime('%Y%m%d_%H%M%S')}_{self.unique_id}"
        return os.path.join(self.output_dir, f"{base_name}.{extension}")

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
            "-" * 80
        ]

    def export_to_txt(self) -> str:
        filename = self._get_filename("txt")
        with open(filename, "w", encoding="utf-8") as f:
            for line in self._get_header_info():
                f.write(line + "\n")
            f.write("\n")
            for p in self.problems:
                f.write(f"{p.name} | ID: {p.full_id} | Rating: {p.rating or 'N/A'}\n")
                f.write(f"Topics: {', '.join(p.tags)}\n")
                f.write(f"Link: {p.link}\n\n")
        return filename

    def export_to_md(self) -> str:
        filename = self._get_filename("md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {SCRIPT_TITLE}\n\n")
            f.write(f"- **Author:** {AUTHOR}\n")
            f.write(f"- **GitHub:** [{GITHUB_LINK}]({GITHUB_LINK})\n")
            f.write(f"- **Generated on:** {self.timestamp_str}\n")
            f.write(f"- **Filters:** {self._get_filter_str()}\n\n")
            f.write("| Problem Name | ID | Rating | Topics | Link |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for p in self.problems:
                tags = ", ".join(p.tags)
                f.write(f"| {p.name} | {p.full_id} | {p.rating or 'N/A'} | {tags} | [Link]({p.link}) |\n")
        return filename

    def export_to_pdf(self) -> str:
        filename = self._get_filename("pdf")
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Header Section
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, SCRIPT_TITLE, ln=True, align="C")
        
        pdf.set_font("helvetica", "", 10)
        pdf.cell(0, 6, f"Author: {AUTHOR}", ln=True, align="C")
        pdf.set_text_color(0, 0, 255)
        pdf.cell(0, 6, GITHUB_LINK, ln=True, align="C", link=GITHUB_LINK)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 6, f"Generated on: {self.timestamp_str}", ln=True, align="C")
        pdf.multi_cell(0, 6, f"Filters: {self._get_filter_str()}", align="C")
        pdf.ln(5)
        
        for p in self.problems:
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 8, f"{p.name} ({p.full_id})", ln=True)
            
            pdf.set_font("helvetica", "", 10)
            pdf.cell(0, 6, f"Rating: {p.rating or 'N/A'}", ln=True)
            pdf.multi_cell(0, 6, f"Topics: {', '.join(p.tags)}")
            
            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 6, "View on Codeforces", ln=True, link=p.link)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(4)
            
        pdf.output(filename)
        return filename

    def export_to_html(self) -> str:
        filename = self._get_filename("html")
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{SCRIPT_TITLE}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: auto; padding: 20px; }}
                h1 {{ color: #2c3e50; text-align: center; }}
                .meta {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; box-shadow: 0 2px 15px rgba(0,0,0,0.1); }}
                th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #3498db; color: white; }}
                tr:hover {{ background-color: #f1f1f1; }}
                .tag {{ background: #e0e0e0; padding: 2px 8px; border-radius: 4px; font-size: 0.85em; margin-right: 4px; display: inline-block; }}
                a {{ color: #3498db; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>{SCRIPT_TITLE}</h1>
            <div class="meta">
                <p><strong>Author:</strong> {AUTHOR} | <strong>GitHub:</strong> <a href="{GITHUB_LINK}">{GITHUB_LINK}</a></p>
                <p><strong>Generated on:</strong> {self.timestamp_str}</p>
                <p><strong>Filters:</strong> {self._get_filter_str()}</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>ID</th>
                        <th>Rating</th>
                        <th>Topics</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
        """
        for p in self.problems:
            tags_html = "".join([f'<span class="tag">{t}</span>' for t in p.tags])
            html_content += f"""
                <tr>
                    <td>{p.name}</td>
                    <td>{p.full_id}</td>
                    <td>{p.rating or 'N/A'}</td>
                    <td>{tags_html}</td>
                    <td><a href="{p.link}" target="_blank">View Problem</a></td>
                </tr>
            """
        
        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        return filename
