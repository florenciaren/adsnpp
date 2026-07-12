"""AHP/TOPSIS multi-criteria decision engine for reactor technology selection.

Implements Analytic Hierarchy Process (AHP) pairwise-comparison weighting
combined with Technique for Order of Preference by Similarity to Ideal
Solution (TOPSIS) ranking, per IAEA NG-G-3.1 / INPRO methodology.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class RankedAlternative:
    """A single technology's TOPSIS ranking result."""

    technology: str
    closeness: float
    rank: int


class DecisionEngine:
    """AHP-weighted TOPSIS engine over an arbitrary set of indicators.

    Parameters
    ----------
    criteria:
        Indicator names, in the same column order used in ``scores`` and
        ``pairwise_comparison``.
    benefit_criteria:
        Subset of ``criteria`` where a higher raw value is better. Any
        criterion not listed is treated as a cost criterion (lower is
        better).
    """

    def __init__(self, criteria: list[str], benefit_criteria: set[str] | None = None):
        if not criteria:
            raise ValueError("criteria must be a non-empty list")
        self.criteria = list(criteria)
        self.benefit_criteria = benefit_criteria or set(criteria)

    def weights_from_pairwise(self, pairwise_comparison: np.ndarray) -> np.ndarray:
        """Derive AHP weights from an n×n pairwise comparison matrix.

        Uses the normalized principal eigenvector method.
        """
        matrix = np.asarray(pairwise_comparison, dtype=float)
        n = len(self.criteria)
        if matrix.shape != (n, n):
            raise ValueError(f"pairwise_comparison must be {n}x{n}")

        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        principal = np.argmax(eigenvalues.real)
        weights = np.abs(eigenvectors[:, principal].real)
        return weights / weights.sum()

    def rank(
        self, scores: dict[str, dict[str, float]], weights: np.ndarray | None = None
    ) -> list[RankedAlternative]:
        """Rank technologies with TOPSIS.

        Parameters
        ----------
        scores:
            ``{technology_name: {criterion: raw_value}}``.
        weights:
            Per-criterion weights (sums to 1). Defaults to equal weights.
        """
        technologies = list(scores.keys())
        matrix = np.array(
            [[scores[t][c] for c in self.criteria] for t in technologies], dtype=float
        )

        if weights is None:
            weights = np.full(len(self.criteria), 1.0 / len(self.criteria))
        weights = np.asarray(weights, dtype=float)

        norm = matrix / np.linalg.norm(matrix, axis=0)
        weighted = norm * weights

        ideal_best = np.array(
            [
                weighted[:, i].max() if c in self.benefit_criteria else weighted[:, i].min()
                for i, c in enumerate(self.criteria)
            ]
        )
        ideal_worst = np.array(
            [
                weighted[:, i].min() if c in self.benefit_criteria else weighted[:, i].max()
                for i, c in enumerate(self.criteria)
            ]
        )

        dist_best = np.linalg.norm(weighted - ideal_best, axis=1)
        dist_worst = np.linalg.norm(weighted - ideal_worst, axis=1)
        closeness = dist_worst / (dist_best + dist_worst)

        order = np.argsort(-closeness)
        return [
            RankedAlternative(technology=technologies[i], closeness=float(closeness[i]), rank=rank)
            for rank, i in enumerate(order, start=1)
        ]
