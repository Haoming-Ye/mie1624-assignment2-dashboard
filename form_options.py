"""Display survey options clearly while preserving their trained answer labels."""
OTHER = "Other, please specify"

# These are display labels only. Widget values keep the exact survey wording.
LABELS = {
    OTHER: "Other",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "Primary/elementary school": "Primary / elementary school",
    "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": "Secondary / high school",
    "Some college/university study without earning a degree": "Some college / university, no degree",
    "Associate degree (A.A., A.S., etc.)": "Associate degree",
    "Bachelor's degree (B.A., B.S., B.Eng., etc.)": "Bachelor's degree",
    "Master's degree (M.A., M.S., M.Eng., MBA, etc.)": "Master's degree",
    "Professional degree (JD, MD, Ph.D, Ed.D, etc.)": "Professional / doctoral degree (e.g. JD, MD, PhD)",
    "Just me - I am a freelancer, sole proprietor, etc.": "Just me / self-employed",
    "Independent contractor, freelancer, or self-employed": "Self-employed, freelancer, or independent contractor",
    "I prefer not to say": "Prefer not to say",
    "Hybrid (some remote, leans heavy to in-person)": "Hybrid, mostly in person",
    "Hybrid (some in-person, leans heavy to flexibility)": "Hybrid, more flexible",
    "Your choice (very flexible, you can come in when you want or just as needed)": "Flexible, in-person attendance as needed",
    "Individual contributor in a senior or staff-level role": "Senior / staff individual contributor",
    "I approve or manage budget for tools": "Approve or manage tool budgets",
    "I do not have a role in choosing or using software tools at my organization": "No role in choosing or using software tools",
    "I evaluate, recommend, or shortlist tools": "Evaluate, recommend, or shortlist tools",
    "I influence tool choices by giving feedback or requirements": "Influence choices through feedback or requirements",
    "I make the final decision to purchase tools": "Make final purchasing decisions",
    "I use tools selected by others": "Use tools chosen by others",
    "I used a programming, scripting, or markup language for any reason": "Programming, scripting, or markup languages",
    "I used a development environment (IDE) to write code or interact with agent-assisted developer tools": "IDEs, code editors, or agent-assisted developer tools",
    "I built, maintained or learned about web technologies": "Web technologies",
    "I used a database for storage, querying, deployment": "Databases",
    "I used a cloud platform or any tools related to cloud technologies": "Cloud platforms and related tools",
    "I used an LLM (large language model)": "Large language models (LLMs)",
    "I used a community platform or online public forum to search, comment, post to, or read from for technology-related content": "Technology communities and online forums",
    "I used a knowledge management platform (such as a wiki)": "Knowledge management platforms",
    "I used an enterprise search platform (a secure way to search for disparate internal content)": "Enterprise search for internal content",
    "I used security software for permissions and compliance operations": "Security and compliance software",
    "AI use is mostly optional and left up to individuals": "AI use is optional for individuals",
    "My organization does not currently use AI tools or agents for work": "No AI tools or agents used for work",
    "Some teams actively encourage AI use, but practices vary across the organization": "Some teams encourage AI use",
    "My organization provides approved AI tools and guidance for how to use them": "Approved AI tools and guidance are provided",
    "My organization expects some employees to use AI tools for certain types of work": "Some employees are expected to use AI for certain tasks",
    "My organization measures or evaluates AI use as part of employee or team performance": "AI use is measured in employee or team performance",
    "We are not using AI tools or models in a meaningful way": "No meaningful AI use",
    "We are trying multiple tools or models before deciding what to use longer-term": "Trying several AI tools before deciding",
    "Different teams choose their own tools or models": "Teams choose their own AI tools or models",
    "We mostly use one approved tool or model": "Mostly one approved AI tool or model",
    "We use a few approved tools or models": "Several approved AI tools or models",
    "We are building internal tools or models": "Building internal AI tools or models",
    "School (i.e., university, college, etc)": "School, college, or university",
    "School (i.e., University, College, etc)": "School, college, or university",
    "Online courses or certification (includes all media types)": "Online courses or certifications",
    "Online Courses or Certification (includes all media types)": "Online courses or certifications",
    "Technical documentation (is generated for/by the tool or system)": "Technical documentation",
    "Videos (not associated with specific online course or certification)": "Videos outside a course or certification",
    "Other online resources (e.g. standard search, forum, online community)": "Other online resources (search, forums, communities)",
    "AI codegen tools or AI-enabled apps": "AI coding tools or AI-enabled apps",
    "AI CodeGen tools or AI-enabled apps": "AI coding tools or AI-enabled apps",
    "Internal documentation (i.e. Design, product, or planning docs), wiki, or knowledge base": "Internal documentation, wiki, or knowledge base",
    "Internal chat tools, such as Slack or Teams": "Internal chat, such as Slack or Teams",
}

