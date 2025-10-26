# Changelog

All notable changes to EvolveSkill will be documented in this file.

## [2.2.0] - 2025-10-26

### Added
- **MCP Provider Skill**: New skill for integrating Model Context Protocol tools
  - Discover MCP tools from approved catalogs
  - Attach MCP tools to skills with security sandboxing
  - Test MCP tool integration
  - Complete integration guide and documentation
  - Docker runtime support with strict security defaults
  - 3 standalone scripts: discover_mcp.py, attach_mcp.py, test_mcp.py

### Fixed
- **MCP Provider Structure**: Refactored to comply with Claude skill standards
  - Moved from `skills/` to `.claude/skills/mcp-provider/`
  - Removed Python package structure (__init__.py files)
  - Added proper YAML frontmatter to SKILL.md
  - Simplified from 18 files to 3 standalone scripts
  - Updated README.md with correct paths

## [2.1.0] - 2025-10-26

### Added
- **Test Suite**: Comprehensive unit tests for all modules (17+ tests)
  - Cortex API tests: event limits, JSON validity, filters, pattern analysis, session summary, atomic writes
  - Synapse tests: pattern detection, config validation, data models, cortex reader, report generation
  - Forge tests: skill validation, frontmatter parsing, initialization, packaging, edge cases
  - Shell script syntax validation
- **Complete Docstrings**: Professional documentation for all functions
  - Detailed Args, Returns, Raises sections
  - Usage examples and notes
  - Clear algorithm descriptions
- **Centralized Configuration**: New `config.py` module for shared settings
  - MAX_EVENTS configurable (default: 1000)
  - LOG_SIZE_MB configurable (default: 10MB)
  - PATTERN_THRESHOLD configurable (default: 5)
- **Makefile**: Convenient commands for development
  - `make install`: Install Cortex git hooks
  - `make trace`: Force Cortex trace
  - `make analyze`: Run Synapse analyzer
  - `make package`: Build distribution
  - `make test`: Run test suite
- **Test Runner**: New `scripts/run_tests.sh` for running all tests

### Improved
- **Memory Management**: Optimized for large files
  - Cortex now limits log parsing to 2MB by default
  - Streaming reads for large files
  - Configurable memory limits
- **Input Validation**: Enhanced error handling
  - Better timestamp parsing with proper exception handling
  - Type validation for SessionData objects
  - Robust YAML frontmatter validation
- **Atomic Writes**: Improved file write safety
  - All JSON writes now use temporary files + atomic replace
  - Cross-platform file locking support (optional)
- **Error Messages**: More descriptive error reporting
  - Debug logging for failed operations
  - Clear validation messages in Forge

### Fixed
- Fixed race condition potential in git hooks
- Fixed fragile imports in Synapse modules
- Fixed hardcoded event limits (now uses config)
- Removed duplicate code in pattern_detector_old.py

### Changed
- Updated all modules to use centralized configuration
- Improved code organization and modularity
- Enhanced documentation with implementation status

## [2.0.0] - 2025-10-25

### Added
- Initial release of unified EvolveSkill package
- Three core components: Cortex, Synapse, Forge
- Git hook integration for automatic tracking
- Pattern detection and skill recommendation
- Skill creation and validation tools

---

*Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)*