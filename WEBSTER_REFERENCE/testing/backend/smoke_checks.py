"""Cross-module smoke checks that stay offline and dependency-free."""
from __future__ import annotations

from .integration_suite import IntegrationSuite, IntegrationReport


def build_core_smoke_suite() -> IntegrationSuite:
    """Build checks for the testing layer's core contracts."""
    suite = IntegrationSuite("core-smoke")

    def result_contract() -> None:
        from .test_result import TestResult, TestSummary

        result = TestResult("contract", True, "ok")
        assert result.passed is True
        summary = TestSummary(1, 1, 0)
        assert summary.success_rate == 1.0

    def runner_contract() -> None:
        from .test_runner import TestRunner

        results, summary = TestRunner().run((("pass", lambda: None), ("fail", lambda: (_ for _ in ()).throw(ValueError("expected")))))
        assert summary.total == 2
        assert summary.passed == 1
        assert summary.failed == 1
        assert results[0].passed is True
        assert results[1].passed is False

    def suite_contract() -> None:
        from .integration_suite import IntegrationSuite

        report = IntegrationSuite("nested").add("ok", lambda: None).run()
        assert report.suite == "nested"
        assert report.summary.success_rate == 1.0

    suite.add("result-contract", result_contract)
    suite.add("runner-contract", runner_contract)
    suite.add("suite-contract", suite_contract)
    return suite


def run_core_smoke_checks() -> IntegrationReport:
    """Run the standard offline smoke suite."""
    return build_core_smoke_suite().run()
