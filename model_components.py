"""Model and prediction definitions copied directly from the verified assignment notebook.

The dashboard loads a fitted pipeline. It does not fit these classes during use.
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin
from sklearn.linear_model import LogisticRegression
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

q2_engineered_features = ["LanguageCount", "LogWorkExp", "PythonLogWorkExp"]


q5_5_skill_groups = {
    "LanguagesHaveWorkedWith": "Languages",
    "DatabasesHaveWorkedWith": "Databases",
    "CloudPlatHaveWorkedWith": "Cloud/development tools",
    "WebFrameworkHaveWorkedWith": "Web technologies",
    "KnowMgmtHaveWorkedWith": "Knowledge management"
}

q5_5_setting_options = {
    "LanguagesHaveWorkedWith": "I used a programming, scripting, or markup language for any reason",
    "DatabasesHaveWorkedWith": "I used a database for storage, querying, deployment",
    "CloudPlatHaveWorkedWith": "I used a cloud platform or any tools related to cloud technologies",
    "WebFrameworkHaveWorkedWith": "I built, maintained or learned about web technologies",
    "KnowMgmtHaveWorkedWith": "I used a knowledge management platform (such as a wiki)"
}

def split_survey_answers(answer):
    if pd.isna(answer) or not str(answer).strip():
        return ["__MISSING__"]
    # Split on the survey separator and count a repeated option only once.
    return sorted({option.strip() for option in str(answer).split(";") if option.strip()})

class ToolCountClipper(TransformerMixin, BaseEstimator):
    def __init__(self, quantile=0.99):
        self.quantile = quantile

    def fit(self, X, y=None):
        self.n_features_in_ = np.asarray(X).shape[1]
        # Ignore missing answers when calculating each training limit.
        self.upper_limits_ = np.nanquantile(np.asarray(X, dtype=float), self.quantile, axis=0)
        return self

    def transform(self, X):
        # Values below the cap stay unchanged. Missing values are filled later.
        return np.minimum(np.asarray(X, dtype=float), self.upper_limits_)

    # Keep the column names so the combined encoded features can be labelled.
    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            input_features = [f"x{i}" for i in range(self.n_features_in_)]
        return np.asarray(input_features, dtype=object)

def fill_missing_categories(frame):
    return frame.fillna("__MISSING__")

def add_q2_features(frame, features=None):
    result = frame.copy()
    features = q2_engineered_features if features is None else features
    if "LanguageCount" in features:
        result["LanguageCount"] = frame["LanguagesHaveWorkedWith"].map(
            lambda answer: np.nan if pd.isna(answer) else len(split_survey_answers(answer)))
    if "LogWorkExp" in features:
        # Missing experience stays missing and will be filled using fitting rows later.
        # log1p means the natural log of 1 + x, including a defined value at zero.
        result["LogWorkExp"] = np.log1p(frame["WorkExp"])
    if "PythonLogWorkExp" in features:
        # Match Python as a complete option, not as part of another name.
        # Use 1 for selected, 0 for a recorded list without Python, and NaN for unknown.
        python_selected = frame["LanguagesHaveWorkedWith"].map(
            lambda answer: np.nan if pd.isna(answer) else float("Python" in split_survey_answers(answer)))
        # Compute this directly so it also works when only this feature is requested.
        result["PythonLogWorkExp"] = np.log1p(frame["WorkExp"]) * python_selected
    return result

class CumulativeOrdinalClassifier(ClassifierMixin, BaseEstimator):
    """Combine K-1 binary logistic models for ordered integer class ranks."""

    def __init__(self, n_classes=15, C=1.0, penalty="l2", max_iter=1000,
                 tol=1e-4, random_state=None):
        self.n_classes = n_classes
        self.C = C
        self.penalty = penalty
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state

    def fit(self, X, y):
        X, y = check_X_y(X, y, accept_sparse="csr", dtype=np.float64, y_numeric=True)
        if not isinstance(self.n_classes, (int, np.integer)) or self.n_classes < 2:
            raise ValueError("n_classes must be an integer of at least 2.")
        if not np.all(y == np.floor(y)) or np.any(y < 0) or np.any(y >= self.n_classes):
            raise ValueError("y must contain integer ranks from 0 to n_classes - 1.")

        # Keep the defined salary order even if an intermediate class is absent.
        classes = np.arange(self.n_classes)
        thresholds = classes[:-1]
        if y.min() != 0 or y.max() != self.n_classes - 1:
            raise ValueError("Training rows must include the lowest and highest ranks so every threshold has both outcomes.")

        models = []
        for threshold in thresholds:
            # Positive means above this boundary, not membership in one exact class.
            binary_y = (y > threshold).astype(int)
            # liblinear supports both L1 and L2 for these binary problems.
            model = LogisticRegression(
                C=self.C, penalty=self.penalty, solver="liblinear",
                max_iter=self.max_iter, tol=self.tol, random_state=self.random_state)
            model.fit(X, binary_y)
            models.append(model)

        self.classes_ = classes
        self.thresholds_ = thresholds
        self.models_ = models
        self.n_features_in_ = X.shape[1]
        self.coef_ = np.vstack([model.coef_[0] for model in models])
        self.intercept_ = np.array([model.intercept_[0] for model in models])
        self.n_iter_ = np.array([model.n_iter_.max() for model in models])
        return self

    @staticmethod
    def repair_cumulative(probabilities):
        # Bound probabilities, then enforce a nonincreasing sequence across columns.
        return np.minimum.accumulate(np.clip(probabilities, 0.0, 1.0), axis=1)

    def predict_cumulative_proba(self, X, repair=True):
        check_is_fitted(self, "models_")
        X = check_array(X, accept_sparse="csr", dtype=np.float64)
        if X.shape[1] != self.n_features_in_:
            raise ValueError("Prediction inputs must have the same encoded columns as the fitting inputs.")
        # The binary classes are [0, 1], so column 1 is P(Y > threshold).
        probabilities = np.column_stack([model.predict_proba(X)[:, 1] for model in self.models_])
        return self.repair_cumulative(probabilities) if repair else probabilities

    def predict_proba(self, X):
        cumulative = self.predict_cumulative_proba(X)
        # Add P(Y > -1) = 1 and P(Y > highest rank) = 0 at the two ends.
        boundaries = np.column_stack([np.ones(len(cumulative)), cumulative, np.zeros(len(cumulative))])
        probabilities = boundaries[:, :-1] - boundaries[:, 1:]
        return probabilities / probabilities.sum(axis=1, keepdims=True)

    def predict(self, X):
        # argmax returns the first maximum, which gives the lower rank in a tie.
        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]

def predict_respondent_probabilities(answers):
    """Return the 15 salary-bucket probabilities from one person's survey answers."""
    if not isinstance(answers, (dict, pd.Series)):
        raise TypeError("Supply one respondent's answers as a dictionary or pandas Series.")
    missing_questions = [column for column in q3_required_raw_columns if column not in answers]
    if missing_questions:
        raise ValueError(f"Provide these questions, using None for unanswered questions: {missing_questions}")

    # Copy only the required input answers. Compensation and target fields are not used.
    numerical_questions = [column for column in numeric_columns if column in q3_required_raw_columns]
    cleaned = {}
    for column in q3_required_raw_columns:
        value = answers[column]
        if not pd.api.types.is_scalar(value):
            raise ValueError(f"{column}: use one value in the original CSV answer format.")
        if isinstance(value, str):
            value = value.strip()
            if not value:
                value = np.nan
        if pd.isna(value):
            value = np.nan
        elif column not in numerical_questions and not isinstance(value, str):
            raise ValueError(f"{column}: use the original survey answer text.")
        cleaned[column] = value
    row = pd.DataFrame([cleaned], columns=q3_required_raw_columns)

    # Convert numerical answers and reject infinite values before applying Q1's rules.
    for column in numerical_questions:
        row[column] = pd.to_numeric(row[column], errors="raise")
        if np.isinf(row[column].to_numpy(dtype=float)).any():
            raise ValueError(f"{column}: enter a finite number or leave the answer missing.")

    # Mark invalid fields as missing while keeping the respondent's other answers.
    age_limit = row["Age"].map({
        "Under 18 years old": 17, "18-24 years old": 24, "25-34 years old": 34,
        "35-44 years old": 44, "45-54 years old": 54, "55-64 years old": 64})
    for column in ["YearsCode", "WorkExp"]:
        invalid = row[column].lt(0) | row[column].gt(age_limit)
        row.loc[invalid, column] = np.nan
    for column, lower, upper in [("JobSat", 0, 10), ("KnowledgeA", 0, 168)]:
        if column in row:
            invalid = row[column].notna() & ~row[column].between(lower, upper)
            row.loc[invalid, column] = np.nan
    for column in ["ToolCount", "AIToolCount"]:
        if column in row:
            row.loc[row[column].lt(0), column] = np.nan

    # Recreate the retained engineered inputs and use the already fitted pipeline.
    # Keep them unscaled here because the stored pipeline applies its own scaler.
    model_inputs = add_q2_features(row, features=q2_selected_engineered)
    probabilities = q4_final_pipeline.predict_proba(model_inputs)[0]
    assert probabilities.shape == (len(salary_order),)
    assert np.isfinite(probabilities).all() and ((probabilities >= 0) & (probabilities <= 1)).all()
    assert np.isclose(probabilities.sum(), 1.0)
    return pd.Series(probabilities, index=pd.Index(salary_order, name="Salary bucket"),
                     name="Model-estimated probability")

def q5_5_recorded_options(answer):
    """Return reported selections without treating the missing marker as a skill."""
    return set(split_survey_answers(answer)) - {"__MISSING__"}

def q5_5_skill_profile(answers, skill, groups):
    """Copy a profile and simulate one addition under the stated assumptions."""
    changed = dict(answers)
    settings = q5_5_recorded_options(changed["TechDropDown"])
    for group in groups:
        options = q5_5_recorded_options(changed[group])
        options.add(skill)
        changed[group] = ";".join(sorted(options))
        settings.add(q5_5_setting_options[group])
    changed["TechDropDown"] = ";".join(sorted(settings))

    # Count a newly adopted platform/tool once, including options in two groups.
    counted_groups = {"DatabasesHaveWorkedWith", "CloudPlatHaveWorkedWith",
                      "KnowMgmtHaveWorkedWith"}
    web_tools = {"WordPress", "Drupal", "Node.js", "Deno"}
    adds_work_tool = bool(counted_groups.intersection(groups)) or skill in web_tools
    if adds_work_tool and pd.notna(changed["ToolCount"]):
        changed["ToolCount"] = float(changed["ToolCount"]) + 1
    return changed
