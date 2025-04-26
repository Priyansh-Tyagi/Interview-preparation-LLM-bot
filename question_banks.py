# question_banks.py
def get_questions(role, domain, interview_type, num_questions=3):
    """
    Return questions based on job role, domain, and interview type
    In a real implementation, this would be more extensive
    """
    question_banks = {
        "technical": {
            "Software Engineer": {
                "frontend": [
                    "Explain the difference between local storage and session storage in browsers.",
                    "What is the virtual DOM in React and why is it beneficial?",
                    "How would you optimize website loading performance?",
                    "Explain the concept of CSS BEM methodology.",
                    "How does the JavaScript event loop work?"
                ],
                "backend": [
                    "Explain RESTful API design principles.",
                    "How would you handle database migrations in a production environment?",
                    "Compare SQL and NoSQL databases and when to use each.",
                    "How would you implement authentication and authorization in a web application?",
                    "Explain the concept of microservices architecture."
                ],
                "general": [
                    "Explain the concept of time complexity and give examples.",
                    "How would you approach debugging a complex issue in production?",
                    "Explain the principle of SOLID in object-oriented programming.",
                    "What strategies do you use for testing your code?",
                    "How do you stay current with new technologies in your field?"
                ]
            },
            "Data Scientist": {
                "machine learning": [
                    "Explain the difference between supervised and unsupervised learning.",
                    "How would you handle imbalanced data in a classification problem?",
                    "Explain the concept of overfitting and how to prevent it.",
                    "How would you evaluate a regression model?",
                    "Explain the concept of feature engineering."
                ],
                "general": [
                    "Describe a data cleaning process you've used in the past.",
                    "How would you explain a complex algorithm to a non-technical stakeholder?",
                    "What steps would you take to handle missing data?",
                    "Explain the concept of A/B testing.",
                    "How do you approach data visualization?"
                ]
            }
        },
        "behavioral": {
            "Software Engineer": {
                "general": [
                    "Tell me about a time you had to learn a new technology quickly for a project.",
                    "Describe a situation where you had to resolve a conflict in a team.",
                    "Tell me about a project you're particularly proud of and your contribution.",
                    "How do you handle tight deadlines and pressure?",
                    "Describe a time when you had to make a difficult technical decision."
                ]
            },
            "Data Scientist": {
                "general": [
                    "Tell me about a data analysis project that had a significant impact on the business.",
                    "Describe a situation where your analysis led to an unexpected insight.",
                    "How do you communicate technical findings to non-technical stakeholders?",
                    "Tell me about a time when you had to adjust your analysis based on feedback.",
                    "Describe a situation where you had to work with incomplete or messy data."
                ]
            },
            "Product Manager": {
                "general": [
                    "Tell me about a time when you had to prioritize features for a product.",
                    "Describe a situation where you had to make a decision based on limited data.",
                    "How do you handle stakeholder disagreements?",
                    "Tell me about a product launch that didn't go as planned and what you learned.",
                    "How do you gather and incorporate user feedback into product development?"
                ]
            }
        }
    }
    
    # Add more general questions for roles that might not have specific ones
    for interview_t in question_banks:
        for r in question_banks[interview_t]:
            if "general" not in question_banks[interview_t][r]:
                question_banks[interview_t][r]["general"] = [
                    f"Generic {interview_t} question 1 for {r}",
                    f"Generic {interview_t} question 2 for {r}",
                    f"Generic {interview_t} question 3 for {r}",
                    f"Generic {interview_t} question 4 for {r}",
                    f"Generic {interview_t} question 5 for {r}"
                ]
    
    # Get questions based on selected options
    try:
        if role in question_banks[interview_type]:
            if domain in question_banks[interview_type][role]:
                questions = question_banks[interview_type][role][domain]
            else:
                questions = question_banks[interview_type][role]["general"]
        else:
            # If specific role not found, return generic questions
            questions = [
                f"Generic {interview_type} question 1 for {role}",
                f"Generic {interview_type} question 2 for {role}",
                f"Generic {interview_type} question 3 for {role}",
                f"Generic {interview_type} question 4 for {role}",
                f"Generic {interview_type} question 5 for {role}"
            ]
    except KeyError:
        questions = [
            f"Generic {interview_type} question 1 for {role}",
            f"Generic {interview_type} question 2 for {role}",
            f"Generic {interview_type} question 3 for {role}",
            f"Generic {interview_type} question 4 for {role}",
            f"Generic {interview_type} question 5 for {role}"
        ]
    
    # Select the requested number of questions
    if num_questions < len(questions):
        return random.sample(questions, num_questions)
    else:
        return questions
