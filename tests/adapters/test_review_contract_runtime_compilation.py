"""Real-command review-contract compilation regressions across runtime wrappers."""

from __future__ import annotations

from dataclasses import asdict

import pytest

from gpd import registry
from gpd.core.review_contract_prompt import render_review_contract_prompt
from tests.adapters.review_contract_test_utils import (
    compile_review_contract_command_for_runtime,
    extract_review_contract_section,
)

REVIEW_COMMANDS = ("peer-review", "write-paper")
RUNTIMES = ("claude-code", "codex", "gemini", "opencode")


@pytest.mark.parametrize("command_name", REVIEW_COMMANDS)
def test_registry_rendered_review_contract_matches_the_canonical_dataclass_payload(command_name: str) -> None:
    command = registry.get_command(command_name)
    contract = command.review_contract

    assert contract is not None
    expected_section = render_review_contract_prompt(asdict(contract))

    assert extract_review_contract_section(command.content) == expected_section
    assert command.content.count("## Review Contract") == 1


@pytest.mark.parametrize("command_name", REVIEW_COMMANDS)
@pytest.mark.parametrize("runtime", RUNTIMES)
def test_real_review_command_sources_compile_across_runtime_wrappers_without_losing_review_contract(
    command_name: str,
    runtime: str,
) -> None:
    command = registry.get_command(command_name)
    contract = command.review_contract

    assert contract is not None
    expected_section = render_review_contract_prompt(asdict(contract))
    compiled = compile_review_contract_command_for_runtime(command_name, runtime)

    assert extract_review_contract_section(compiled) == expected_section
    assert compiled.count("## Review Contract") == 1
