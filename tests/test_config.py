# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Static OpenCode contracts, not a runtime sandbox.

Saved approvals and plugins are not included. These checks do not prove that an
arbitrary script cannot read secrets. Only the supplied JSON and agent Markdown
are read; credentials are never interpolated or included in diagnostics.
"""

import argparse
import json
from pathlib import Path
import re
import unittest

import yaml


def matches(pattern, value, shell=False):
    """Whole-value wildcards; shell's trailing ' *' also matches no arguments."""
    if shell and pattern.endswith(" *") and value == pattern[:-2]:
        return True
    expression = re.escape(pattern).replace(r"\*", ".*").replace(r"\?", ".")
    return re.fullmatch(expression, value, flags=re.DOTALL) is not None


def evaluate(global_rules, agent_rules, policies, action, resource):
    effect = "ask"
    for rule in [*global_rules, *agent_rules]:
        if matches(rule["action"], action) and matches(
            rule["resource"], resource, shell=action == "shell"
        ):
            effect = rule["effect"]
    policy_effect = None
    for rule in policies:
        if (rule["action"] == "permission" and matches(
                rule["resource"], f"{action}:{resource}", shell=action == "shell")):
            policy_effect = rule["effect"]
    return "deny" if policy_effect == "deny" else effect


def load_contracts(config_path, agents_path):
    def read(path):
        if path.is_symlink() or re.search(r"(?:^|\.)env(?:\.|$)", path.name):
            raise ValueError(f"Refusing sensitive or symlink input: {path}")
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            raise ValueError(f"Cannot read input: {path}") from None

    try:
        raw = json.loads(read(config_path))
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON: {config_path}") from None
    if not isinstance(raw, dict):
        raise ValueError(f"Expected JSON object: {config_path}")
    config = {key: raw.get(key) for key in
              ("permissions", "agents", "default_agent", "subagent_depth", "experimental")}
    agents, sources = {}, {}
    inline = config["agents"] or {}
    if not isinstance(inline, dict):
        raise ValueError(f"Expected agents object: {config_path}")
    for name, data in inline.items():
        agents[name] = data
        sources[name] = f"{config_path} agent={name}"
    if not agents_path.is_dir():
        raise ValueError(f"Missing agents directory: {agents_path}")
    for path in sorted(agents_path.rglob("*.md")):
        text = read(path)
        front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
        if not front:
            raise ValueError(f"Missing YAML frontmatter: {path}")
        try:
            data = yaml.safe_load(front.group(1))
        except yaml.YAMLError:
            raise ValueError(f"Invalid YAML frontmatter: {path}") from None
        if not isinstance(data, dict):
            raise ValueError(f"Expected frontmatter object: {path}")
        name = path.relative_to(agents_path).with_suffix("").as_posix()
        previous = agents.get(name, {})
        if not isinstance(previous, dict):
            raise ValueError(f"Invalid inline agent: {sources[name]}")
        agents[name] = {**previous, **data}
        if "permissions" in previous and "permissions" in data:
            agents[name]["permissions"] = previous["permissions"] + data["permissions"]
        sources[name] = f"{path} agent={name}"
    agents = {name: data for name, data in agents.items()
              if not isinstance(data, dict) or not data.get("disabled", False)}
    return config, agents, sources


class ConfigContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config, cls.agents, cls.sources = load_contracts(CONFIG, AGENTS)
        cls.global_rules = cls.config["permissions"] or []
        cls.policies = (cls.config["experimental"] or {}).get("policies", [])

    def access(self, name, action, resource):
        return evaluate(self.global_rules, self.agents[name].get("permissions", []),
                        self.policies, action, resource)

    def expect(self, name, action, resource, effect):
        with self.subTest(source=self.sources[name], action=action, resource=resource):
            self.assertEqual(self.access(name, action, resource), effect)

    def test_permission_shapes(self):
        groups = [(str(CONFIG), self.global_rules),
                  (f"{CONFIG} experimental.policies", self.policies)]
        groups += [(self.sources[name], data.get("permissions", []))
                   for name, data in self.agents.items() if isinstance(data, dict)]
        for source, rules in groups:
            with self.subTest(source=source):
                self.assertIsInstance(rules, list, "Expected ordered permission array")
                for index, rule in enumerate(rules):
                    with self.subTest(rule=index):
                        self.assertTrue(isinstance(rule, dict), "Expected permission object")
                        self.assertTrue(all(isinstance(rule.get(key), str) and rule[key]
                                            for key in ("action", "resource", "effect")),
                                        "Permission needs action/resource/effect strings")
                        self.assertTrue(rule["effect"] in {"allow", "ask", "deny"},
                                        "Unsupported permission effect")

    def test_agent_shapes_and_children(self):
        for name, data in self.agents.items():
            with self.subTest(source=self.sources[name]):
                self.assertTrue(isinstance(data, dict), "Expected agent object")
                self.assertTrue(data.get("mode", "primary") in {"primary", "subagent", "all"},
                                "Unsupported agent mode")
                if "model" in data:
                    model = data["model"]
                    string_model = isinstance(model, str) and re.fullmatch(
                        r"[^/\s#]+/[^/\s#]+(?:#[^/\s#]+)?", model)
                    expanded_model = isinstance(model, dict) and all(
                        isinstance(model.get(key), str) and model[key]
                        for key in ("providerID", "model")) and (
                        "variant" not in model or
                        isinstance(model["variant"], str) and bool(model["variant"]))
                    self.assertTrue(string_model or expanded_model,
                                    "Expected provider/model[#variant] or expanded model object")
                self.assertTrue("reasoningEffort" not in data, "Use model #variant instead")
                for rule in data.get("permissions", []):
                    if rule["action"] == "subagent" and rule["effect"] == "allow":
                        child = rule["resource"]
                        if "*" in child or "?" in child:
                            continue
                        self.assertTrue(child in self.agents, f"Unknown child agent ID: {child}")
                        self.assertTrue(self.agents[child].get("mode", "primary")
                                        in {"subagent", "all"}, f"Child not callable: {child}")

    def test_default_and_topology(self):
        with self.subTest(source=str(CONFIG)):
            name = self.config["default_agent"]
            self.assertTrue(isinstance(name, str) and name in self.agents,
                            "Default agent must exist")
            self.assertFalse(self.agents[name].get("hidden", False), "Default must be visible")
            self.assertTrue(self.agents[name].get("mode", "primary") in {"primary", "all"},
                            "Default must be primary-capable")
            self.assertEqual(self.config["subagent_depth"], 3)
        for parent, child in zip(("orchestrator", "autopilot", "code"),
                                 ("autopilot", "code", "qwen-task")):
            self.expect(parent, "subagent", child, "allow")

    def test_secret_hard_denials_survive_broad_allows(self):
        permissive = [{"action": "*", "resource": "*", "effect": "allow"}]
        probes = [("read", path) for path in (
            ".env", "nested/.env", ".env.local", ".env.example", "app.env",
            "/path/.env.backup")]
        probes += [("shell", "cat .env"), ("shell", "cat .env.production")]
        for action, resource in probes:
            with self.subTest(source=str(CONFIG), action=action, resource=resource):
                self.assertEqual(evaluate(self.global_rules + permissive, permissive,
                                          self.policies, action, resource), "deny")
            for name in self.agents:
                self.expect(name, action, resource, "deny")
        for name in ("direct", "autopilot", "code", "review"):
            self.expect(name, "read", "src/main.py", "allow")
            self.expect(name, "shell", "uv run pytest tests/test_config.py", "allow")

    def test_skill_and_specialist_routing(self):
        self.assertTrue("config" in self.agents, "Missing config agent")
        for name in self.agents:
            self.expect(name, "skill", "customize-opencode",
                        "allow" if name == "config" else "deny")
        for name in ("direct", "autopilot"):
            for child in ("config", "github", "cloudflare-expert"):
                self.expect(name, "subagent", child, "allow")

    def test_review_commands_and_read_only_boundary(self):
        for command in ("uv run pytest", "uv run python -m pytest",
                        "uv run python3 -m pytest", "pnpm test", "pnpm run test",
                        "pnpm run lint", "pnpm run typecheck"):
            for suffix in ("", " tests"):
                self.expect("review", "shell", command + suffix, "allow")
        for command in ("npm test", "npm run test", "yarn test", "pytest", "pytest tests"):
            self.expect("review", "shell", command, "deny")
        self.expect("review", "edit", "src/main.py", "deny")
        for child in self.agents:
            self.expect("review", "subagent", child, "deny")

    def test_evaluator_order_and_wildcards(self):
        self.assertTrue(matches("a?*", "abc/def"))
        self.assertFalse(matches("a?", "abc"))
        self.assertFalse(matches("cat", "cat file"))
        self.assertTrue(matches("pnpm test *", "pnpm test", shell=True))
        self.assertFalse(matches("pnpm test *", "pnpm test"))
        deny = {"action": "read", "resource": "*", "effect": "deny"}
        allow = {"action": "read", "resource": "src/*", "effect": "allow"}
        self.assertEqual(evaluate([deny], [allow], [], "read", "src/main.py"), "allow")
        self.assertEqual(evaluate([allow], [deny], [], "read", "src/main.py"), "deny")

    def test_policy_order_preserves_underlying_permissions(self):
        deny = {"action": "permission", "resource": "shell:pnpm test *", "effect": "deny"}
        allow = {**deny, "effect": "allow"}
        for effect in ("ask", "deny", "allow"):
            with self.subTest(underlying=effect):
                rules = [{"action": "shell", "resource": "*", "effect": effect}]
                self.assertEqual(evaluate(rules, [], [deny, allow], "shell", "pnpm test"), effect)
                self.assertEqual(evaluate(rules, [], [allow, deny], "shell", "pnpm test"), "deny")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path.home() / ".config/opencode/opencode.json")
    parser.add_argument("--agents", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    CONFIG, AGENTS = args.config.expanduser(), args.agents.expanduser()
    unittest.main(argv=[__file__], verbosity=1)
