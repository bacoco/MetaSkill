#!/bin/bash
# Run all EvolveSkill tests

set -e

echo "🧪 Running EvolveSkill Tests..."
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name=$1
    local test_cmd=$2

    echo -n "  Testing $test_name... "
    if eval $test_cmd > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗${NC}"
        ((TESTS_FAILED++))
    fi
}

# Test Cortex API
echo "📦 Testing Cortex..."
run_test "cortex_api imports" "python3 -c 'from tests.test_cortex_api import *'"
run_test "event limit enforcement" "python3 -c 'from tests.test_cortex_api import test_event_limit_enforced; test_event_limit_enforced()'"
run_test "JSON validity" "python3 -c 'from tests.test_cortex_api import test_status_file_is_valid_json_after_writes; test_status_file_is_valid_json_after_writes()'"

# Test Synapse modules
echo ""
echo "🧠 Testing Synapse..."
run_test "synapse imports" "python3 -c 'from tests.test_synapse import *'"
run_test "pattern detection" "python3 -c 'from tests.test_synapse import test_pattern_detection; test_pattern_detection()'"
run_test "config validation" "python3 -c 'from tests.test_synapse import test_config_validation; test_config_validation()'"

# Test Forge validation
echo ""
echo "🔨 Testing Forge..."
run_test "skill validation" "python3 -c 'from tests.test_forge import test_skill_validation; test_skill_validation()'"
run_test "frontmatter parsing" "python3 -c 'from tests.test_forge import test_frontmatter_parsing; test_frontmatter_parsing()'"

# Test shell scripts
echo ""
echo "🐚 Testing Shell Scripts..."
run_test "install.sh syntax" "bash -n .claude/skills/cortex/scripts/install.sh"
run_test "package script syntax" "bash -n ./package_evolveskill.sh"

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test Results:"
echo -e "  Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "  Failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Some tests failed${NC}"
    exit 1
fi