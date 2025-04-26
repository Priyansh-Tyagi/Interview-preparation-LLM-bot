import json
import os
import time
from typing import List, Tuple, Dict, Any, Optional

def load_previous_interview(filename: str) -> Tuple[List[List[str]], str]:
    """
    Load a previously saved interview from a file
    
    Args:
        filename: Path to the saved interview JSON file
        
    Returns:
        Tuple containing the chat history and job role
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            
        chat_history = data.get('conversation', [])
        job_role = data.get('job_role', '')
        
        return chat_history, job_role
    except Exception as e:
        print(f"Error loading interview: {e}")
        return [], ""

def get_saved_interviews() -> List[Dict[str, Any]]:
    """
    Get a list of all saved interviews
    
    Returns:
        List of dictionaries containing interview metadata
    """
    saved_dir = "saved_interviews"
    if not os.path.exists(saved_dir):
        return []
        
    interviews = []
    for filename in os.listdir(saved_dir):
        if filename.endswith('.json'):
            try:
                filepath = os.path.join(saved_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                # Extract metadata
                interviews.append({
                    'filename': filepath,
                    'job_role': data.get('job_role', 'Unknown'),
                    'timestamp': data.get('timestamp', ''),
                    'question_count': len(data.get('conversation', []))
                })
            except Exception:
                continue
    
    # Sort by timestamp, newest first
    interviews.sort(key=lambda x: x['timestamp'], reverse=True)
    return interviews

def get_interview_questions_by_role(role: str) -> List[str]:
    """
    Get sample interview questions for a specific job role
    
    Args:
        role: The job role to get questions for
        
    Returns:
        List of interview questions
    """
    # Generic questions for any role
    generic_questions = [
        "Tell me about yourself.",
        "What are your greatest strengths?",
        "What do you consider to be your weaknesses?",
        "Why are you interested in working for our company?",
        "Where do you see yourself in 5 years?",
        "Why should we hire you?",
        "How do you handle stress and pressure?",
        "Describe a difficult work situation and how you overcame it."
    ]
    
    # Role-specific questions
    role_specific = {
        "software engineer": [
            "Explain the difference between an array and a linked list.",
            "What is your experience with agile development?",
            "Describe a challenging programming problem you've solved.",
            "How do you ensure your code is maintainable and scalable?",
            "What programming languages are you proficient in?"
        ],
        "data scientist": [
            "Explain the difference between supervised and unsupervised learning.",
            "How do you handle missing data in a dataset?",
            "What techniques do you use for feature selection?",
            "Describe a data science project you've worked on.",
            "How do you communicate technical findings to non-technical stakeholders?"
        ],
        "product manager": [
            "How do you prioritize features for a product?",
            "Describe how you would launch a new product.",
            "How do you gather and incorporate user feedback?",
            "Tell me about a time you had to make a difficult product decision.",
            "How do you measure product success?"
        ]
    }
    
    # Check if we have specific questions for this role
    role_lower = role.lower()
    questions = generic_questions.copy()
    
    for key, specific_questions in role_specific.items():
        if key in role_lower:
            questions.extend(specific_questions)
            break
    
    return questions