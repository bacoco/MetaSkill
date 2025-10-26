#!/usr/bin/env python3
"""
MCP Test Script - Validate MCP tool integration

Usage:
    python3 test_mcp.py --skill-path .claude/skills/my-skill --tool-name "db-tools"
    python3 test_mcp.py --skill-path .claude/skills/my-skill --tool-name "api-tools" --verbose
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List


class MCPTester:
    """Test MCP tool integration"""

    def __init__(self, skill_path: Path, tool_name: str, verbose: bool = False):
        self.skill_path = Path(skill_path)
        self.tool_name = tool_name
        self.verbose = verbose
        self.mcp_dir = self.skill_path / "mcp_tools" / tool_name
        self.results: List[Dict[str, Any]] = []

    def run_all_tests(self) -> bool:
        """Run all tests and return success status"""
        print(f"🧪 Testing MCP tool integration...")
        print(f"   Skill: {self.skill_path.name}")
        print(f"   Tool: {self.tool_name}")
        print()

        tests = [
            ("Directory structure", self.test_directory_structure),
            ("Manifest file", self.test_manifest),
            ("Environment file", self.test_environment_file),
            ("Docker configuration", self.test_docker_config),
            ("Security settings", self.test_security_settings),
        ]

        all_passed = True

        for test_name, test_func in tests:
            try:
                result = test_func()
                status = "✅ PASS" if result["passed"] else "❌ FAIL"
                print(f"{status} {test_name}")

                if self.verbose and result.get("details"):
                    print(f"     {result['details']}")

                self.results.append({
                    "test": test_name,
                    **result
                })

                if not result["passed"]:
                    all_passed = False

            except Exception as e:
                print(f"❌ FAIL {test_name} - {e}")
                all_passed = False

        print()
        return all_passed

    def test_directory_structure(self) -> Dict[str, Any]:
        """Test that MCP tool directory exists and is structured correctly"""
        if not self.mcp_dir.exists():
            return {
                "passed": False,
                "details": f"MCP directory not found: {self.mcp_dir}"
            }

        required_files = ["manifest.json", "README.md"]
        missing = [f for f in required_files if not (self.mcp_dir / f).exists()]

        if missing:
            return {
                "passed": False,
                "details": f"Missing files: {', '.join(missing)}"
            }

        return {
            "passed": True,
            "details": f"All required files present in {self.mcp_dir.name}/"
        }

    def test_manifest(self) -> Dict[str, Any]:
        """Test manifest file validity"""
        manifest_path = self.mcp_dir / "manifest.json"

        if not manifest_path.exists():
            return {"passed": False, "details": "manifest.json not found"}

        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)

            required_fields = ["mcp_id", "tool_name", "transport"]
            missing = [f for f in required_fields if f not in manifest]

            if missing:
                return {
                    "passed": False,
                    "details": f"Missing fields: {', '.join(missing)}"
                }

            return {
                "passed": True,
                "details": f"Valid manifest for MCP ID: {manifest['mcp_id']}"
            }

        except json.JSONDecodeError as e:
            return {"passed": False, "details": f"Invalid JSON: {e}"}

    def test_environment_file(self) -> Dict[str, Any]:
        """Test environment file existence"""
        env_example = self.mcp_dir / ".env.example"

        if not env_example.exists():
            return {
                "passed": False,
                "details": ".env.example not found"
            }

        return {
            "passed": True,
            "details": "Environment template exists"
        }

    def test_docker_config(self) -> Dict[str, Any]:
        """Test Docker configuration if present"""
        docker_config = self.mcp_dir / "docker_config.json"

        if not docker_config.exists():
            return {
                "passed": True,
                "details": "No Docker config (optional)"
            }

        try:
            with open(docker_config, 'r') as f:
                config = json.load(f)

            if "image" not in config:
                return {
                    "passed": False,
                    "details": "Missing 'image' in Docker config"
                }

            return {
                "passed": True,
                "details": f"Docker image: {config['image']}"
            }

        except json.JSONDecodeError as e:
            return {"passed": False, "details": f"Invalid Docker config: {e}"}

    def test_security_settings(self) -> Dict[str, Any]:
        """Test security configuration"""
        manifest_path = self.mcp_dir / "manifest.json"

        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)

            security = manifest.get("security", {})

            if not security:
                return {
                    "passed": False,
                    "details": "No security settings found"
                }

            # Check for strict sandbox
            sandbox = security.get("sandbox")
            if sandbox != "strict":
                return {
                    "passed": False,
                    "details": f"Sandbox not strict: {sandbox}"
                }

            return {
                "passed": True,
                "details": "Security settings valid (strict sandbox)"
            }

        except Exception as e:
            return {"passed": False, "details": f"Error reading security: {e}"}

    def generate_report(self) -> Dict[str, Any]:
        """Generate test report"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])

        return {
            "skill_path": str(self.skill_path),
            "tool_name": self.tool_name,
            "tests_run": total,
            "tests_passed": passed,
            "tests_failed": total - passed,
            "success_rate": (passed / total * 100) if total > 0 else 0,
            "results": self.results
        }


def main():
    parser = argparse.ArgumentParser(
        description="Test MCP tool integration in a Claude Code skill"
    )
    parser.add_argument(
        "--skill-path",
        required=True,
        help="Path to the skill directory"
    )
    parser.add_argument(
        "--tool-name",
        required=True,
        help="Name of the MCP tool to test"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed test output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    tester = MCPTester(
        skill_path=args.skill_path,
        tool_name=args.tool_name,
        verbose=args.verbose
    )

    all_passed = tester.run_all_tests()

    if args.json:
        report = tester.generate_report()
        print(json.dumps(report, indent=2))
    else:
        report = tester.generate_report()
        print(f"📊 Test Summary:")
        print(f"   Tests run: {report['tests_run']}")
        print(f"   Passed: {report['tests_passed']}")
        print(f"   Failed: {report['tests_failed']}")
        print(f"   Success rate: {report['success_rate']:.1f}%")
        print()

        if all_passed:
            print("✅ All tests passed! MCP tool is correctly integrated.")
        else:
            print("❌ Some tests failed. Check the output above for details.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
