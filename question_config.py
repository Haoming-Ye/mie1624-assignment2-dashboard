"""Original survey questions needed by the final selected model."""
SECTIONS = [
    ("Your profile", "A few details about your background.", [
        "Country", "Age", "Education", "Currency", "Employment"]),
    ("Experience & work", "Your experience and current professional role.", [
        "YearsCode", "WorkExp", "EmploymentAddl", "OrgSize", "WorkSetting", "ICorPM",
        "JobSat", "ToolCount", "PurchasePower", "RoleFunctions", "KnowledgeQ", "KnowledgeTime_1"]),
    ("Skills", "What you have used and how you have learned.", [
        "LanguagesHaveWorkedWith", "DatabasesHaveWorkedWith", "CloudPlatHaveWorkedWith",
        "WebFrameworkHaveWorkedWith", "KnowMgmtHaveWorkedWith", "TechDropDown", "LearnCodeHow"]),
    ("AI use", "AI tools and learning in your current workflow.", [
        "LearnAI", "AISelect", "AITry", "AIUse", "LearnAIHow", "AIWorkCurrentlyUse"]),
]

QUESTIONS = {
    "Country": ("Country of residence", "The country where you currently live."),
    "Age": ("Age range", "Your current age group."),
    "Education": ("Highest completed education", "Leave out qualifications still in progress."),
    "Currency": ("Currency used day to day", "The currency you use day to day. If you use several, choose the one you are most comfortable estimating in. All predicted salary ranges are shown in USD."),
    "Employment": ("Main employment status", "Choose your main current employment status."),
    "YearsCode": ("Years of coding experience", "Include education and personal projects. Round to the nearest whole year."),
    "WorkExp": ("Years of professional work experience", "Total years working professionally, including work that did not involve coding. Round to the nearest whole year. You can leave this unanswered if you have no professional experience."),
    "EmploymentAddl": ("Additional work, school, or life responsibilities", "Your current responsibilities in addition to your main employment status. Select all that apply."),
    "OrgSize": ("Number of employees at your main employer", "If you had several employers, use the one you spent the most time working for in the past year. Count the whole primary company."),
    "WorkSetting": ("Work arrangement", "Whether you work in person, remotely, or in a hybrid arrangement. The two hybrid options distinguish work that leans toward in-person attendance from work that leans toward flexibility."),
    "ICorPM": ("Individual contributor or people manager?", "An individual contributor is primarily responsible for their own work rather than managing employees. A people manager supervises employees. Choose the option that best describes your current role."),
    "JobSat": ("Job satisfaction (0 to 10)", "Your satisfaction with your current professional role. Zero is the lowest satisfaction rating and 10 is the highest."),
    "ToolCount": ("Number of tools used in a typical work month", "Count distinct software tools, platforms, or services used for primary work in a typical month over the past year. Exclude operating systems, browsers, programming languages, libraries, packages, one-off scripts, and interchangeable utilities serving the same narrow purpose."),
    "PurchasePower": ("Role in choosing software", "Your role in choosing or using software at your organization. Select all that apply."),
    "RoleFunctions": ("Typical weekly work activities", "Activities that are part of your work in a typical week. Select all that apply."),
    "KnowledgeQ": ("Sources you use for work-related questions", "The sources you use most often when answering a work-related question. Select up to five."),
    "KnowledgeTime_1": ("Importance of recent information from coworkers", "How important is it that information from coworkers or teammates is recent or clearly timestamped?"),
    "LanguagesHaveWorkedWith": ("Programming, scripting, and markup languages", "Languages you did extensive development work in over the past year. Select all that apply."),
    "DatabasesHaveWorkedWith": ("Databases used", "Database environments you did extensive development work in over the past year. Select all that apply."),
    "CloudPlatHaveWorkedWith": ("Cloud and development tools", "Cloud platforms, container tools, package managers, build tools, and infrastructure tools you did extensive development work in over the past year."),
    "WebFrameworkHaveWorkedWith": ("Web frameworks and technologies used", "Web frameworks and technologies you did extensive development work in over the past year. Select all that apply."),
    "KnowMgmtHaveWorkedWith": ("Knowledge management platforms used", "Platforms you used for work in the past year to organize or share knowledge, such as Google Docs, SharePoint, or Notion. Select all that apply."),
    "TechDropDown": ("Types of technology you used in the past year", "Technology settings used at work, school, or in personal projects in the last 12 months. Select all that apply."),
    "LearnCodeHow": ("How you learned to code", "How you learned to code in the past year. Select all that apply."),
    "LearnAI": ("Learning AI over the past year", "Whether you spent time learning AI programming or AI-enabled tools on your own or at work in the past year."),
    "AISelect": ("AI tools used at work", "AI tools or agents you currently use in your role at work. Select all that apply."),
    "AITry": ("Your organization's approach to AI tools", "Choose the option that best describes how your organization currently approaches AI tools or models."),
    "AIUse": ("How your organization uses AI", "Choose the option that best describes how AI tools or agents are used at your organization today."),
    "LearnAIHow": ("How you learned to code for AI", "How you learned to code for AI in the past year. Select all that apply."),
    "AIWorkCurrentlyUse": ("Tasks you use AI for", "Workflow tasks you currently use AI or AI agents for. Include current use rather than planned use."),
}
