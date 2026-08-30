from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = SKILL_ROOT / "scripts" / "validate_html_artifact.py"
SPEC = importlib.util.spec_from_file_location("validate_html_artifact", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def html_document(body: str, *, extra_script: str = "") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body>{body}<script>{extra_script}</script></body>
</html>
"""


def learning_html_document(body: str, *, extra_script: str = "") -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head>
<body>{body}<script>{extra_script}</script></body>
</html>
"""


CONCEPT_BODY = """
<main data-concept-lens x-data="{}">
  <section data-concept-lineage></section>
  <nav data-stage-tabs></nav>
  <section data-debt-detector></section>
  <section data-sources><a href="https://example.com/a">A</a></section>
  <button data-copy-action>Copy</button>
</main>
"""

RESEARCH_BODY = """
<main data-research-dashboard x-data="{persona: 'product'}">
  <header data-dashboard-summary></header>
  <nav data-persona-tabs></nav>
  <section data-evidence-map></section>
  <section data-confidence></section>
  <section data-next-actions></section>
  <section data-sources><span data-source-path>sources/local-report.md</span></section>
</main>
"""

LEARNING_BODY = """
<main data-learning-report>
  <header data-report-thesis><h1>主题</h1></header>
  <nav data-report-nav><a href="#mechanism">机制</a></nav>
  <section data-reading-path><h2>核心判断</h2><article data-core-claim>一</article><article data-core-claim>二</article><article data-core-claim>三</article></section>
  <section id="mechanism" data-mechanism><div data-visual-memory>流程</div></section>
  <section data-report-comparison><p>对照</p></section>
  <section data-application><p>行动</p><article data-action>一</article><article data-action>二</article></section>
  <aside data-report-boundary><p>边界</p></aside>
  <aside data-sources><details data-evidence-appendix data-evidence-placement="collapsed"><summary>来源</summary><p>Source</p></details></aside>
</main>
"""


class HtmlArtifactValidatorTests(unittest.TestCase):
    def validate_text(self, text: str, suffix: str = ".html") -> tuple[bool, list[str]]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / f"dashboard{suffix}"
            path.write_text(text, encoding="utf-8")
            return VALIDATOR.validate(path)

    def assert_invalid(self, text: str, expected_issue: str) -> None:
        ok, issues = self.validate_text(text)
        self.assertFalse(ok)
        self.assertTrue(
            any(expected_issue in issue for issue in issues),
            f"Expected issue containing {expected_issue!r}, got {issues!r}",
        )

    def test_legacy_concept_lens_dashboard_passes(self) -> None:
        ok, issues = self.validate_text(html_document(CONCEPT_BODY))
        self.assertTrue(ok, issues)

    def test_legacy_clipboard_event_attribute_passes(self) -> None:
        body = CONCEPT_BODY.replace(
            "<button data-copy-action>Copy</button>",
            '<button @click="navigator.clipboard.writeText(\'example\')">摘要</button>',
        )
        ok, issues = self.validate_text(html_document(body))
        self.assertTrue(ok, issues)

    def test_general_research_dashboard_with_local_source_path_passes(self) -> None:
        ok, issues = self.validate_text(html_document(RESEARCH_BODY))
        self.assertTrue(ok, issues)

    def test_learning_report_passes_without_remote_framework_scripts(self) -> None:
        ok, issues = self.validate_text(learning_html_document(LEARNING_BODY))
        self.assertTrue(ok, issues)

    def test_learning_report_requires_secondary_evidence(self) -> None:
        body = LEARNING_BODY.replace(
            '<details data-evidence-appendix data-evidence-placement="collapsed">',
            '<section data-evidence-appendix>',
        ).replace("</details>", "</section>")
        self.assert_invalid(
            learning_html_document(body), "evidence must be secondary or collapsible"
        )

    def test_learning_report_requires_core_claims(self) -> None:
        body = LEARNING_BODY.replace('<article data-core-claim>三</article>', "")
        self.assert_invalid(learning_html_document(body), "3-5 core claims")

    def test_learning_report_rejects_too_many_core_claims(self) -> None:
        body = LEARNING_BODY.replace(
            '<article data-core-claim>三</article>',
            '<article data-core-claim>三</article><article data-core-claim>四</article><article data-core-claim>五</article><article data-core-claim>六</article>',
        )
        self.assert_invalid(learning_html_document(body), "3-5 core claims")

    def test_learning_report_requires_bounded_actions(self) -> None:
        body = LEARNING_BODY.replace('<article data-action>二</article>', "")
        self.assert_invalid(learning_html_document(body), "at least 2 bounded actions")

    def test_learning_report_rejects_open_evidence_appendix(self) -> None:
        body = LEARNING_BODY.replace(
            '<details data-evidence-appendix', '<details open data-evidence-appendix'
        )
        self.assert_invalid(learning_html_document(body), "collapsed by default")

    def test_learning_report_rejects_control_surface_in_reading_layer(self) -> None:
        body = LEARNING_BODY.replace("核心判断", "核心判断与 terminal status")
        self.assert_invalid(learning_html_document(body), "Research-control vocabulary")

    def test_learning_report_allows_control_vocabulary_in_audit_layer(self) -> None:
        body = LEARNING_BODY.replace("Source", "terminal status: complete")
        ok, issues = self.validate_text(learning_html_document(body))
        self.assertTrue(ok, issues)

    def test_learning_report_rejects_required_remote_asset(self) -> None:
        text = learning_html_document(LEARNING_BODY).replace(
            "</head>", '<link rel="stylesheet" href="https://example.com/report.css"></head>'
        )
        self.assert_invalid(text, "must be self-contained")

    def test_learning_report_rejects_unresolved_internal_link(self) -> None:
        body = LEARNING_BODY.replace('href="#mechanism"', 'href="#missing"')
        self.assert_invalid(learning_html_document(body), "Unresolved internal link target")

    def test_learning_report_summary_contract_passes(self) -> None:
        summary = """# Delivery companion

## 主要读者
增长产品经理。

## Research Job
理解激活失败机制并决定下一轮验证。

## 中心论点
注册完成不等于用户已经跨过价值门槛。

## 核心观点
- 激活对象是首次价值闭环，不是账户状态。
- 认知成本和协作风险会产生不同的退出行为。
- 实验必须绑定机制与可判定信号。

## 下一步行动
重写第一个项目的引导并运行分层实验。

## 重要边界
访谈不能单独证明人群占比。

## 产物路径
`report.html`

## 审计位置
报告末尾折叠来源附录。

## 验证结果
PASS：静态和浏览器检查通过。
"""
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "summary.md"
            path.write_text(summary, encoding="utf-8")
            self.assertEqual(VALIDATOR.validate_learning_summary(path), [])

    def test_learning_report_summary_requires_semantic_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "summary.md"
            path.write_text("# 有内容但没有交付合同\n", encoding="utf-8")
            issues = VALIDATOR.validate_learning_summary(path)
            self.assertTrue(any("central thesis" in issue for issue in issues), issues)
            self.assertTrue(any("3-5 item core-claim" in issue for issue in issues), issues)

    def test_learning_report_summary_requires_three_to_five_claims(self) -> None:
        summary = """主要读者：产品经理
Research Job：学习机制
中心论点：一个判断
核心观点：
- 观点一
- 观点二
下一步行动：运行实验
重要边界：仅适用于当前样本
产物路径：report.html
审计位置：文末
验证结果：PASS
"""
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "summary.md"
            path.write_text(summary, encoding="utf-8")
            issues = VALIDATOR.validate_learning_summary(path)
            self.assertIn("Learning report summary needs 3-5 core claims", issues)

    def test_missing_general_marker_fails(self) -> None:
        body = RESEARCH_BODY.replace(" data-evidence-map", "")
        self.assert_invalid(html_document(body), "Evidence map marker")

    def test_both_dashboard_roots_fail(self) -> None:
        body = RESEARCH_BODY.replace(
            "data-research-dashboard", "data-research-dashboard data-concept-lens"
        )
        self.assert_invalid(html_document(body), "exactly one dashboard root")

    def test_duplicate_same_dashboard_root_fails(self) -> None:
        body = RESEARCH_BODY + '<aside data-research-dashboard x-data="{}"></aside>'
        self.assert_invalid(html_document(body), "exactly one dashboard root")

    def test_required_marker_outside_dashboard_root_fails(self) -> None:
        body = RESEARCH_BODY.replace("<section data-evidence-map></section>", "")
        body += "<section data-evidence-map></section>"
        self.assert_invalid(html_document(body), "Evidence map marker")

    def test_marker_only_in_comment_fails(self) -> None:
        body = RESEARCH_BODY.replace(" data-evidence-map", "") + "<!-- data-evidence-map -->"
        self.assert_invalid(html_document(body), "Evidence map marker")

    def test_marker_only_in_script_string_fails(self) -> None:
        body = RESEARCH_BODY.replace(" data-evidence-map", "")
        self.assert_invalid(
            html_document(body, extra_script="const fake = 'data-evidence-map';"),
            "Evidence map marker",
        )

    def test_backend_call_fails(self) -> None:
        self.assert_invalid(
            html_document(RESEARCH_BODY, extra_script="fetch('/api/research')"),
            "backend call",
        )

    def test_backend_like_text_in_presentation_attribute_passes(self) -> None:
        body = RESEARCH_BODY.replace(
            "<header data-dashboard-summary></header>",
            '<header data-dashboard-summary title="Example: fetch(\'/api/docs\')"></header>',
        )
        ok, issues = self.validate_text(html_document(body))
        self.assertTrue(ok, issues)

    def test_backend_call_in_alpine_attribute_fails(self) -> None:
        body = RESEARCH_BODY.replace(
            "x-data=\"{persona: 'product'}\"",
            "x-data=\"{persona: 'product'}\" x-init=\"fetch('/api/research')\"",
        )
        self.assert_invalid(html_document(body), "backend call")

    def test_axios_call_in_event_attribute_fails(self) -> None:
        body = RESEARCH_BODY.replace(
            "<section data-next-actions></section>",
            '<button data-next-actions @click="axios.get(\'/api/research\')">Run</button>',
        )
        self.assert_invalid(html_document(body), "backend call")

    def test_unresolved_placeholder_fails(self) -> None:
        self.assert_invalid(html_document(RESEARCH_BODY + "<p>TODO</p>"), "TODO")

    def test_non_html_extension_fails(self) -> None:
        ok, issues = self.validate_text(html_document(RESEARCH_BODY), suffix=".txt")
        self.assertFalse(ok)
        self.assertIn("File extension should be .html or .htm", issues)

    def test_persisted_general_dashboard_fixture_passes(self) -> None:
        fixture = SKILL_ROOT / "evals" / "fixtures" / "research-dashboard" / "dashboard.html"
        ok, issues = VALIDATOR.validate(fixture)
        self.assertTrue(ok, issues)


if __name__ == "__main__":
    unittest.main()
