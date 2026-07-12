import numpy as np
import pytest

from adsnpp.core.decision_engine import DecisionEngine


def test_rank_orders_dominant_alternative_first():
    engine = DecisionEngine(criteria=["cost", "safety"], benefit_criteria={"safety"})
    scores = {
        "A": {"cost": 10, "safety": 0.9},
        "B": {"cost": 50, "safety": 0.3},
    }
    ranked = engine.rank(scores)

    assert ranked[0].technology == "A"
    assert ranked[0].rank == 1
    assert ranked[1].rank == 2
    assert ranked[0].closeness > ranked[1].closeness


def test_weights_from_pairwise_sum_to_one():
    engine = DecisionEngine(criteria=["a", "b", "c"])
    pairwise = np.array(
        [
            [1, 3, 5],
            [1 / 3, 1, 2],
            [1 / 5, 1 / 2, 1],
        ]
    )
    weights = engine.weights_from_pairwise(pairwise)

    assert weights.shape == (3,)
    assert weights == pytest.approx(weights, abs=0)
    assert weights.sum() == pytest.approx(1.0)
    assert all(w > 0 for w in weights)


def test_rejects_empty_criteria():
    with pytest.raises(ValueError):
        DecisionEngine(criteria=[])
