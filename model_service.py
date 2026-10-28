"""Frozen-model predictions and the notebook's recommendation procedure."""
from pathlib import Path
from types import FunctionType
import copy

import joblib
import numpy as np

import model_components as components


class SalaryModel:
    def __init__(self, bundle):
        self.pipeline = bundle["pipeline"]
        self.metadata = bundle["metadata"]
        # Give the unchanged notebook function its fitted objects and column lists.
        # Each service has its own namespace, with no global mutation or refitting.
        namespace = dict(vars(components))
        namespace.update({
            "q3_required_raw_columns": self.metadata["required_columns"],
            "numeric_columns": self.metadata["numeric_columns"],
            "q2_selected_engineered": self.metadata["engineered_features"],
            "q4_final_pipeline": self.pipeline,
            "salary_order": self.metadata["salary_order"],
        })
        original = components.predict_respondent_probabilities
        self._predict = FunctionType(original.__code__, namespace, original.__name__)

    @classmethod
    def load(cls, path=None):
        path = path or Path(__file__).parent / "artifacts" / "model.joblib"
        return cls(joblib.load(path))

    def predict(self, answers):
        return self._predict(answers).to_numpy()

    @staticmethod
    def score(probabilities):
        return float(np.asarray(probabilities) @ np.arange(15))

    def existing_skills(self, answers):
        result = set()
        for group in components.q5_5_skill_groups:
            result.update(components.q5_5_recorded_options(answers[group]))
        return result

    def add_skills(self, answers, skills):
        """Apply distinct additions together, counting each new tool once."""
        changed = copy.deepcopy(answers)
        existing = self.existing_skills(answers)
        for skill in dict.fromkeys(skills):
            if skill in existing:
                continue
            record = self.metadata["candidates"].get(skill)
            if record is None or record["support"] < self.metadata["minimum_support"]:
                raise ValueError("Choose a skill from the recommendations for this profile.")
            changed = components.q5_5_skill_profile(changed, skill, record["groups"])
            existing.add(skill)
        return changed

    def recommend(self, answers):
        """Evaluate each eligible addition from the same unchanged profile."""
        probabilities = self.predict(answers)
        current_score = self.score(probabilities)
        existing = self.existing_skills(answers)
        rows = []
        for skill, record in sorted(self.metadata["candidates"].items()):
            if skill in existing or record["support"] < self.metadata["minimum_support"]:
                continue
            changed = self.add_skills(answers, [skill])
            after = self.predict(changed)
            score = self.score(after)
            rows.append({
                "skill": skill,
                "group": ", ".join(components.q5_5_skill_groups[g] for g in record["groups"]),
                "support": record["support"],
                "score": score,
                "increase": score - current_score,
                "probabilities": after.tolist(),
            })
        positive = sorted((r for r in rows if r["increase"] > 0),
                          key=lambda r: (-r["increase"], r["skill"]))
        return {"probabilities": probabilities.tolist(), "score": current_score,
                "evaluated": len(rows), "positive": len(positive),
                "recommendations": positive[:3]}
