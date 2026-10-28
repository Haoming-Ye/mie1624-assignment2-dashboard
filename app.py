"""Salary Predictor and Skill Advisor: frozen predictions from original answers."""
from pathlib import Path
from html import escape
import copy
import json
import math

import numpy as np
import streamlit as st

from model_service import SalaryModel
from question_config import QUESTIONS, SECTIONS
from form_options import OTHER, option_order, option_label

HERE = Path(__file__).resolve().parent
APP_NAME = "Salary Predictor and Skill Advisor"
st.set_page_config(page_title=APP_NAME, page_icon="S", layout="wide",
                   initial_sidebar_state="locked")

CSS = """
<style>
.stApp{background:#fff;color:#191919}
.block-container{max-width:1120px;padding-top:5rem;padding-bottom:4rem}
[data-testid="stSidebar"]{background:#fff;border-right:1px solid #e9e9e9}
[data-testid="stSidebar"][aria-expanded="true"]{min-width:230px;max-width:250px}
/* Let the collapsed sidebar release its space in the page layout. */
[data-testid="stSidebar"][aria-expanded="false"]{min-width:0!important;max-width:0!important;border-right:0}
/* The locked desktop sidebar does not need an empty control row. */
@media(min-width:769px){[data-testid="stSidebarHeader"]{display:none}
[data-testid="stSidebarUserContent"]{padding-top:32px}}
[data-testid="stSidebar"] .block-container{padding-top:2rem}
h1{font-weight:600!important;letter-spacing:-1.1px!important;font-size:2.2rem!important}
h2{font-weight:550!important;letter-spacing:-.4px!important;font-size:1.4rem!important}
h3{font-weight:550!important;font-size:1.06rem!important}
button{border-radius:9px!important}
[class*="st-key-multi_"] [data-testid="stMarkdownContainer"] p{font-size:14px;line-height:1.5;margin:0}
[class*="st-key-multi_"] [data-testid="stMarkdown"]{min-height:22px}
[class*="st-key-multi_"] [data-testid="stPopoverButton"]{min-height:40px;background:#f7f7f7;border-color:transparent;text-align:left}
[class*="st-key-multi_"] [data-testid="stPopoverButton"] div{justify-content:flex-start}
[class*="st-key-multi_"] [data-testid="stPopoverButton"]>div{width:100%;justify-content:space-between}
.brand{font-size:20px;line-height:1.3;font-weight:650;letter-spacing:-.3px;margin:0 0 10px}
.course{color:#666;font-size:12px;line-height:1.6;margin:0 0 34px}
.breadcrumb{font-size:12px;line-height:1.6;color:#777;padding:0 0 18px;border-bottom:1px solid #e9e9e9;margin-bottom:22px}
.subtle{font-size:13px;color:#737373;line-height:1.65}
.eyebrow{font-size:10px;font-weight:600;letter-spacing:1.2px;color:#777;margin:24px 0 12px}
.metric-grid{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:15px;margin:20px 0 32px}
.metric-box{border:1px solid #e9e9e9;border-radius:12px;padding:20px}
.metric-label{font-size:12px;color:#777;margin-bottom:10px}
.metric-value{font-size:27px;font-weight:550;letter-spacing:-.6px;line-height:1.3}
.metric-unit{font-size:11px;color:#777;margin-top:8px}
.chart{border:1px solid #e9e9e9;border-radius:12px;padding:24px 22px 18px;margin-bottom:16px}
.chart-title{font-size:15px;font-weight:550;margin-bottom:5px}
.chart-note{font-size:11px;color:#777;margin-bottom:20px}
.prob-row{display:grid;grid-template-columns:195px minmax(0,1fr) 57px;align-items:center;gap:12px;min-height:31px}
.bucket-label{font-size:11px;color:#555;white-space:nowrap;text-align:right}
.bar-track{height:12px;background:#f7f7f7;border-radius:2px;overflow:hidden}
.bar{height:12px;background:#4472c4;border-radius:2px}
.bar.mode{background:#203f73}.bar.after{background:#ed7d31}
.prob-value{font-size:11px;color:#555;font-variant-numeric:tabular-nums}
.axis{margin:10px 69px 0 207px;border-top:1px solid #ddd;display:flex;justify-content:space-between;padding-top:7px;color:#888;font-size:10px}
.axis-label{text-align:center;font-size:11px;color:#777;margin:12px 0 0 195px}
.paired .bar-track{height:24px;background:transparent;display:flex;flex-direction:column;gap:3px}
.paired .bar{height:10px}.paired.prob-row{min-height:38px}
.paired .prob-value{line-height:17px;font-size:10px}
.legend{font-size:11px;color:#666;display:flex;gap:20px;justify-content:flex-end;margin:0 0 15px}
.legend i{display:inline-block;width:15px;height:8px;margin-right:6px;border-radius:1px}
.rec-wrap{overflow-x:auto;border:1px solid #e9e9e9;border-radius:12px;margin:15px 0}
.rec-table{width:100%;border-collapse:collapse;font-size:13px}
.rec-table th{background:#fafafa;color:#777;font-size:11px;font-weight:500;text-align:left;padding:15px 18px;border-bottom:1px solid #e9e9e9}
.rec-table td{padding:17px 18px;border-bottom:1px solid #f0f0f0}
.rec-table tr:last-child td{border-bottom:0}.rec-table .number{text-align:right;font-variant-numeric:tabular-nums}
.skill-name{font-weight:550}.skill-group{font-size:11px;color:#777;margin-top:4px}
.rank{font-size:12px;color:#888}.gain{color:#295339}
.comparison-strip{font-size:13px;color:#666;line-height:1.8;margin-bottom:15px}
@media(max-width:760px){.block-container{padding-left:1.2rem;padding-right:1.2rem}
.metric-grid{grid-template-columns:1fr 1fr}.metric-box:first-child{grid-column:1/-1}
.metric-value{font-size:23px}.chart{padding:20px 10px}.prob-row{grid-template-columns:127px minmax(0,1fr) 43px;gap:7px}
.bucket-label{font-size:9px}.prob-value{font-size:10px}.axis{margin-left:134px;margin-right:50px}.axis-label{margin-left:100px}
.rec-table th,.rec-table td{padding:12px 10px}.rec-table{font-size:12px}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_resource
def load_model():
    # The cached artifact contains fitted settings, not respondent-level data.
    return SalaryModel.load()


model = load_model()
meta = model.metadata
if "answers" not in st.session_state:
    st.session_state.answers = {c: None for c in meta["required_columns"]}
    st.session_state.page = 0
    st.session_state.result = None
if "blanks_reviewed" not in st.session_state:
    st.session_state.blanks_reviewed = False
if "profile_source" not in st.session_state:
    st.session_state.profile_source = "custom"
if st.session_state.get("form_version") != 4:
    # Preserve survey answers when the form controls change.
    for key in list(st.session_state):
        if key.startswith(("answer_", "detail_", "choice_", "search_")) or key in {"custom_answers", "other_details"}:
            del st.session_state[key]
    st.session_state.form_version = 4


def reset_profile(example=False):
    for key in list(st.session_state):
        if key.startswith(("answer_", "addition_", "choice_", "search_")) or key == "review_blanks":
            del st.session_state[key]
    if example:
        st.session_state.answers = json.loads((HERE / "example_data.json").read_text(encoding="utf-8"))["answers"]
    else:
        st.session_state.answers = {c: None for c in meta["required_columns"]}
    st.session_state.page = 0
    st.session_state.result = None
    st.session_state.compare_open = False
    st.session_state.blanks_reviewed = False
    st.session_state.profile_source = "author" if example else "custom"


def store_answer(column):
    value = st.session_state[f"answer_{column}"]
    if column in meta["multiselect_columns"]:
        value = ";".join(value) if value else None
    st.session_state.answers[column] = value
    st.session_state.result = None
    if st.session_state.profile_source in {"author", "edited_author"}:
        st.session_state.profile_source = "edited_author"
    st.session_state.blanks_reviewed = False
    st.session_state.pop("review_blanks", None)


def store_choice(column, option, checkbox_key):
    # Save the original survey values, regardless of the current search filter.
    answer = st.session_state.answers[column]
    selected = set(answer.split(";")) if answer else set()
    if st.session_state[checkbox_key]:
        selected.add(option)
    else:
        selected.discard(option)
    st.session_state[f"answer_{column}"] = [
        value for value in option_order(column, meta["options"][column]) if value in selected]
    store_answer(column)


def render_multiple_choice(column, label, help_text):
    selected = st.session_state[f"answer_{column}"]
    summary = ", ".join(option_label(value) for value in selected) if selected else "Select all that apply"
    limit = 5 if column == "KnowledgeQ" else None
    with st.container(key=f"multi_{column}", gap="xsmall"):
        st.markdown(label, help=help_text)
        with st.popover(summary, key=f"options_{column}", width="stretch", wrap=False):
            st.caption(f"{len(selected)} selected. " + (
                "Choose up to five." if limit else "Select all that apply."))
            query = ""
            options = option_order(column, meta["options"][column])
            if len(options) > 10:
                query = st.text_input("Search options", key=f"search_{column}",
                                      type="search", live=True).strip().casefold()
            visible = [value for value in options if query in option_label(value).casefold()]
            if not visible:
                st.caption("No matching options. Try another search.")
            # The list scrolls while every option keeps its original order.
            with st.container(height=280 if len(visible) > 6 else "content",
                              border=False, gap="xxsmall"):
                for option in visible:
                    key = f"choice_{column}_{meta['options'][column].index(option)}"
                    if key not in st.session_state:
                        st.session_state[key] = option in selected
                    st.checkbox(option_label(option), key=key, width="stretch",
                                disabled=bool(limit and len(selected) >= limit and option not in selected),
                                on_change=store_choice, args=(column, option, key))


def unanswered_questions(answers):
    return [column for _, _, columns in SECTIONS for column in columns
            if answers[column] is None]


def store_blank_review():
    st.session_state.blanks_reviewed = st.session_state.review_blanks


def render_question(column):
    label, hint = QUESTIONS[column]
    key = f"answer_{column}"
    value = st.session_state.answers[column]
    multiple = column in meta["multiselect_columns"]
    has_other = OTHER in meta["options"].get(column, [])
    if key not in st.session_state:
        if multiple:
            value = [] if value is None else value.split(";")
        st.session_state[key] = value
    help_text = hint
    if has_other:
        help_text += " Choose Other if your answer is not listed."
    if column in meta["numeric_columns"]:
        st.number_input(label, min_value=0, max_value=10 if column == "JobSat" else None,
                        step=1, value=None, key=key, placeholder="Enter a whole number",
                        help=help_text, on_change=store_answer, args=(column,))
    elif multiple:
        render_multiple_choice(column, label, help_text)
    else:
        st.selectbox(label, options=option_order(column, meta["options"][column]), key=key,
                     index=None, placeholder="Select an answer", format_func=option_label,
                     accept_new_options=False,
                     help=help_text, on_change=store_answer, args=(column,))


def profile_issues(answers):
    issues = []
    limits = {"Under 18 years old": 17, "18-24 years old": 24, "25-34 years old": 34,
              "35-44 years old": 44, "45-54 years old": 54, "55-64 years old": 64}
    limit = limits.get(answers["Age"])
    for name in ["YearsCode", "WorkExp"]:
        value = answers[name]
        if value is not None and limit is not None and value > limit:
            issues.append(f"{QUESTIONS[name][0]} exceeds your age group. Correct it or leave it unanswered.")
    for col in meta["multiselect_columns"]:
        selected = [] if answers[col] is None else answers[col].split(";")
        exclusive = [v for v in selected if v.casefold().replace("’", "'").startswith(
            ("none", "prefer not", "i prefer not", "i don't use", "i do not use",
             "i do not have a role", "not sure"))]
        if exclusive and len(selected) > 1:
            issues.append(f"{QUESTIONS[col][0]}: choose '{exclusive[0]}' by itself or remove it.")
    return issues


def interval_labels():
    labels = []
    for label in meta["salary_order"]:
        if label.startswith(">"):
            labels.append(f"({label[1:]}, ∞)")
        else:
            lower, upper = label.split("–", 1)
            labels.append(f"[{lower}, {upper.lstrip('<≤')}{']' if upper.startswith('≤') else ')'}")
    return labels


def chart(probabilities, after=None):
    values = np.asarray(probabilities)
    largest = max(values.max(), 0 if after is None else max(after)) * 100
    maximum = min(100, max(10, math.ceil(largest * 1.12 / 10) * 10))
    highest = int(values.argmax())
    title = "Your salary-bucket probabilities" if after is None else "Before and after the selected additions"
    content = ['<div class="chart">', f'<div class="chart-title">{title}</div>',
               '<div class="chart-note">Annual compensation in USD. All 15 ordered salary buckets are shown.</div>']
    if after is not None:
        content.append('<div class="legend"><span><i style="background:#4472c4"></i>Current profile</span><span><i style="background:#ed7d31"></i>After additions</span></div>')
    else:
        content.append('<div class="legend"><span><i style="background:#4472c4"></i>Predicted probability</span><span><i style="background:#203f73"></i>Highest probability</span></div>')
    for rank, (label, probability) in enumerate(zip(interval_labels(), values)):
        content.append(f'<div class="prob-row{" paired" if after is not None else ""}"><div class="bucket-label">{escape(label)}</div><div class="bar-track">')
        color = " mode" if after is None and rank == highest else ""
        content.append(f'<div class="bar{color}" style="width:{probability * 100 / maximum * 100:.8f}%"></div>')
        if after is not None:
            content.append(f'<div class="bar after" style="width:{after[rank] * 100 / maximum * 100:.8f}%"></div>')
        numbers = f"{probability * 100:.2f}%"
        if after is not None:
            numbers += f"<br>{after[rank] * 100:.2f}%"
        content.append(f'</div><div class="prob-value">{numbers}</div></div>')
    content.append('<div class="axis">' + ''.join(f'<span>{v:g}%</span>' for v in np.linspace(0, maximum, 6)) + '</div>')
    content.append('<div class="axis-label">Model-estimated probability (%)</div></div>')
    st.html("".join(content))


def calculate_results():
    issues = profile_issues(st.session_state.answers)
    if issues:
        for issue in issues:
            st.error(issue)
        return
    if not any(v is not None for v in st.session_state.answers.values()):
        st.info("Answer at least one question before viewing your results.")
        return
    if unanswered_questions(st.session_state.answers) and not st.session_state.blanks_reviewed:
        st.error("Review the unanswered questions below and complete any that apply to you. Confirm the remaining blanks before continuing.")
        return
    with st.spinner("Calculating your distribution and comparing eligible additions..."):
        st.session_state.result = model.recommend(st.session_state.answers)
        st.session_state.result_answers = copy.deepcopy(st.session_state.answers)
    for key in list(st.session_state):
        if key.startswith("addition_"):
            del st.session_state[key]
    st.session_state.compare_open = False
    st.session_state.page = 4
    st.rerun()


def compare_first():
    recs = st.session_state.result["recommendations"]
    for row in recs:
        st.session_state[f"addition_{row['skill']}"] = row == recs[0]
    st.session_state.compare_open = True


with st.sidebar:
    st.html('<div class="brand">Salary Predictor<br>and Skill Advisor</div><div class="course">MIE1624 · Assignment 2</div>')
    for number, (name, _, columns) in enumerate(SECTIONS):
        if st.button(f"{number + 1}. {name}", key=f"nav_{number}", width="stretch",
                     type="primary" if st.session_state.page == number else "tertiary"):
            st.session_state.page = number
            st.rerun()
    if st.button("Results", key="nav_results", width="stretch",
                 disabled=st.session_state.result is None,
                 type="primary" if st.session_state.page == 4 else "tertiary"):
        st.session_state.page = 4
        st.rerun()
    st.divider()
    st.button("Load author's answers", key="load_example", width="stretch",
              help="Loads the assignment author's survey answers used in Q5.5. This replaces the current answers in this session.",
              on_click=reset_profile, args=(True,))
    st.button("Start a new profile", key="clear_profile", width="stretch", on_click=reset_profile)
    st.caption("Your answers are used for this session. They are not saved to a database.")

page = st.session_state.page
name = SECTIONS[page][0] if page < 4 else "Results"
st.html(f'<div class="breadcrumb">{escape(APP_NAME)} &nbsp; / &nbsp; {escape(name)}</div>')

if page < 4:
    title, description, columns = SECTIONS[page]
    st.caption(f"STEP {page + 1} OF 4")
    st.title(title)
    st.write(description)
    if st.session_state.profile_source == "author":
        st.caption("Showing the assignment author's Q5.5 survey answers.")
    elif st.session_state.profile_source == "edited_author":
        st.caption("Showing an edited copy of the author's example answers.")
    st.caption("Answer the questions that apply to you. You can leave a question blank if it does not apply. A blank answer is different from selecting None of the above.")
    answered = sum(v is not None for v in st.session_state.answers.values())
    st.progress(answered / 30, text=f"{answered} of 30 questions answered")
    st.write("")
    for start in range(0, len(columns), 2):
        left, right = st.columns(2, gap="large")
        with left:
            render_question(columns[start])
        if start + 1 < len(columns):
            with right:
                render_question(columns[start + 1])
    for issue in profile_issues(st.session_state.answers):
        st.warning(issue)
    if page == 3:
        missing = unanswered_questions(st.session_state.answers)
        if missing:
            st.subheader("Review unanswered questions")
            st.warning(f"{30 - len(missing)} of 30 questions answered. Complete every question that applies to you. Missing answers can affect the estimate, and a high predicted probability does not guarantee a correct prediction.")
            with st.expander(f"Unanswered questions ({len(missing)})"):
                for column in missing:
                    st.write(f"- {QUESTIONS[column][0]}")
            if "review_blanks" not in st.session_state:
                st.session_state.review_blanks = st.session_state.blanks_reviewed
            st.checkbox("I reviewed these questions and want to keep the remaining answers blank.",
                        key="review_blanks", on_change=store_blank_review)
    st.divider()
    left, _, right = st.columns([1, 1, 1])
    with left:
        if st.button("Back", disabled=page == 0, width="stretch"):
            st.session_state.page -= 1
            st.rerun()
    with right:
        if page < 3:
            if st.button("Continue", type="primary", width="stretch"):
                st.session_state.page += 1
                st.rerun()
        elif st.button("Show my results", type="primary", width="stretch"):
            calculate_results()
else:
    result = st.session_state.result
    if st.session_state.profile_source == "author":
        st.title("Author's example results")
        st.write("Model estimates and skill recommendations for the assignment author's Q5.5 survey answers.")
    elif st.session_state.profile_source == "edited_author":
        st.title("Edited example results")
        st.write("Model estimates and skill recommendations for your edited copy of the author's example.")
    else:
        st.title("Your results")
        st.write("A model estimate based on your survey answers, with skills to explore.")
    missing = unanswered_questions(st.session_state.result_answers)
    st.caption(f"Based on {30 - len(missing)} of 30 answered questions.")
    if missing:
        st.info("This estimate uses incomplete information. A high predicted probability does not guarantee an accurate prediction. You can edit your answers to add more information.")
    probabilities = np.asarray(result["probabilities"])
    mode = int(probabilities.argmax())
    salary_label = interval_labels()[mode]
    st.html(f'''<div class="metric-grid">
      <div class="metric-box"><div class="metric-label">Most likely salary bucket</div><div class="metric-value">{escape(salary_label)}</div><div class="metric-unit">Annual compensation, USD</div></div>
      <div class="metric-box"><div class="metric-label">Probability of that bucket</div><div class="metric-value">{probabilities[mode] * 100:.2f}%</div><div class="metric-unit">Model estimate</div></div>
      <div class="metric-box"><div class="metric-label">Current profile score</div><div class="metric-value">{result['score']:.4f}</div><div class="metric-unit">Bucket positions, from 0 to 14</div></div>
    </div>''')
    chart(probabilities)
    with st.expander("How to read these results"):
        st.write("Each bar is the probability of one salary bucket. The 15 probabilities add up to 100% before rounding. Square brackets include an endpoint, and parentheses exclude it.")
        st.write("The current profile score is the sum of each bucket's rank multiplied by its probability. Ranks run from 0 to 14. The score uses all 15 probabilities and is measured in bucket positions, not dollars. Salary buckets have unequal dollar widths.")
        st.write("These probabilities have not been checked for calibration. The model's held-out test accuracy is 33.42%, so an individual estimate can be wrong. More unanswered questions leave the model with less information about you.")
    st.write("")
    st.header("Skills to explore")
    st.caption("Scores are in bucket positions, not dollars. Each addition is compared with your current profile, so the increases are separate rather than cumulative.")
    recs = result["recommendations"]
    if recs:
        rows = []
        for rank, row in enumerate(recs, 1):
            rows.append(f'''<tr><td class="rank">{rank}</td><td><div class="skill-name">{escape(row['skill'])}</div><div class="skill-group">{escape(row['group'])}</div></td><td class="number">{row['support']:,}</td><td class="number">{row['score']:.4f}</td><td class="number gain">+{row['increase']:.4f}</td></tr>''')
        st.html('<div class="rec-wrap"><table class="rec-table"><thead><tr><th>Rank</th><th>Skills</th><th class="number">Training respondents</th><th class="number">Score after adding the skill</th><th class="number">Score increase</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')
        if len(recs) < 3:
            st.info(f"This profile has {len(recs)} eligible additions with a positive predicted score change. Only those additions are shown.")
        st.button("Compare first recommendation", key="compare_first", on_click=compare_first)
        with st.expander("Try a combination", expanded=st.session_state.get("compare_open", False)):
            st.write("Choose any combination of the recommendations to calculate their joint effect. Individual score increases are not added together.")
            chosen = []
            for row in recs:
                if st.checkbox(row["skill"], key=f"addition_{row['skill']}"):
                    chosen.append(row["skill"])
            if chosen:
                after_answers = model.add_skills(st.session_state.result_answers, chosen)
                after = model.predict(after_answers)
                score = model.score(after)
                after_mode = int(after.argmax())
                st.html(f'<div class="comparison-strip">Current profile score: <strong>{result["score"]:.4f}</strong><br>Score after the additions: <strong>{score:.4f}</strong><br>Score change: <strong>{score - result["score"]:+.4f} bucket positions</strong><br>Most likely bucket after the additions: <strong>{escape(interval_labels()[after_mode])}</strong> ({after[after_mode] * 100:.2f}%)</div>')
                chart(probabilities, after)
                st.caption("A combination can have a smaller improvement than an individual addition, or no improvement. The most likely bucket can stay the same even when the average-rank score increases.")
            else:
                st.caption("No additions selected. Your profile and its distribution remain unchanged.")
    else:
        st.info("No eligible additions increased the score for these answers. Try another profile only if it reflects your actual answers.")
    with st.expander("How recommendations are ranked"):
        st.write("Recommendations cover skills, technologies, or tools in the model's retained language, database, cloud/development, web, and knowledge-management questions. The survey records use rather than proficiency.")
        st.write(f"Each option must be named, not already reported in any of those questions, and reported by at least {meta['minimum_support']} training respondents (1%, rounded up). Missing, none, other, and prefer-not-to-say options are excluded. Respondents are counted once when an option appears in more than one question.")
        st.write("Each scenario adds one option to its relevant survey questions and related technology setting. A new database, cloud/development tool, or knowledge-management platform adds one to the monthly work-tool count if that count was answered. WordPress, Drupal, Node.js, and Deno also add one. Languages and framework packages do not. Other answers stay fixed.")
        st.write("The app predicts each new distribution using the same fitted model and preprocessing, then subtracts the current profile score from the new score. Positive changes are ranked from largest to smallest, with exact ties broken alphabetically. The first three are shown, or fewer if fewer positive changes exist.")
        st.caption(f"Eligible additions evaluated: {result['evaluated']}. Positive score changes: {result['positive']}.")
    st.caption("Learning a skill or adopting a technology or tool does not guarantee a salary increase. These comparisons reflect survey associations, not causal effects. Unusual answer combinations, missing information, learning time, cost, and proficiency can limit their usefulness.")
    if st.button("Edit my answers", key="edit_answers"):
        st.session_state.page = 0
        st.rerun()
