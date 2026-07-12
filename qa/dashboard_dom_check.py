"""Static DOM/data contract QA for the generated offline dashboard."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "dashboard" / "Walmart_Dashboard.html").read_text(encoding="utf-8")
data = json.loads((ROOT / "scripts" / "dashboard_data.json").read_text(encoding="utf-8"))

class ContractParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.tabs=[]; self.pages=[]; self.canvases=[]; self.tbodies=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag == "button" and "data-page" in a: self.tabs.append(a["data-page"])
        if tag == "section" and a.get("id", "").startswith("page-"): self.pages.append(a["id"][5:])
        if tag == "canvas" and a.get("id"): self.canvases.append(a["id"])
        if tag == "tbody" and a.get("id"): self.tbodies.append(a["id"])

p=ContractParser(); p.feed(html)
expected=["exec","holiday","types","econ","forecast","stores"]
assert p.tabs == expected, p.tabs
assert sorted(p.pages) == sorted(expected), p.pages
assert len(p.canvases) == 7 and len(p.tbodies) == 5
for key in ["weekly_kpi","holiday_impact","holiday_type_breakdown","regression_results",
            "statistical_tests","forecast_predictions","forecast_metrics","store_segmentation"]:
    assert data.get(key), f"Empty dashboard dataset: {key}"
assert not re.search(r">\s*(?:undefined|NaN)\s*<", html, re.I)
for ident in p.canvases + p.tbodies:
    assert html.count(ident) >= 2, f"DOM target is never populated: {ident}"
print(f"dashboard_contract_ok tabs={len(p.tabs)} canvases={len(p.canvases)} tables={len(p.tbodies)}")
