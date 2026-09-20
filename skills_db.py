"""
The skill dictionary.

Each skill has:
  aliases  - other ways it gets written, so "sklearn" matches "scikit-learn"
  category - used for grouping in the UI
  learn    - what to actually do about it if you're missing it

This file is the heart of the tool. Adding skills here makes it smarter.
"""

SKILLS = {
    # ---------------- Languages ----------------
    "Python": {
        "aliases": ["python", "python3"],
        "category": "Languages",
        "learn": "Already the core language for ML. Focus on pandas and NumPy fluency over syntax.",
    },
    "SQL": {
        "aliases": ["sql", "mysql", "postgresql", "postgres", "sqlite", "t-sql"],
        "category": "Languages",
        "learn": "Learn joins, window functions and GROUP BY. Practice on SQLZoo or StrataScratch.",
    },
    "R": {
        "aliases": [" r ", "rstudio", "r language"],
        "category": "Languages",
        "learn": "Only worth learning if the role is statistics-heavy or in research.",
    },
    "Java": {
        "aliases": ["java"],
        "category": "Languages",
        "learn": "Relevant for large-scale backend or Android roles, not core ML.",
    },
    "JavaScript": {
        "aliases": ["javascript", "js", "typescript"],
        "category": "Languages",
        "learn": "Useful for shipping ML demos as web apps rather than notebooks.",
    },

    # ---------------- Core ML ----------------
    "Machine Learning": {
        "aliases": ["machine learning", "ml", "supervised learning",
                    "unsupervised learning"],
        "category": "Machine Learning",
        "learn": "Build three end-to-end projects: classification, regression, clustering.",
    },
    "Deep Learning": {
        "aliases": ["deep learning", "neural network", "neural networks", "cnn",
                    "rnn", "lstm", "transformer"],
        "category": "Machine Learning",
        "learn": "Start with CNNs on image data, then sequence models. Fast.ai or the Deep Learning Specialization.",
    },
    "scikit-learn": {
        "aliases": ["scikit-learn", "sklearn", "scikit learn"],
        "category": "Machine Learning",
        "learn": "The default toolkit for classical ML. Learn Pipeline and GridSearchCV specifically.",
    },
    "TensorFlow": {
        "aliases": ["tensorflow", "tf", "keras"],
        "category": "Machine Learning",
        "learn": "Pick this or PyTorch, not both. Keras is the gentler entry point.",
    },
    "PyTorch": {
        "aliases": ["pytorch", "torch"],
        "category": "Machine Learning",
        "learn": "Dominant in research and increasingly in industry. Learn nn.Module and DataLoader first.",
    },
    "NLP": {
        "aliases": ["nlp", "natural language processing", "text mining",
                    "sentiment analysis", "spacy", "nltk"],
        "category": "Machine Learning",
        "learn": "Learn tokenization, embeddings and fine-tuning. Hugging Face course is the fastest route.",
    },
    "Computer Vision": {
        "aliases": ["computer vision", "opencv", "image classification",
                    "object detection", "yolo"],
        "category": "Machine Learning",
        "learn": "Start with transfer learning on a pretrained model. You need fewer images than you think.",
    },
    "LLMs": {
        "aliases": ["llm", "llms", "large language model", "gpt", "prompt engineering",
                    "rag", "retrieval augmented", "langchain", "llamaindex"],
        "category": "Machine Learning",
        "learn": "Build one RAG application end to end. That single project covers embeddings, vector search and prompting.",
    },
    "MLOps": {
        "aliases": ["mlops", "model deployment", "mlflow", "model monitoring",
                    "kubeflow"],
        "category": "Machine Learning",
        "learn": "Deploy one model behind an API and track experiments with MLflow. Rare in student CVs, so it stands out.",
    },

    # ---------------- Data ----------------
    "pandas": {
        "aliases": ["pandas"],
        "category": "Data",
        "learn": "Learn groupby, merge and pivot properly. These three cover most real work.",
    },
    "NumPy": {
        "aliases": ["numpy"],
        "category": "Data",
        "learn": "Understand broadcasting and vectorization instead of writing loops.",
    },
    "Data Visualization": {
        "aliases": ["data visualization", "data visualisation", "matplotlib",
                    "seaborn", "plotly", "tableau", "power bi", "powerbi"],
        "category": "Data",
        "learn": "Matplotlib plus seaborn is enough. Learn when a chart type is wrong, not just how to draw it.",
    },
    "Statistics": {
        "aliases": ["statistics", "statistical analysis", "hypothesis testing",
                    "a/b testing", "ab testing", "regression analysis"],
        "category": "Data",
        "learn": "Hypothesis testing and confidence intervals. Most interviews probe this and most candidates are weak on it.",
    },
    "Data Cleaning": {
        "aliases": ["data cleaning", "data wrangling", "etl", "data preprocessing",
                    "feature engineering"],
        "category": "Data",
        "learn": "Take a deliberately messy public dataset and clean it. Document every decision you make.",
    },
    "Big Data": {
        "aliases": ["big data", "spark", "pyspark", "hadoop", "databricks"],
        "category": "Data",
        "learn": "Only matters if the role mentions scale. PySpark basics are enough for most job ads.",
    },
    "Web Scraping": {
        "aliases": ["web scraping", "beautifulsoup", "scrapy", "selenium",
                    "playwright"],
        "category": "Data",
        "learn": "Build your own dataset from a live site. Shows you can work without a clean CSV handed to you.",
    },

    # ---------------- Engineering ----------------
    "Git": {
        "aliases": ["git", "github", "gitlab", "version control"],
        "category": "Engineering",
        "learn": "Branching, pull requests and resolving a merge conflict. Expected in every role.",
    },
    "Docker": {
        "aliases": ["docker", "container", "containerization"],
        "category": "Engineering",
        "learn": "Containerize one of your projects. A Dockerfile in a student repo is genuinely uncommon.",
    },
    "APIs": {
        "aliases": ["api", "rest api", "fastapi", "flask", "django"],
        "category": "Engineering",
        "learn": "Wrap a model in FastAPI. It turns a notebook into something another person can use.",
    },
    "Cloud": {
        "aliases": ["aws", "azure", "gcp", "google cloud", "sagemaker",
                    "cloud computing"],
        "category": "Engineering",
        "learn": "Pick one provider. Free-tier deployment of a small app is enough to list it honestly.",
    },
    "Streamlit": {
        "aliases": ["streamlit", "gradio", "dash"],
        "category": "Engineering",
        "learn": "Fastest way to turn a model into something clickable. A weekend to learn.",
    },
    "Linux": {
        "aliases": ["linux", "bash", "shell scripting", "unix"],
        "category": "Engineering",
        "learn": "Navigating a filesystem, pipes, and running scripts on a remote machine.",
    },

    # ---------------- Working ----------------
    "Communication": {
        "aliases": ["communication", "presentation", "stakeholder",
                    "cross-functional", "documentation"],
        "category": "Working",
        "learn": "Write up one project as if explaining it to a non-technical manager.",
    },
    "Agile": {
        "aliases": ["agile", "scrum", "kanban", "jira", "sprint"],
        "category": "Working",
        "learn": "Familiarity is enough. Mention it if you've worked in sprints on a team project.",
    },
    "Problem Solving": {
        "aliases": ["problem solving", "analytical thinking", "critical thinking"],
        "category": "Working",
        "learn": "Shown through projects, not claimed in a skills list.",
    },
}


# Skills worth flagging as high-leverage when missing: rare in student
# resumes, common in job ads.
HIGH_LEVERAGE = {"MLOps", "Docker", "APIs", "Cloud", "SQL", "LLMs", "Big Data"}


def all_skill_names():
    return list(SKILLS.keys())


def category_of(skill):
    return SKILLS.get(skill, {}).get("category", "Other")


def learning_note(skill):
    return SKILLS.get(skill, {}).get("learn", "")
