import random

career_prompts = {
    "frontend": [
        "Build a responsive personal portfolio using HTML, CSS, and React.",
        "Create a weather app using a public API and display live data.",
        "Design an interactive landing page using Tailwind CSS and animations.",
        "Implement a dark mode toggle with React state management.",
        "Develop a simple to-do app with local storage functionality."
    ],
    "ai": [
        "Design a chatbot using OpenAI API or LangChain.",
        "Build a resume analyzer using NLP and Python.",
        "Create a prompt engineering project that auto-generates AI study plans.",
        "Develop an AI model that summarizes news articles.",
        "Make a voice-controlled assistant using speech recognition and GPT."
    ],
    "data": [
        "Analyze sales data and create a dashboard using Power BI or Streamlit.",
        "Predict house prices using linear regression and Python.",
        "Clean and visualize large datasets using Pandas and Matplotlib.",
        "Build a student performance prediction model using scikit-learn.",
        "Create a data visualization project with interactive charts."
    ],
    "default": [
        "Write 5 creative prompts to improve learning in your domain.",
        "Generate a daily motivation prompt related to your field.",
        "Suggest project ideas that strengthen your portfolio."
    ]
}

def generate_prompt(career_goal, number=3):
    """Generate prompts based on the entered career goal."""
    goal = career_goal.lower()

    if "frontend" in goal or "web" in goal:
        prompts = career_prompts["frontend"]
    elif "ai" in goal or "prompt" in goal or "ml" in goal:
        prompts = career_prompts["ai"]
    elif "data" in goal or "analytics" in goal:
        prompts = career_prompts["data"]
    else:
        prompts = career_prompts["default"]

    return random.sample(prompts, k=min(number, len(prompts)))
