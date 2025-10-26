"""
Test suite for Forge skill creation tools
"""

import tempfile
from pathlib import Path
import importlib.util


def load_forge_module(module_name):
    """Load Forge module"""
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / f".claude/skills/forge/scripts/{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, str(module_path))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore
    return module


def test_skill_validation():
    """Test skill validation functionality"""
    try:
        validate = load_forge_module("quick_validate")

        # Test with valid skill
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_path = Path(tmpdir)
            skill_md = skill_path / "SKILL.md"

            # Create valid skill
            skill_md.write_text("""---
name: test-skill
description: This is a test skill for validation
---

# Test Skill

This is the skill content.
""")

            valid, message = validate.validate_skill(skill_path)
            assert valid == True
            assert "valid" in message.lower()

    except Exception as e:
        raise AssertionError(f"Skill validation test failed: {e}")


def test_frontmatter_parsing():
    """Test YAML frontmatter parsing"""
    try:
        validate = load_forge_module("quick_validate")

        with tempfile.TemporaryDirectory() as tmpdir:
            skill_path = Path(tmpdir)
            skill_md = skill_path / "SKILL.md"

            # Test missing frontmatter
            skill_md.write_text("# No Frontmatter")
            valid, message = validate.validate_skill(skill_path)
            assert valid == False
            assert "frontmatter" in message.lower()

            # Test invalid YAML
            skill_md.write_text("""---
name: [invalid yaml
description: test
---
""")
            valid, message = validate.validate_skill(skill_path)
            assert valid == False
            assert "yaml" in message.lower()

            # Test missing required fields
            skill_md.write_text("""---
name: test-skill
---
""")
            valid, message = validate.validate_skill(skill_path)
            assert valid == False
            assert "description" in message.lower()

            # Test invalid name format
            skill_md.write_text("""---
name: Test_Skill_123
description: Invalid name format
---
""")
            valid, message = validate.validate_skill(skill_path)
            assert valid == False
            assert "hyphen-case" in message.lower()

            # Test name too long
            skill_md.write_text(f"""---
name: {"a" * 65}
description: Name too long
---
""")
            valid, message = validate.validate_skill(skill_path)
            assert valid == False
            assert "too long" in message.lower()

            # Test description with angle brackets
            skill_md.write_text("""---
name: test-skill
description: This has <brackets> in it
---
""")
            valid, message = validate.validate_skill(skill_path)
            assert valid == False
            assert "angle brackets" in message.lower()

    except Exception as e:
        raise AssertionError(f"Frontmatter parsing test failed: {e}")


def test_skill_initialization():
    """Test skill initialization"""
    try:
        init_skill = load_forge_module("init_skill")

        with tempfile.TemporaryDirectory() as tmpdir:
            skill_name = "test-new-skill"
            skill_path = Path(tmpdir) / skill_name

            # Initialize skill
            init_skill.init_skill(skill_name, tmpdir)

            # Check created files
            assert skill_path.exists()
            assert (skill_path / "SKILL.md").exists()
            assert (skill_path / "scripts").exists()
            assert (skill_path / "references").exists()
            assert (skill_path / "assets").exists()

            # Check SKILL.md contains skill name
            content = (skill_path / "SKILL.md").read_text()
            assert skill_name in content
            assert "name: " + skill_name in content

    except Exception as e:
        raise AssertionError(f"Skill initialization test failed: {e}")


def test_package_skill():
    """Test skill packaging functionality"""
    try:
        package = load_forge_module("package_skill")
        init_skill = load_forge_module("init_skill")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test skill
            skill_name = "package-test-skill"
            skill_path = Path(tmpdir) / skill_name
            init_skill.init_skill(skill_name, tmpdir)

            # Package it
            output_dir = Path(tmpdir) / "output"
            output_dir.mkdir()

            package_path = package.package_skill(str(skill_path), str(output_dir))

            # Check package was created
            assert Path(package_path).exists()
            assert package_path.endswith(".zip")

    except Exception as e:
        raise AssertionError(f"Skill packaging test failed: {e}")


def test_validation_edge_cases():
    """Test validation with edge cases"""
    try:
        validate = load_forge_module("quick_validate")

        with tempfile.TemporaryDirectory() as tmpdir:
            skill_path = Path(tmpdir)
            skill_md = skill_path / "SKILL.md"

            # Test with unexpected YAML keys
            skill_md.write_text("""---
name: test-skill
description: Valid description
unexpected_key: should trigger warning
---
# Content
""")
            valid, message = validate.validate_skill(skill_path)
            assert valid == False
            assert "unexpected" in message.lower()

            # Test with very long description
            long_desc = "x" * 1025  # Over 1024 limit
            skill_md.write_text(f"""---
name: test-skill
description: {long_desc}
---
""")
            valid, message = validate.validate_skill(skill_path)
            assert valid == False
            assert "too long" in message.lower()

    except Exception as e:
        raise AssertionError(f"Edge case validation test failed: {e}")


# Export all test functions
__all__ = [
    "test_skill_validation",
    "test_frontmatter_parsing",
    "test_skill_initialization",
    "test_package_skill",
    "test_validation_edge_cases"
]