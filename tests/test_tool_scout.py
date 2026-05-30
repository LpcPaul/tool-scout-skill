import importlib.util
import pathlib
import sys
import unittest


SCRIPT_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / ".claude"
    / "skills"
    / "tool-scout"
    / "scripts"
    / "tool_scout.py"
)

spec = importlib.util.spec_from_file_location("tool_scout", SCRIPT_PATH)
tool_scout = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = tool_scout
spec.loader.exec_module(tool_scout)


class ToolScoutTests(unittest.TestCase):
    def test_query_plan_expands_feishu_claude_code(self):
        plan = tool_scout.build_query_plan("通过飞书机器人命令 Claude Code")
        joined = " ".join(plan.queries).lower()
        self.assertIn("feishu", joined)
        self.assertIn("lark", joined)
        self.assertIn("claude code", joined)
        self.assertLessEqual(len(plan.queries), 12)

    def test_target_product_helper_needs_native_feature_audit(self):
        plan = tool_scout.build_query_plan(
            "Codex Desktop helper for selected text comments and side chat questions"
        )
        joined = " ".join(plan.native_audit_queries).lower()
        self.assertTrue(plan.native_audit_queries)
        self.assertIn("codex desktop", joined)
        self.assertIn("selected text", joined)
        self.assertIn("context menu", joined)

    def test_general_tool_search_does_not_force_native_feature_audit(self):
        plan = tool_scout.build_query_plan("MCP server for browser automation")
        self.assertEqual(plan.native_audit_queries, [])

    def test_dedupe_merges_same_url(self):
        candidates = [
            tool_scout.Candidate(
                name="A",
                kind="GitHub repo",
                source="github",
                url="https://github.com/example/tool",
                description="first",
            ),
            tool_scout.Candidate(
                name="A package",
                kind="npm package",
                source="npm",
                url="https://github.com/example/tool",
                description="second",
            ),
        ]
        deduped = tool_scout.dedupe_candidates(candidates)
        self.assertEqual(len(deduped), 1)
        self.assertIn("npm", deduped[0].sources)

    def test_v1_rejects_wrong_direction(self):
        need = tool_scout.NeedProfile(
            raw="飞书机器人控制 Claude Code",
            normalized_goal="Feishu controls Claude Code",
            positive_terms={"feishu", "lark", "claude", "code", "control"},
            hard_terms={"feishu", "claude"},
            negative_patterns=("claude controls feishu",),
        )
        candidate = tool_scout.Candidate(
            name="wrong-way",
            kind="MCP server",
            source="test",
            url="https://example.com",
            description="Claude controls Feishu documents",
        )
        tool_scout.apply_gates_and_scores(candidate, need)
        self.assertFalse(candidate.v1)

    def test_score_prefers_direct_evidence(self):
        need = tool_scout.NeedProfile(
            raw="Feishu bot controls Claude Code",
            normalized_goal="Feishu bot controls Claude Code",
            positive_terms={"feishu", "lark", "bot", "controls", "claude", "code"},
            hard_terms={"feishu", "claude"},
            negative_patterns=(),
        )
        candidate = tool_scout.Candidate(
            name="bridge",
            kind="GitHub repo",
            source="github",
            url="https://github.com/example/bridge",
            description="Feishu/Lark bot controls Claude Code CLI with streaming output",
            stars=100,
            updated_at="2026-05-01T00:00:00Z",
            license="MIT",
        )
        tool_scout.apply_gates_and_scores(candidate, need)
        self.assertTrue(candidate.v0)
        self.assertTrue(candidate.v1)
        self.assertGreater(candidate.score, 0.5)


if __name__ == "__main__":
    unittest.main()
