"""Nuclear Circular Economy Framework (N-CEF v2) scoring engine.

Computes a 5-dimension Circular Economy Index (CEI) per reactor technology,
aligned with ISO 14040 life-cycle-assessment principles: resource
efficiency, waste minimization, energy versatility, local value creation,
and digital circularity.
"""

from __future__ import annotations

from dataclasses import dataclass

#: Plausible reactor outlet-temperature range (°C), used to normalize
#: `outlet_temp_celsius` onto a 0-1 scale for the energy-versatility
#: dimension (higher process-heat temperature -> more end-use flexibility).
_OUTLET_TEMP_RANGE = (250.0, 950.0)

#: Equal-weighted default; override via NCEFScoringEngine(weights=...).
_DEFAULT_DIMENSION_WEIGHTS = {
    "resource_efficiency": 0.2,
    "waste_minimization": 0.2,
    "energy_versatility": 0.2,
    "local_value_creation": 0.2,
    "digital_circularity": 0.2,
}


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _normalize_outlet_temp(celsius: float) -> float:
    low, high = _OUTLET_TEMP_RANGE
    return _clip01((celsius - low) / (high - low))


@dataclass(frozen=True)
class NCEFResult:
    """Per-technology N-CEF scoring result."""

    technology: str
    resource_efficiency: float
    waste_minimization: float
    energy_versatility: float
    local_value_creation: float
    digital_circularity: float
    adjusted_cei: float


class NCEFScoringEngine:
    """Scores reactor technologies against the 5 N-CEF v2 dimensions.

    Expected indicator keys per technology (all in [0, 1] except
    ``outlet_temp_celsius``, given in degrees Celsius):

    - ``uranium_utilization_efficiency``, ``thermal_efficiency``
      (-> resource efficiency)
    - ``hlw_volume_norm`` (lower is better), ``coolant_recycle_fraction``
      (-> waste minimization)
    - ``hydrogen_production_readiness``, ``grid_expansion_potential``,
      ``outlet_temp_celsius`` (-> energy versatility)
    - ``local_content_fraction`` (-> local value creation)
    - ``digital_twin_maturity`` (-> digital circularity)
    """

    def __init__(self, weights: dict[str, float] | None = None):
        self.weights = weights or dict(_DEFAULT_DIMENSION_WEIGHTS)
        total = sum(self.weights.values())
        if not (0.999 <= total <= 1.001):
            raise ValueError(f"dimension weights must sum to 1.0, got {total}")

    def score_technology(self, technology: str, indicators: dict[str, float]) -> NCEFResult:
        resource_efficiency = (
            indicators["uranium_utilization_efficiency"] + indicators["thermal_efficiency"]
        ) / 2

        waste_minimization = (
            (1 - indicators["hlw_volume_norm"]) + indicators["coolant_recycle_fraction"]
        ) / 2

        energy_versatility = (
            indicators["hydrogen_production_readiness"]
            + indicators["grid_expansion_potential"]
            + _normalize_outlet_temp(indicators["outlet_temp_celsius"])
        ) / 3

        local_value_creation = indicators["local_content_fraction"]
        digital_circularity = indicators["digital_twin_maturity"]

        adjusted_cei = (
            self.weights["resource_efficiency"] * resource_efficiency
            + self.weights["waste_minimization"] * waste_minimization
            + self.weights["energy_versatility"] * energy_versatility
            + self.weights["local_value_creation"] * local_value_creation
            + self.weights["digital_circularity"] * digital_circularity
        )

        return NCEFResult(
            technology=technology,
            resource_efficiency=resource_efficiency,
            waste_minimization=waste_minimization,
            energy_versatility=energy_versatility,
            local_value_creation=local_value_creation,
            digital_circularity=digital_circularity,
            adjusted_cei=adjusted_cei,
        )

    def compare_technologies(
        self, technologies: dict[str, dict[str, float]]
    ) -> list[NCEFResult]:
        """Score each technology and return results sorted by adjusted_cei desc."""
        results = [self.score_technology(name, ind) for name, ind in technologies.items()]
        return sorted(results, key=lambda r: r.adjusted_cei, reverse=True)
