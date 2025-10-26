# Makefile for EvolveSkill convenience commands

# Defaults (override with: make analyze THRESHOLD=5 DAYS=14)
THRESHOLD ?= 5
DAYS ?= 7
OUTPUT ?= Synapse_RECOMMENDATIONS.md

.PHONY: help install analyze auto-generate trace package dist-clean test

help:
	@echo "Targets:"
	@echo "  make install        - Install Cortex git hooks in this repo"
	@echo "  make trace          - Force a Cortex trace now"
	@echo "  make analyze        - Run Synapse analyzer (DAYS=$(DAYS), THRESHOLD=$(THRESHOLD))"
	@echo "  make auto-generate  - Run Synapse auto-skill generator"
	@echo "  make package        - Build EvolveSkill distribution zip"
	@echo "  make test           - Run all unit tests"
	@echo "  make dist-clean     - Clean dist artifacts"

install:
	@bash .claude/skills/cortex/scripts/install.sh

trace:
	@python3 .claude/skills/cortex/scripts/trace_session.py --repo . --verbose

analyze:
	@python3 .claude/skills/synapse/scripts/synapse_analyzer.py --repo . --threshold $(THRESHOLD) --days $(DAYS) --output $(OUTPUT)
	@echo "\nRecommendations written to $(OUTPUT)"

auto-generate:
	@python3 .claude/skills/synapse/scripts/auto_skill_generator.py --threshold $(THRESHOLD) --days $(DAYS)

package:
	@bash ./package_evolveskill.sh 2.2.0

test:
	@bash ./scripts/run_tests.sh

dist-clean:
	@rm -rf dist || true
