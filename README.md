# Salary Predictor and Skill Advisor

An interactive dashboard developed for MIE1624 Assignment 2 using the 2026 Stack Overflow Developer Survey. It estimates salary-bucket probabilities from survey answers and recommends skills, technologies, or tools to explore.

## Open the dashboard

[**Launch Salary Predictor and Skill Advisor**](https://haoming-ye-salary-skill-advisor.streamlit.app/)

The public dashboard runs in your browser. No sign-in, installation, or data upload is required.

## What you can do

- Answer 30 original survey questions across four sections: Your profile, Experience & work, Skills, and AI use.
- View predicted probabilities across all 15 ordered salary buckets, with annual compensation shown in USD.
- Explore up to three ranked recommendations based on their predicted improvement in your current profile score.
- Compare individual additions or any combination of the recommendations and see how the full probability distribution changes.

## How to use it

1. Enter your answers, using the question-mark icons for guidance. Answer every question that applies to you.
2. Review any unanswered questions on the AI use page and confirm the blanks you want to keep.
3. Select **Show my results** to view your salary-bucket probabilities and recommendations.
4. Select **Compare first recommendation** or expand **Try a combination** to explore different scenarios.

You can select **Load author's answers** to use the assignment author's Q5.5 example. **Start a new profile** clears the current answers and results. Answers are kept in the current app session and are not saved to an application database.

## Understanding the results

Each bar shows the estimated probability of one salary bucket. The 15 probabilities add up to 100% before rounding. Square brackets include an endpoint, and parentheses exclude it.

The **current profile score** is the probability-weighted average of bucket ranks from 0 to 14. A higher score means a higher average predicted bucket rank. Salary buckets have different dollar widths, so the score and its changes are measured in bucket positions, not dollars. The most likely bucket can stay the same even when the score increases.

Recommendations cover skills, technologies, or tools in the retained language, database, cloud/development, web, and knowledge-management questions. Eligible options must be named, absent from the profile, and reported by at least 109 training respondents. Each addition is first compared separately with the current profile. Positive score changes are ranked from largest to smallest, with up to three recommendations shown. Combinations are evaluated together using the model rather than by adding individual score increases.

### Author's example

The author's current profile score is **2.0288**. The three highest-ranked individual additions are:

| Rank | Skill | Score after adding the skill | Score increase |
| --- | --- | ---: | ---: |
| 1 | IBM DB2 | 2.4446 | +0.4159 |
| 2 | Databricks SQL | 2.3202 | +0.2914 |
| 3 | Fortran | 2.2443 | +0.2155 |

Each row starts from the same current profile. These are separate scenarios.

## Model and limitations

The dashboard uses the final cumulative-threshold ordinal logistic regression model selected in the assignment notebook, with L1 regularization and `C = 0.1`. It combines 14 binary logistic models to produce probabilities for 15 ordered salary buckets. The final model uses 31 retained feature groups, represented by 642 encoded inputs.

The saved model includes the preprocessing fitted on the training data. The dashboard derives engineered features and applies the same missing-value handling, encoding, and scaling to each new profile. It does not retrain the model when someone requests a prediction.

The model's held-out test accuracy is **33.42%**, so an individual prediction can be wrong. Its probabilities have not been checked for calibration. Missing answers and unusual profiles can further limit the usefulness of an estimate. Recommendations reflect survey associations and do not establish that learning a skill or adopting a technology or tool causes a salary increase. They also do not account for learning time, cost, or proficiency.

## Repository contents

| File | Purpose |
| --- | --- |
| `app.py` | Dashboard interface, input checks, and result displays |
| `question_config.py` and `form_options.py` | Question wording, guidance, and answer options |
| `model_components.py` and `model_service.py` | Preprocessing, ordinal predictions, and recommendation calculations |
| `artifacts/model.joblib` | Fitted model, preprocessing, and prediction metadata |
| `artifacts/manifest.json` | Model configuration and verification summary |
| `example_data.json` | Author's example answers and reference results |
| `requirements.txt` | Pinned Python dependencies |
| `.streamlit/config.toml` | Dashboard theme and runtime settings |

The original respondent-level datasets, assignment notebook, and course materials are not included in this repository. The fitted artifact is sufficient to run the dashboard without those files or API keys.

## Run locally (optional)

Use Python 3.12. From the repository folder, install the dependencies and start the app:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The public version is hosted on Streamlit Community Cloud using branch `main`, entrypoint `app.py`, and Python 3.12.