ORDERED = {
    "Age": ["Under 18 years old", "18-24 years old", "25-34 years old", "35-44 years old",
            "45-54 years old", "55-64 years old", "65 years or older"],
    "Education": ["Primary/elementary school",
        "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)",
        "Some college/university study without earning a degree", "Associate degree (A.A., A.S., etc.)",
        "Bachelor's degree (B.A., B.S., B.Eng., etc.)", "Master's degree (M.A., M.S., M.Eng., MBA, etc.)",
        "Professional degree (JD, MD, Ph.D, Ed.D, etc.)"],
    "OrgSize": ["Just me - I am a freelancer, sole proprietor, etc.", "Less than 20 employees",
        "20 to 99 employees", "100 to 499 employees", "500 to 999 employees",
        "1,000 to 4,999 employees", "5,000 to 9,999 employees", "10,000 or more employees"],
    "KnowledgeTime_1": ["Least important", "Not very important", "Somewhat important", "Important", "Very important"],
    "Employment": ["Employed", "Independent contractor, freelancer, or self-employed", "Student", "Not employed", "Retired"],
    "WorkSetting": ["In-person", "Hybrid (some remote, leans heavy to in-person)",
        "Hybrid (some in-person, leans heavy to flexibility)", "Remote",
        "Your choice (very flexible, you can come in when you want or just as needed)"],
    "ICorPM": ["Individual contributor", "Individual contributor in a senior or staff-level role",
        "Both people manager and individual contributor", "People manager"],
    "LearnAI": ["No", "Yes, on my own", "Yes, at work", "Yes, both on my own and at work"],
    "EmploymentAddl": ["Attending school (full-time)", "Attending school (part-time)",
        "Engaged in paid work (less than 10 hours per week)", "Engaged in paid work (10-19 hours per week)",
        "Engaged in paid work (20-29 hours per week)", "Caring for dependents (children, elderly, etc.)",
        "Volunteering (regularly)", "Transitioning to retirement (gradually reducing work hours)"],
    "PurchasePower": ["I use tools selected by others", "I influence tool choices by giving feedback or requirements",
        "I evaluate, recommend, or shortlist tools", "I approve or manage budget for tools",
        "I make the final decision to purchase tools", "I do not have a role in choosing or using software tools at my organization"],
    "TechDropDown": ["I used a programming, scripting, or markup language for any reason",
        "I used a development environment (IDE) to write code or interact with agent-assisted developer tools",
        "I built, maintained or learned about web technologies", "I used a database for storage, querying, deployment",
        "I used a cloud platform or any tools related to cloud technologies", "I used an LLM (large language model)",
        "I used a community platform or online public forum to search, comment, post to, or read from for technology-related content",
        "I used a knowledge management platform (such as a wiki)",
        "I used an enterprise search platform (a secure way to search for disparate internal content)",
        "I used security software for permissions and compliance operations"],
    "AITry": ["We are not using AI tools or models in a meaningful way",
        "We are trying multiple tools or models before deciding what to use longer-term",
        "Different teams choose their own tools or models", "We mostly use one approved tool or model",
        "We use a few approved tools or models", "We are building internal tools or models"],
    "AIUse": ["My organization does not currently use AI tools or agents for work",
        "AI use is mostly optional and left up to individuals",
        "Some teams actively encourage AI use, but practices vary across the organization",
        "My organization provides approved AI tools and guidance for how to use them",
        "My organization expects some employees to use AI tools for certain types of work",
        "My organization measures or evaluates AI use as part of employee or team performance"],
}


def option_order(column, options):
    """Order real choices logically or alphabetically, with fallback choices last."""
    positions = {v.casefold(): i for i, v in enumerate(ORDERED.get(column, []))}

    def key(value):
        text = value.casefold().replace("’", "'")
        special = 0
        if text.startswith(("none", "i don't use", "i do not have a role")):
            special = 1
        elif text == OTHER.casefold():
            special = 2
        elif text in {"not sure", "i don't know"}:
            special = 3
        elif "prefer not" in text:
            special = 4
        return special, positions.get(value.casefold(), len(positions)), option_label(value).casefold()

    return sorted(options, key=key)


def option_label(value):
    """Use concise labels while keeping a distinct choice for every survey value."""
    return LABELS.get(value, value)
