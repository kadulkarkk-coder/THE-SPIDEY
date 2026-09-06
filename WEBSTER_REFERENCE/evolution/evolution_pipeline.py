"""Controlled pipeline that turns validated improvements into plugin registrations."""
from __future__ import annotations

from dataclasses import dataclass

from ..plugins.plugin_manager import PluginManager
from ..plugins.plugin_types import PluginSpec
from .evolution_benchmark import EvolutionBenchmark, BenchmarkResult
from .evolution_candidate import EvolutionCandidate
from .evolution_lineage import EvolutionLineage, EvolutionRecord
from .evolution_validator import EvolutionValidator, ValidationReport
from .plugin_manifest import EvolutionPluginManifest
from .plugin_sandbox import PluginSandbox, SandboxResult


@dataclass(frozen=True)
class EvolutionDecision:
    accepted: bool
    validation: ValidationReport
    sandbox: SandboxResult | None = None
    benchmark: BenchmarkResult | None = None
    reason: str = ""


class EvolutionPipeline:
    """Validate, sandbox, benchmark, then register an evolved plugin.

    Nothing is installed unless every gate passes. The core application is
    never rewritten by this pipeline.
    """

    def __init__(self, plugin_manager: PluginManager | None = None) -> None:
        self.plugins = plugin_manager or PluginManager()
        self.validator = EvolutionValidator()
        self.sandbox = PluginSandbox()
        self.benchmark = EvolutionBenchmark()
        self.lineage = EvolutionLineage()

    def propose(self, candidate: EvolutionCandidate, manifest: EvolutionPluginManifest,
                *, check, baseline: float, candidate_score: float) -> EvolutionDecision:
        validation = self.validator.validate(manifest)
        if not validation.valid:
            return EvolutionDecision(False, validation, reason="validation failed")
        sandbox = self.sandbox.run(check)
        if not sandbox.passed:
            return EvolutionDecision(False, validation, sandbox=sandbox, reason="sandbox failed")
        benchmark = self.benchmark.compare(baseline, candidate_score)
        if not benchmark.accepted:
            return EvolutionDecision(False, validation, sandbox, benchmark, "benchmark gate failed")
        spec = PluginSpec(
            plugin_id=candidate.plugin_id,
            name=candidate.plugin_id,
            description=candidate.problem,
            capabilities=tuple(candidate.permissions),
            builtin=False,
            metadata={"evolution_id": candidate.evolution_id, "version": candidate.version},
        )
        self.plugins.register(spec, enabled=False)
        self.lineage.record(EvolutionRecord(candidate.evolution_id, candidate.plugin_id,
                                             candidate.version, candidate.parent_version, "validated",
                                             manifest.rollback_version))
        return EvolutionDecision(True, validation, sandbox, benchmark, "candidate registered for explicit activation")
