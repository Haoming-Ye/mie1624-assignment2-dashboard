# Salary Predictor and Skill Advisor

Interactive dashboard for MIE1624 Assignment 2. Enter the 30 original survey answers used by the selected model to view probabilities across 15 ordered salary buckets and ranked recommendations for skills, technologies, or tools.

## Run locally

Use Python 3.12, install requirements.txt, then run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The fitted model and its training-fitted preprocessing are included in artifacts/model.joblib. The app does not read a respondent CSV, run the assignment notebook, repeat training, or require API keys. Answers are kept in the current session, with no application database.

## Deploy on Streamlit Community Cloud

Select this repository, branch main, and entrypoint app.py. In Advanced settings choose Python 3.12. Set the deployed app to public so viewers can open its URL without signing in.

## Check the example

Choose Load author's answers, review the unanswered questions on the AI use page, then choose Show my results. The Q5.5 example has a current profile score of 2.0288 and recommendations IBM DB2, Databricks SQL, and Fortran. IBM DB2 alone gives score 2.4446, an increase of 0.4159 bucket positions.

Probabilities are model estimates. Recommendations describe survey associations and do not establish that learning or adopting something causes a salary increase. Scores are in bucket positions, not dollars.

The original assignment dataset, notebook, course materials, development environment, and analysis caches are not included in this repository.
