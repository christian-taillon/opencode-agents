# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Small static contracts for V2.0.26; not a runtime or sandbox test.

Default inputs are portable and sanitized. --config opts into inspecting a
supplied JSON installation candidate without credential interpolation/output.
"""

import argparse
import json
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_CLOUDFLARE = "cloudflare" + "-expert"
RETIRED = {
    "code",
    "orchestrator",
    "ops-fast",
    "ops-context",
    "qwen-task",
    "yolo",
    PREVIOUS_CLOUDFLARE,
}
PRIMARIES = {"direct", "autopilot", "contained"}
ADAPTERS = {"claude", "antigravity"}
LEAVES = {
    "coder",
    "review",
    "adversarial",
    "utility",
    "operations",
    "config",
    "github",
    "cloudflare",
    "gated-direct",
    "tutor",
    *ADAPTERS,
    "contained-code-local",
    "contained-net-research",
    "contained-text-only",
}
FIELDS = {
    "model",
    "request",
    "system",
    "description",
    "mode",
    "hidden",
    "color",
    "steps",
    "disabled",
    "permissions",
}
CONFIG_FIELDS = {
    "$schema",
    "shell",
    "model",
    "default_agent",
    "update",
    "share",
    "enterprise",
    "username",
    "permissions",
    "agents",
    "snapshots",
    "watcher",
    "formatter",
    "lsp",
    "media",
    "tool_output",
    "mcp",
    "compaction",
    "skills",
    "commands",
    "instructions",
    "references",
    "websearch",
    "plugins",
    "worktree",
    "warming",
    "providers",
    "experimental",
}


def read_safe(path):
    if any(p.is_symlink() for p in (path, *path.parents)) or any(
        re.search(r"(?:^|\.)env(?:\.|$)", p) for p in path.parts
    ):
        raise ValueError("Refusing sensitive or symlink input")
    return path.read_text(encoding="utf-8")


def load_agents(root):
    agents, bodies = {}, {}
    for path in sorted(root.rglob("*.md")):
        text = read_safe(path)
        front = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
        if not front:
            raise ValueError("Missing agent/document frontmatter")
        data = yaml.safe_load(front[1])
        if not isinstance(data, dict):
            raise ValueError("Invalid frontmatter object")
        if data.get("disabled"):
            continue
        name = path.relative_to(root).with_suffix("").as_posix()
        agents[name], bodies[name] = data, text[front.end() :]
    return agents, bodies


def has_rule(data, action, resource, effect):
    return {"action": action, "resource": resource, "effect": effect} in data.get(
        "permissions", []
    )


def matches(value, pattern):
    expression = (
        re.escape(pattern.replace("\\", "/"))
        .replace(r"\ ", " ")
        .replace(r"\*", ".*")
        .replace(r"\?", ".")
    )
    if expression.endswith(" .*"):
        expression = expression[:-3] + "( .*)?"
    return re.fullmatch(expression, value.replace("\\", "/"), re.S) is not None


def effect(action, resource, *rulesets):
    result = "ask"
    for rules in rulesets:
        for rule in rules:
            if matches(action, rule["action"]) and matches(resource, rule["resource"]):
                result = rule["effect"]
    return result


class ConfigContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads(read_safe(CONFIG))
        cls.agents, cls.bodies = load_agents(AGENTS)

    def rules(self, name):
        # Pinned defaults/built-ins precede global JSON, then global Markdown.
        # Plan's runtime-directory edit exception is outside these shell probes.
        # Project overrides need their own later entries.
        defaults = [
            {"action": "*", "resource": "*", "effect": "allow"},
            {"action": "read", "resource": "*.env", "effect": "ask"},
            {"action": "read", "resource": "*.env.*", "effect": "ask"},
            {"action": "read", "resource": "*.env.example", "effect": "allow"},
        ]
        builtin = [{"action": "question", "resource": "*", "effect": "allow"}]
        if name == "plan":
            builtin.append({"action": "edit", "resource": "*", "effect": "deny"})
        return [
            defaults,
            builtin if name in {"build", "plan"} else [],
            self.config.get("permissions", []),
            self.config.get("agents", {}).get(name, {}).get("permissions", []),
            self.agents.get(name, {}).get("permissions", []),
        ]

    def expect(self, name, action, resource, expected):
        with self.subTest(agent=name, action=action, resource=resource):
            self.assertEqual(effect(action, resource, *self.rules(name)), expected)

    def test_effective_ordered_boundaries(self):
        for name in self.agents:
            if name not in PRIMARIES:
                for child in self.agents:
                    self.expect(name, "subagent", child, "deny")
            if name not in ADAPTERS:
                for tool in ("switchboard_delegate", "switchboard_harnesses"):
                    self.expect(name, tool, "*", "deny")
            if name in ("direct", "autopilot"):
                for child in ADAPTERS:
                    self.expect(
                        name,
                        "subagent",
                        child,
                        "allow" if (name, child) == ("direct", "claude") else "deny",
                    )
        for name in ("review", "adversarial", "operations", "tutor"):
            self.expect(name, "edit", "src/main.py", "deny")
        for name in (
            "direct",
            "autopilot",
            "coder",
            "utility",
            "operations",
            "config",
            "github",
            "cloudflare",
            "gated-direct",
            "plan",
            "build",
        ):
            for command in (
                "sudo ls",
                "git reset --hard HEAD",
                "git push --force origin",
                "git push -f origin",
            ):
                self.expect(name, "shell", command, "deny")
        for command in (
            "rm -rf /tmp/opencode/work/../outside",
            "rm -rf /tmp/opencode/work /outside",
        ):
            self.expect("coder", "shell", command, "ask")
            self.assertEqual(
                effect("shell", command, self.config.get("permissions", [])), "ask"
            )
        self.expect("plan", "shell", "uv run pytest tests", "ask")
        self.expect("review", "shell", "pnpm test", "allow")
        self.expect("direct", "execute", "*", "allow")

    def test_effective_models_and_wildcards(self):
        self.assertTrue(matches("pnpm test", "pnpm test *"))
        self.assertTrue(matches("a/b", r"a\?"))
        self.assertEqual(
            effect(
                "edit", "file", [{"action": "*", "resource": "*", "effect": "allow"}]
            ),
            "allow",
        )

        def provider(model):
            return (
                model.split("/", 1)[0]
                if isinstance(model, str)
                else model.get("providerID", "")
            )

        self.assertNotIn("anthropic", str(self.config.get("model", "")).lower())
        self.assertNotIn("claude", str(self.config.get("model", "")).lower())
        self.assertTrue(
            "anthropic" not in self.config.get("providers", {}),
            "Native Anthropic provider configured",
        )
        for data in self.config.get("providers", {}).values():
            for name, model in data.get("models", {}).items():
                self.assertNotRegex(name.lower(), "anthropic|claude")
                self.assertNotRegex(
                    str(model.get("modelID", "")).lower(), "anthropic|claude"
                )
        for name in self.agents.keys() | self.config.get("agents", {}).keys():
            inline = self.config.get("agents", {}).get(name, {})
            self.assertNotRegex(
                str(inline.get("model", "")).lower(), "anthropic|claude", name
            )
            selected = self.agents.get(name, {}).get(
                "model", inline.get("model", self.config.get("model", ""))
            )
            self.assertNotEqual(provider(selected), "anthropic", name)
            self.assertNotRegex(str(selected).lower(), "anthropic|claude", name)
        for name, model in (
            ("direct", "openai/gpt-6.1-sol#xhigh"),
            ("coder", "openai/gpt-6.1-sol#high"),
            ("cloudflare", "openai/gpt-6.1-sol#high"),
        ):
            self.assertEqual(self.agents[name]["model"], model)

    def test_explicit_adapter_roles(self):
        for name in ADAPTERS:
            self.assertEqual(self.agents[name]["mode"], "subagent")
            self.assertEqual(self.agents[name]["model"], "openai/gpt-6-luna#high")

    def test_explicit_claude_request_route(self):
        self.expect("direct", "subagent", "claude", "allow")
        self.expect("direct", "subagent", "antigravity", "deny")
        self.expect("autopilot", "subagent", "claude", "deny")
        for tool in ("switchboard_delegate", "switchboard_harnesses"):
            self.expect("direct", tool, "*", "deny")
            self.expect("claude", tool, "*", "allow")
        self.expect("claude", "shell", "claude synthetic-task", "deny")
        self.assertIn(
            "Only when the user explicitly requests `claude`", self.bodies["direct"]
        )
        self.assertIn("Never select it automatically", self.bodies["direct"])
        self.assertIn(
            "explicit user-requested delegation from `direct`", self.bodies["claude"]
        )

    def test_native_shapes(self):
        self.assertIsInstance(self.config, dict)
        self.assertFalse(set(self.config) - CONFIG_FIELDS, "Unsupported config fields")
        experimental = self.config.get("experimental", {})
        self.assertFalse(
            set(experimental) - {"subagent_depth", "policies", "portable_shell_scanner"}
        )
        policies = experimental.get("policies", [])
        for policy in policies:
            self.assertIn(
                policy["action"], {"provider.use", "tool.use", "integration.use"}
            )
            self.assertIn(policy["effect"], {"allow", "deny"})
        groups = [self.config.get("permissions", []), policies]
        for name, data in {**self.agents, **self.config.get("agents", {})}.items():
            with self.subTest(agent=name):
                self.assertFalse(set(data) - FIELDS, "Unsupported agent fields")
                self.assertIn(
                    data.get("mode", "primary"), {"primary", "subagent", "all"}
                )
                if "model" in data:
                    model = data["model"]
                    if isinstance(model, str):
                        self.assertRegex(model, r"^[^/\s#]+/[^\s#]+(?:#[^\s#]+)?$")
                    else:
                        self.assertIsInstance(model, dict)
                        self.assertFalse(
                            set(model) - {"providerID", "model", "variant"}
                        )
                        for field in ("providerID", "model"):
                            self.assertIsInstance(model.get(field), str)
                if "steps" in data:
                    self.assertTrue(type(data["steps"]) is int and data["steps"] > 0)
                groups.append(data.get("permissions", []))
        for rules in groups:
            self.assertIsInstance(rules, list)
            for rule in rules:
                self.assertEqual(set(rule), {"action", "resource", "effect"})
                self.assertTrue(all(isinstance(v, str) and v for v in rule.values()))
                self.assertIn(rule["effect"], {"allow", "ask", "deny"})

    def test_inventory_and_defaults(self):
        self.assertEqual(set(self.agents), PRIMARIES | LEAVES)
        self.assertFalse(RETIRED & set(self.config.get("agents", {})))
        self.assertEqual(self.config.get("default_agent"), "direct")
        self.assertEqual(self.agents["direct"]["mode"], "all")
        self.assertEqual(self.agents["direct"]["model"], "openai/gpt-6.1-sol#xhigh")
        self.assertEqual(self.agents["autopilot"]["mode"], "primary")
        self.assertEqual(self.agents["coder"]["model"], "openai/gpt-6.1-sol#high")
        self.assertEqual(self.agents["cloudflare"]["model"], "openai/gpt-6.1-sol#high")
        self.assertEqual(self.agents["cloudflare"]["mode"], "all")

    def test_flat_routes_and_depth(self):
        self.assertTrue(
            "subagent_depth" not in self.config, "Unsupported top-level depth"
        )
        self.assertEqual(self.config.get("experimental", {}).get("subagent_depth"), 1)
        for name, data in self.agents.items():
            routes = [r for r in data["permissions"] if r["action"] == "subagent"]
            with self.subTest(agent=name):
                if name in LEAVES:
                    self.assertEqual(
                        routes,
                        [{"action": "subagent", "resource": "*", "effect": "deny"}],
                    )
                for r in routes:
                    if r["effect"] != "deny":
                        self.assertIn(r["resource"], LEAVES)
                        if r["resource"] in ADAPTERS:
                            self.assertEqual(
                                (name, r["resource"]), ("direct", "claude")
                            )
                        self.assertIn(
                            self.agents[r["resource"]]["mode"], {"all", "subagent"}
                        )
        for name, data in self.config.get("agents", {}).items():
            for r in data.get("permissions", []):
                if r["action"] == "subagent" and r["effect"] != "deny":
                    self.assertIn(name, PRIMARIES)
                    self.assertIn(r["resource"], LEAVES - ADAPTERS)
        expected = {
            "coder",
            "review",
            "adversarial",
            "operations",
            "utility",
            "config",
            "github",
            "cloudflare",
        }
        for name in ("direct", "autopilot"):
            self.assertEqual(
                {
                    r["resource"]
                    for r in self.agents[name]["permissions"]
                    if r["action"] == "subagent" and r["effect"] == "allow"
                },
                expected | ({"claude"} if name == "direct" else set()),
            )

    def test_boundaries(self):
        for name, data in self.agents.items():
            self.assertEqual(
                data["permissions"][0],
                {"action": "*", "resource": "*", "effect": "deny"},
                name,
            )
        for name in ("review", "adversarial"):
            for command in ("uv run pytest", "pnpm test"):
                self.expect(name, "shell", command, "allow")
            self.expect(name, "shell", "npm test", "deny")
        self.expect("github", "github_create_pull_request", "*", "allow")
        self.expect("cloudflare", "cloudflare-api_request", "*", "allow")
        for name in ("coder", "utility", "operations"):
            for command in ("git commit -m synthetic", "git push origin"):
                self.expect(name, "shell", command, "deny")
        self.expect("gated-direct", "shell", "uv run pytest", "ask")
        self.expect(
            "gated-direct", "external_directory", "/synthetic/reference/*", "ask"
        )
        self.expect("contained-code-local", "webfetch", "https://example.com", "deny")
        for name in ("contained-net-research", "contained-text-only"):
            for action in ("read", "edit", "shell"):
                self.expect(name, action, "synthetic", "deny")
        for name in self.agents:
            self.expect(
                name,
                "skill",
                "customize-opencode",
                "allow" if name == "config" else "deny",
            )

    def test_environment_file_policies(self):
        policies = self.config.get("experimental", {}).get("policies", [])
        # Pinned policy hook selects the last tool.use match; allow lifts a deny.
        # These are synthetic resources, never files read or commands executed.
        blocked = (
            "read:.env",
            "read:/synthetic/.env",
            "read:/synthetic/config.env",
            "read:/synthetic/.env.example",
            "read:/synthetic/.env.backup",
            "read:/synthetic/.env.local.bak",
            "shell:cat /synthetic/.env",
            "shell:cat /synthetic/.env.example",
            "shell:printf .env.backup",
            "shell:cat .env",
            'shell:cat ".env"',
            "shell:cat '.env'",
            "shell:cat config.env",
            "shell:cat config.env other.txt",
            'shell:cat "config.env"',
            "shell:cat 'config.env'",
            "shell:printf `cat config.env`",
        )
        ordinary = (
            "shell:python3 -c 'import os; assert os.environ is not None'",
            "shell:python3 -c 'import os; assert list(os.environ)'",
        )
        for resources, expected in ((blocked, "deny"), (ordinary, "allow")):
            for resource in resources:
                with self.subTest(resource=resource):
                    selected = next(
                        (
                            p
                            for p in reversed(policies)
                            if p["action"] == "tool.use"
                            and matches(resource, p["resource"])
                        ),
                        {},
                    )
                    self.assertEqual(selected.get("effect", "allow"), expected)

    def test_model_independence_and_adapter_isolation(self):
        for name, data in self.config.get("agents", {}).items():
            if name in self.agents:
                self.assertNotIn("anthropic", str(data.get("model", "")).lower())
                self.assertFalse(data.get("disabled", False), "Managed role disabled")
                if name not in ADAPTERS:
                    self.assertFalse(
                        any(
                            r["effect"] == "allow"
                            and "switchboard" in r["action"].lower()
                            for r in data.get("permissions", [])
                        )
                    )
                if name in LEAVES:
                    for rule in data.get("permissions", []):
                        self.assertFalse(
                            rule["action"] == "*" and rule["effect"] != "deny"
                        )
                        self.assertFalse(
                            rule["action"] == "subagent" and rule["effect"] != "deny"
                        )
                if name in {"review", "adversarial", "operations"}:
                    self.assertFalse(
                        any(
                            r["action"] == "edit" and r["effect"] != "deny"
                            for r in data.get("permissions", [])
                        )
                    )
        for name, data in self.agents.items():
            with self.subTest(agent=name):
                self.assertNotIn("anthropic", str(data.get("model", "")).lower())
                if name not in ADAPTERS:
                    self.assertNotRegex(
                        self.bodies[name].lower(),
                        r"anthropic|switchboard|externalmodel|externaleffort",
                    )
                    if name != "direct":
                        self.assertNotRegex(self.bodies[name].lower(), r"claude")
                    self.assertFalse(
                        any(
                            r["effect"] == "allow"
                            and "switchboard" in r["action"].lower()
                            for r in data["permissions"]
                        )
                    )
        for name in ADAPTERS:
            self.assertTrue(has_rule(self.agents[name], "execute", "*", "allow"))
            self.assertFalse(has_rule(self.agents[name], "shell", "*", "allow"))
        self.assertTrue(has_rule(self.agents["direct"], "execute", "*", "allow"))
        for name in self.agents.keys() - ADAPTERS - {"direct"}:
            self.assertFalse(has_rule(self.agents[name], "execute", "*", "allow"), name)

    def test_removed_references(self):
        for command in self.config.get("commands", {}).values():
            if "agent" in command:
                self.assertIn(command["agent"], self.agents)
        for name, body in self.bodies.items():
            self.assertNotRegex(
                body,
                r"`(?:code|orchestrator|ops-fast|ops-context|qwen-task|yolo)`",
                name,
            )
        for name in self.agents:
            self.assertNotIn(name, RETIRED)
        for path in sorted(AGENTS.rglob("*.md")):
            for line in read_safe(path).splitlines():
                if PREVIOUS_CLOUDFLARE in line:
                    self.assertEqual(path.relative_to(AGENTS).as_posix(), "README.md")
                    self.assertTrue(
                        line.startswith(f"| {PREVIOUS_CLOUDFLARE} | cloudflare |"),
                        "Previous specialist ID permitted only in migration mapping",
                    )
        for path in sorted(AGENTS.rglob("*.json")):
            self.assertTrue(
                PREVIOUS_CLOUDFLARE not in read_safe(path),
                "Stale specialist ID in current configuration",
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", type=Path, default=ROOT / "tests/fixtures/config.json"
    )
    parser.add_argument("--agents", type=Path, default=ROOT)
    args = parser.parse_args()
    CONFIG, AGENTS = args.config.expanduser(), args.agents.expanduser()
    unittest.main(argv=[__file__], verbosity=2)
