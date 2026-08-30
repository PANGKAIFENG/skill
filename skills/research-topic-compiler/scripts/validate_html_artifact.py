#!/usr/bin/env python3
"""Static checks for research-topic-compiler HTML artifacts."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


COMMON_REQUIRED_ATTRIBUTES = {
    "Sources marker": "data-sources",
}

DASHBOARD_TYPES = {
    "learning-report": {
        "root": "data-learning-report",
        "required_attributes": {
            "Report thesis marker": "data-report-thesis",
            "Report navigation marker": "data-report-nav",
            "Reading path marker": "data-reading-path",
            "Mechanism marker": "data-mechanism",
            "Comparison marker": "data-report-comparison",
            "Application marker": "data-application",
            "Boundary marker": "data-report-boundary",
            "Evidence appendix marker": "data-evidence-appendix",
        },
    },
    "concept-lens": {
        "root": "data-concept-lens",
        "required_attributes": {
            "Alpine data binding": "x-data",
            "Concept lineage marker": "data-concept-lineage",
            "Stage tabs marker": "data-stage-tabs",
            "Debt detector marker": "data-debt-detector",
        },
    },
    "research-dashboard": {
        "root": "data-research-dashboard",
        "required_attributes": {
            "Alpine data binding": "x-data",
            "Dashboard summary marker": "data-dashboard-summary",
            "Persona marker": "data-persona-tabs",
            "Evidence map marker": "data-evidence-map",
            "Confidence marker": "data-confidence",
            "Next actions marker": "data-next-actions",
        },
    },
}

FORBIDDEN_PATTERNS = [
    re.compile(r"TODO|TBD|FIXME|PLACEHOLDER", re.IGNORECASE),
    re.compile(r"随着时代的发展"),
    re.compile(r"技术是一把双刃剑"),
    re.compile(r"\blorem\s+ipsum\b", re.IGNORECASE),
]

BACKEND_CALL_PATTERNS = [
    re.compile(r"\bfetch\s*\(", re.IGNORECASE),
    re.compile(r"\bXMLHttpRequest\b", re.IGNORECASE),
    re.compile(r"\baxios\s*\.", re.IGNORECASE),
    re.compile(r"[\"']/api/", re.IGNORECASE),
    re.compile(r"(?:^|[\"'(])/api/", re.IGNORECASE),
]

LEARNING_CONTROL_SURFACE_PATTERNS = [
    re.compile(r"\bNBE(?:\s+Action)?\b", re.IGNORECASE),
    re.compile(r"\bterminal\s+status\b", re.IGNORECASE),
    re.compile(r"\b(?:Evidence|Explanation)\s+Framework\s+V\w*\b", re.IGNORECASE),
    re.compile(r"\bconfidence\s+ledger\b", re.IGNORECASE),
    re.compile(r"证据标签筛选|证据覆盖率|研究终态"),
]

LEARNING_SUMMARY_FIELDS = {
    "primary reader": re.compile(r"(?:primary\s+reader|主要读者|目标读者)", re.IGNORECASE),
    "research job": re.compile(r"(?:research\s+job|研究任务|学习任务)", re.IGNORECASE),
    "central thesis": re.compile(r"(?:central\s+thesis|中心论点|核心论点)", re.IGNORECASE),
    "core claims": re.compile(r"(?:core\s+claims?|核心观点|核心判断)", re.IGNORECASE),
    "intended action": re.compile(r"(?:intended\s+actions?|下一步行动|改进行动|行动建议)", re.IGNORECASE),
    "important boundary": re.compile(r"(?:important\s+boundary|重要边界|适用边界)", re.IGNORECASE),
    "artifact path": re.compile(r"(?:artifact\s+path|产物路径|报告路径)", re.IGNORECASE),
    "audit location": re.compile(r"(?:audit\s+location|审计位置|来源位置|证据位置)", re.IGNORECASE),
    "validation result": re.compile(r"(?:validation\s+result|验证结果|验收结果)", re.IGNORECASE),
}

VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class ArtifactParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.attributes: set[str] = set()
        self.attribute_values: list[str] = []
        self.executable_attribute_values: list[str] = []
        self.attributes_by_root = {dashboard_type: set() for dashboard_type in DASHBOARD_TYPES}
        self.attribute_values_by_root = {
            dashboard_type: [] for dashboard_type in DASHBOARD_TYPES
        }
        self.visible_text_by_root = {dashboard_type: [] for dashboard_type in DASHBOARD_TYPES}
        self.root_occurrences: list[str] = []
        self.script_sources: list[str] = []
        self.script_text: list[str] = []
        self.learning_evidence_elements: list[tuple[str, dict[str, str]]] = []
        self.learning_claim_count = 0
        self.learning_visual_count = 0
        self.learning_action_count = 0
        self.learning_heading_count = 0
        self.learning_reading_text: list[str] = []
        self.ids: set[str] = set()
        self.internal_hrefs: list[str] = []
        self.required_assets: list[str] = []
        self.visible_text: list[str] = []
        self._tag_stack: list[tuple[str, str | None, bool]] = []
        self._inside_script = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        values = {name.lower(): value or "" for name, value in attrs}
        names = set(values)
        if values.get("id"):
            self.ids.add(values["id"])
        if values.get("href", "").startswith("#"):
            self.internal_hrefs.append(values["href"][1:])
        if tag == "script" and values.get("src"):
            self.required_assets.append(values["src"])
        if tag == "link" and "stylesheet" in values.get("rel", "").lower() and values.get("href"):
            self.required_assets.append(values["href"])
        if tag in {"img", "source", "video", "audio", "iframe", "object", "embed"}:
            for asset_name in ("src", "srcset", "data"):
                asset_value = values.get(asset_name, "")
                if asset_value and not asset_value.lstrip().lower().startswith("data:"):
                    self.required_assets.append(asset_value)
        self.attributes.update(names)
        self.attribute_values.extend(value for value in values.values() if value)
        for name, value in values.items():
            executable_binding = name.startswith(("x-", "@", "on", ":"))
            request_target = name in {"action", "formaction"}
            script_source = tag == "script" and name == "src"
            javascript_url = value.lstrip().lower().startswith("javascript:")
            if value and (executable_binding or request_target or script_source or javascript_url):
                self.executable_attribute_values.append(value)

        declared_roots = [
            dashboard_type
            for dashboard_type, rules in DASHBOARD_TYPES.items()
            if rules["root"] in names
        ]
        self.root_occurrences.extend(declared_roots)

        inherited_root = self._tag_stack[-1][1] if self._tag_stack else None
        inherited_evidence = self._tag_stack[-1][2] if self._tag_stack else False
        active_root = declared_roots[0] if len(declared_roots) == 1 else inherited_root
        inside_learning_evidence = inherited_evidence or (
            active_root == "learning-report" and "data-evidence-appendix" in names
        )
        if active_root:
            self.attributes_by_root[active_root].update(names)
            self.attribute_values_by_root[active_root].extend(
                value for value in values.values() if value
            )
            if active_root == "learning-report":
                if "data-core-claim" in names:
                    self.learning_claim_count += 1
                if "data-visual-memory" in names:
                    self.learning_visual_count += 1
                if "data-action" in names:
                    self.learning_action_count += 1
                if tag in {"h1", "h2"}:
                    self.learning_heading_count += 1
                if "data-evidence-appendix" in names:
                    self.learning_evidence_elements.append((tag, values))

        if tag == "script":
            self._inside_script = True
            if values.get("src"):
                self.script_sources.append(values["src"])

        if tag not in VOID_ELEMENTS:
            self._tag_stack.append((tag, active_root, inside_learning_evidence))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_ELEMENTS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "script":
            self._inside_script = False
        for index in range(len(self._tag_stack) - 1, -1, -1):
            if self._tag_stack[index][0] == tag:
                del self._tag_stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if self._inside_script:
            self.script_text.append(data)
        else:
            self.visible_text.append(data)
            active_root = self._tag_stack[-1][1] if self._tag_stack else None
            if active_root:
                self.visible_text_by_root[active_root].append(data)
                if active_root == "learning-report" and not self._tag_stack[-1][2]:
                    self.learning_reading_text.append(data)


def _parse(text: str) -> ArtifactParser:
    parser = ArtifactParser()
    parser.feed(text)
    parser.close()
    return parser


def validate(path: Path) -> tuple[bool, list[str]]:
    issues: list[str] = []
    if not path.exists():
        return False, [f"File not found: {path}"]
    if path.suffix.lower() not in {".html", ".htm"}:
        issues.append("File extension should be .html or .htm")

    text = path.read_text(encoding="utf-8", errors="ignore")
    parser = _parse(text)

    if not re.search(r"<html\b", text, flags=re.IGNORECASE):
        issues.append("Missing <html> tag")
    if not re.search(r"</html>", text, flags=re.IGNORECASE):
        issues.append("Missing closing </html> tag")
    if not parser.script_sources and not parser.script_text and "data-learning-report" not in parser.attributes:
        issues.append("Missing <script> tag")

    sources = [source.lower() for source in parser.script_sources]

    if len(parser.root_occurrences) != 1:
        issues.append("Expected exactly one dashboard root marker")
    else:
        dashboard_type = parser.root_occurrences[0]
        rules = DASHBOARD_TYPES[dashboard_type]
        scoped_attributes = parser.attributes_by_root[dashboard_type]
        required = {**COMMON_REQUIRED_ATTRIBUTES, **rules["required_attributes"]}
        for label, attribute in required.items():
            if attribute not in scoped_attributes:
                issues.append(f"Missing required attribute: {label} ({attribute})")

        if dashboard_type != "learning-report":
            if not any("cdn.tailwindcss.com" in source for source in sources):
                issues.append("Missing required script: Tailwind CSS CDN")
            if not any("alpinejs" in source for source in sources):
                issues.append("Missing required script: Alpine.js CDN")

        if dashboard_type == "learning-report":
            if not 3 <= parser.learning_claim_count <= 5:
                issues.append("Learning report needs 3-5 core claims")
            if not 1 <= parser.learning_visual_count <= 3:
                issues.append("Learning report needs 1-3 visual memory markers")
            if parser.learning_action_count < 2:
                issues.append("Learning report needs at least 2 bounded actions")
            if parser.learning_heading_count < 2:
                issues.append("Learning report needs a title and section headings")
            if not parser.learning_evidence_elements:
                issues.append("Learning report evidence appendix is empty")
            else:
                for tag, attrs in parser.learning_evidence_elements:
                    placement = attrs.get("data-evidence-placement", "")
                    if tag != "details" and placement not in {"endnotes", "footnotes", "collapsed"}:
                        issues.append("Learning report evidence must be secondary or collapsible")
                        break
                    if tag == "details" and "open" in attrs:
                        issues.append("Learning report evidence appendix must be collapsed by default")
                        break

            reading_text = " ".join(parser.learning_reading_text)
            for pattern in LEARNING_CONTROL_SURFACE_PATTERNS:
                match = pattern.search(reading_text)
                if match:
                    issues.append(
                        "Research-control vocabulary found in learning report reading layer: "
                        f"{match.group(0)}"
                    )
                    break

            if parser.required_assets:
                issues.append(
                    "Learning report must be self-contained; required asset found: "
                    f"{parser.required_assets[0]}"
                )

            style_blocks = re.findall(
                r"<style\b[^>]*>(.*?)</style>", text, flags=re.IGNORECASE | re.DOTALL
            )
            for style_text in style_blocks:
                match = re.search(
                    r"(?:@import\s+|url\s*\(\s*[\"']?)https?://",
                    style_text,
                    flags=re.IGNORECASE,
                )
                if match:
                    issues.append("Learning report CSS must not require remote assets")
                    break

            unresolved = sorted(
                target for target in set(parser.internal_hrefs) if target and target not in parser.ids
            )
            if unresolved:
                issues.append(
                    "Unresolved internal link target: " + ", ".join(unresolved[:3])
                )

        if dashboard_type == "concept-lens":
            if len(re.findall(r"https?://", text)) < 3:
                issues.append("Expected at least 3 source or CDN URLs")
            visible = " ".join(parser.visible_text_by_root[dashboard_type])
            attribute_values = " ".join(parser.attribute_values_by_root[dashboard_type])
            if (
                "data-copy-action" not in scoped_attributes
                and not re.search(r"copy|复制|clipboard", visible, flags=re.IGNORECASE)
                and not re.search(r"copy|clipboard", attribute_values, flags=re.IGNORECASE)
            ):
                issues.append("Missing copy interaction hint")

    for pattern in FORBIDDEN_PATTERNS:
        match = pattern.search(text)
        if match:
            issues.append(f"Forbidden or unresolved text found: {match.group(0)}")

    executable_text = "\n".join(
        [*parser.script_text, *parser.executable_attribute_values]
    )
    for pattern in BACKEND_CALL_PATTERNS:
        match = pattern.search(executable_text)
        if match:
            issues.append(f"Forbidden backend call found: {match.group(0)}")
            break

    return not issues, issues


def validate_learning_summary(path: Path) -> list[str]:
    """Validate the delivery companion for a learning-report artifact."""
    if not path.exists():
        return [f"Companion summary not found: {path}"]

    text = path.read_text(encoding="utf-8", errors="ignore").strip()
    if not text:
        return [f"Companion summary is empty: {path}"]

    issues: list[str] = []
    for label, pattern in LEARNING_SUMMARY_FIELDS.items():
        if not pattern.search(text):
            issues.append(f"Learning report summary missing field: {label}")

    claim_section = re.search(
        r"(?:core\s+claims?|核心观点|核心判断)\s*[:：]?\s*(.*?)(?=\n#{1,6}\s|\Z)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if claim_section is None:
        issues.append("Learning report summary needs a 3-5 item core-claim section")
    else:
        bullet_count = len(
            re.findall(r"(?m)^\s*(?:[-*+]\s+|\d+[.)、]\s*)", claim_section.group(1))
        )
        if not 3 <= bullet_count <= 5:
            issues.append("Learning report summary needs 3-5 core claims")

    validation_section = re.search(
        r"(?:validation\s+result|验证结果|验收结果)\s*[:：]?\s*(.*?)(?=\n#{1,6}\s|\Z)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if validation_section is not None and not re.search(
        r"\b(?:pass|passed|fail|failed|pending|limited)\b|通过|失败|待验证|受限",
        validation_section.group(1),
        flags=re.IGNORECASE,
    ):
        issues.append("Learning report summary validation result needs an explicit status")

    return issues


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print(
            "Usage: validate_html_artifact.py <artifact.html> [companion-summary.md]",
            file=sys.stderr,
        )
        return 2

    path = Path(sys.argv[1]).expanduser().resolve()
    ok, issues = validate(path)
    if len(sys.argv) == 3:
        summary_path = Path(sys.argv[2]).expanduser().resolve()
        html_text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        if "data-learning-report" in html_text:
            issues.extend(validate_learning_summary(summary_path))
        elif not summary_path.exists():
            issues.append(f"Companion summary not found: {summary_path}")
        elif not summary_path.read_text(encoding="utf-8", errors="ignore").strip():
            issues.append(f"Companion summary is empty: {summary_path}")
        ok = not issues
    if ok:
        print(f"PASS: {path}")
        return 0

    print(f"FAIL: {path}")
    for issue in issues:
        print(f"- {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
