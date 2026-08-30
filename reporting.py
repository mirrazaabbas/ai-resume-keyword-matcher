"""Safe standalone reporting for resume/job analysis."""
from __future__ import annotations

import html
from typing import Any


def _items(values: list[Any]) -> str:
    if not values:
        return "<li>None detected</li>"
    return "".join(f"<li>{html.escape(str(value))}</li>" for value in values)


def to_html(result: dict[str, Any]) -> str:
    sections = result.get("section_presence", {})
    section_rows = "".join(
        f"<tr><td>{html.escape(str(name))}</td><td>{'Yes' if present else 'No'}</td></tr>"
        for name, present in sections.items()
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Resume Match Report</title>
<style>body{{font-family:system-ui,sans-serif;max-width:900px;margin:40px auto;padding:0 20px;line-height:1.5}}.score{{font-size:2rem;font-weight:700}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:8px;text-align:left}}code{{background:#f3f3f3;padding:2px 5px}}</style></head><body>
<h1>Resume Match Report</h1>
<p class="score">Overall: {float(result['overall_match_score']):.1f}%</p>
<p>Required skills: {float(result['required_skill_score']):.1f}% · Lexical similarity: {float(result['lexical_similarity_score']):.1f}% · Section structure: {float(result['section_structure_score']):.1f}%</p>
<h2>Matched required skills</h2><ul>{_items(list(result['matched_required_skills']))}</ul>
<h2>Missing required skills to verify</h2><ul>{_items(list(result['missing_required_skills']))}</ul>
<h2>Resume sections</h2><table><thead><tr><th>Section</th><th>Detected</th></tr></thead><tbody>{section_rows}</tbody></table>
<h2>Truth-preserving recommendations</h2><ul>{_items(list(result['truthful_recommendations']))}</ul>
<h2>Accuracy boundary</h2><p>{html.escape(str(result['accuracy_note']))}</p>
</body></html>"""
