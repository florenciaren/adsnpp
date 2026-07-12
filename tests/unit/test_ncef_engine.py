import pytest

from adsnpp.circular.ncef_engine import NCEFScoringEngine

TECHNOLOGIES = {
    "BWRX-300": {
        "uranium_utilization_efficiency": 0.79,
        "outlet_temp_celsius": 285,
        "hlw_volume_norm": 0.30,
        "hydrogen_production_readiness": 0.20,
        "grid_expansion_potential": 0.85,
        "thermal_efficiency": 0.34,
        "local_content_fraction": 0.45,
        "digital_twin_maturity": 0.82,
        "coolant_recycle_fraction": 0.92,
    },
    "HTR-PM": {
        "uranium_utilization_efficiency": 0.82,
        "outlet_temp_celsius": 750,
        "hlw_volume_norm": 0.25,
        "hydrogen_production_readiness": 0.78,
        "grid_expansion_potential": 0.72,
        "thermal_efficiency": 0.42,
        "local_content_fraction": 0.35,
        "digital_twin_maturity": 0.71,
        "coolant_recycle_fraction": 0.88,
    },
}


def test_compare_technologies_returns_sorted_results():
    engine = NCEFScoringEngine()
    results = engine.compare_technologies(TECHNOLOGIES)

    assert {r.technology for r in results} == set(TECHNOLOGIES)
    assert len(results) == 2
    assert results[0].adjusted_cei >= results[1].adjusted_cei
    for r in results:
        assert 0.0 <= r.adjusted_cei <= 1.0


def test_weights_must_sum_to_one():
    with pytest.raises(ValueError):
        NCEFScoringEngine(weights={"resource_efficiency": 0.5})


def test_higher_outlet_temp_increases_energy_versatility():
    engine = NCEFScoringEngine()
    low_temp = engine.score_technology("low", {**TECHNOLOGIES["BWRX-300"], "outlet_temp_celsius": 250})
    high_temp = engine.score_technology("high", {**TECHNOLOGIES["BWRX-300"], "outlet_temp_celsius": 900})

    assert high_temp.energy_versatility > low_temp.energy_versatility
