# utils.py
import json
import os
from datetime import datetime

def generate_report(session_data, answers, feedback, scores):
    """Generate a comprehensive report of the interview session"""
    
    # Calculate average score
    valid_scores = [s for s in scores if s > 0]  # Filter out skipped questions
    avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
    
    # Identify strengths and weaknesses
    strengths = []
    weaknesses = []
    
    # This is simplified - in a real app, you would use the LLM to analyze feedback
    if avg_score >= 8:
        strengths.append("Strong technical knowledge")
        strengths.append("Clear communication")
    elif avg_score >= 6:
        strengths.append("Good foundational knowledge")
        weaknesses.append("Could improve depth in certain areas")
    else:
        weaknesses.append("Needs to strengthen technical knowledge")
        weaknesses.append("Could improve answer structure")
    
    # Generate report
    report = f"""
    # Interview Report

    ## Session Summary
    - Role: {session_data['role']}
    - Domain: {session_data['domain']}
    - Interview Type: {session_data['interview_type']}
    - Date: {session_data['start_time']}

    ## Performance
    - Questions Attempted: {len(answers)}
    - Average Score: {avg_score:.1f}/10

    ## Strengths
    {chr(10).join('- ' + s for s in strengths)}

    ## Areas for Improvement
    {chr(10).join('- ' + w for w in weaknesses)}

    ## Question Breakdown
    """
    
    for i, (question, answer, fb, score) in enumerate(zip(session_data['questions'], answers, feedback, scores)):
        report += f"""
    ### Question {i+1}: {question}
    - Your Answer: {"[SKIPPED]" if answer == "SKIPPED" else answer}
    - Score: {score}/10
    - Feedback: {fb}
    """
    
    report += """
    ## Resources for Improvement
    - [Technical Interview Handbook](https://www.techinterviewhandbook.org/)
    - [Cracking the Coding Interview](https://www.crackingthecodinginterview.com/)
    - [Grokking the System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)
    """
    
    return report

def save_session(session_data, answers, feedback, scores, report):
    """Save the interview session for future reference"""
    
    # Create directory if it doesn't exist
    if not os.path.exists("interview_sessions"):
        os.makedirs("interview_sessions")
    
    # Create a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"interview_sessions/session_{timestamp}.json"
    
    # Prepare data
    session_record = {
        "session_info": session_data,
        "answers": answers,
        "feedback": feedback,
        "scores": scores,
        "report": report
    }
    
    # Save to file
    try:
        with open(filename, "w") as f:
            json.dump(session_record, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving session: {str(e)}")
        return False

