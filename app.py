import gradio as gr
import time
import json
from datetime import datetime
import random
from llm_handler import get_llm_response, evaluate_answer
from question_banks import get_questions
from utils import generate_report, save_session

# Global variables to track session state
current_question_index = 0
interview_history = []
user_answers = []
feedback_history = []
scores = []

def start_interview(role, domain, interview_type, num_questions=3):
    """Initialize a new interview session"""
    global current_question_index, interview_history, user_answers, feedback_history, scores
    
    # Reset session variables
    current_question_index = 0
    interview_history = []
    user_answers = []
    feedback_history = []
    scores = []
    
    # Get questions based on role, domain and interview type
    questions = get_questions(role, domain, interview_type, num_questions)
    
    # Initialize session data
    session_data = {
        "role": role,
        "domain": domain,
        "interview_type": interview_type,
        "questions": questions,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    interview_history.append(session_data)
    
    # Return first question
    if questions:
        return questions[0], "", "", gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    else:
        return "No questions available for this combination. Please try different options.", "", "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

def submit_answer(role, domain, interview_type, question, answer):
    """Process user's answer and provide feedback"""
    global current_question_index, user_answers, feedback_history, scores, interview_history
    
    if not interview_history:
        return question, "Please start an interview first.", "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
    
    # Save the answer
    user_answers.append(answer)
    
    # Get feedback from LLM
    feedback, score = evaluate_answer(role, domain, interview_type, question, answer)
    feedback_history.append(feedback)
    scores.append(score)
    
    questions = interview_history[0]["questions"]
    
    # Check if we have more questions
    current_question_index += 1
    
    if current_question_index < len(questions):
        next_question = questions[current_question_index]
        return next_question, feedback, f"Score: {score}/10", gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)
    else:
        # End of interview
        report = generate_report(interview_history[0], user_answers, feedback_history, scores)
        save_session(interview_history[0], user_answers, feedback_history, scores, report)
        return "", feedback, f"Score: {score}/10", gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

def retry_question():
    """Allow user to retry the current question"""
    global current_question_index, interview_history
    
    if not interview_history:
        return "Please start an interview first.", "", "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
    
    # Go back to current question (don't increment)
    questions = interview_history[0]["questions"]
    
    if 0 <= current_question_index < len(questions):
        return questions[current_question_index], "", "", gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    else:
        return "No current question to retry.", "", "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

def skip_question(role, domain, interview_type):
    """Skip the current question"""
    global current_question_index, interview_history, user_answers, feedback_history, scores
    
    if not interview_history:
        return "Please start an interview first.", "", "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
    
    # Add empty records for skipped question
    user_answers.append("SKIPPED")
    feedback_history.append("Question was skipped.")
    scores.append(0)
    
    # Increment to next question
    current_question_index += 1
    questions = interview_history[0]["questions"]
    
    if current_question_index < len(questions):
        next_question = questions[current_question_index]
        return next_question, "Question skipped.", "", gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    else:
        # End of interview
        report = generate_report(interview_history[0], user_answers, feedback_history, scores)
        save_session(interview_history[0], user_answers, feedback_history, scores, report)
        return "", "Interview complete.", "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

def view_report():
    """Display the final interview report"""
    if not interview_history or len(user_answers) == 0:
        return "No completed interview to report."
    
    report = generate_report(interview_history[0], user_answers, feedback_history, scores)
    return report

def create_ui():
    """Create the Gradio interface"""
    with gr.Blocks(theme=gr.themes.Soft(), css="""
        .container {max-width: 800px; margin: auto;}
        .header {text-align: center; margin-bottom: 20px;}
        .feedback-box {background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-top: 10px;}
        .score-box {font-weight: bold; margin-top: 10px;}
    """) as app:
        gr.Markdown("# Interview Preparation Bot")
        gr.Markdown("Practice your interview skills with AI feedback")
        
        with gr.Tab("Setup Interview"):
            with gr.Row():
                with gr.Column():
                    role = gr.Dropdown(
                        choices=["Software Engineer", "Data Scientist", "Product Manager", "UX Designer", "DevOps Engineer"],
                        label="Select Job Role",
                        value="Software Engineer"
                    )
                    domain = gr.Dropdown(
                        choices=["frontend", "backend", "full-stack", "machine learning", "system design", "general"],
                        label="Select Domain (Optional)",
                        value="general"
                    )
                    
                with gr.Column():
                    interview_type = gr.Radio(
                        choices=["technical", "behavioral"],
                        label="Interview Type",
                        value="technical"
                    )
                    num_questions = gr.Slider(
                        minimum=1,
                        maximum=5,
                        value=3,
                        step=1,
                        label="Number of Questions"
                    )
                    
            start_btn = gr.Button("Start Interview", variant="primary")
        
        with gr.Tab("Interview Session"):
            with gr.Row():
                with gr.Column():
                    question_box = gr.Textbox(label="Question", lines=3, interactive=False)
                    answer_box = gr.Textbox(label="Your Answer", lines=5, placeholder="Type your answer here...")
                    
                    with gr.Row():
                        submit_btn = gr.Button("Submit Answer", variant="primary", visible=False)
                        retry_btn = gr.Button("Retry Question", visible=False)
                        skip_btn = gr.Button("Skip Question", visible=False)
                    
                with gr.Column():
                    feedback_box = gr.Textbox(label="Feedback", lines=5, interactive=False)
                    score_box = gr.Textbox(label="Score", interactive=False)
            
            report_btn = gr.Button("View Final Report", visible=False)
            report_output = gr.Textbox(label="Interview Report", lines=10, interactive=False)
        
        # Event handlers
        start_btn.click(
            start_interview,
            inputs=[role, domain, interview_type, num_questions],
            outputs=[question_box, feedback_box, score_box, submit_btn, retry_btn, skip_btn]
        )
        
        submit_btn.click(
            submit_answer,
            inputs=[role, domain, interview_type, question_box, answer_box],
            outputs=[question_box, feedback_box, score_box, submit_btn, retry_btn, report_btn]
        )
        
        retry_btn.click(
            retry_question,
            inputs=[],
            outputs=[question_box, feedback_box, score_box, submit_btn, retry_btn, report_btn]
        )
        
        skip_btn.click(
            skip_question,
            inputs=[role, domain, interview_type],
            outputs=[question_box, feedback_box, score_box, submit_btn, skip_btn, report_btn]
        )
        
        report_btn.click(
            view_report,
            inputs=[],
            outputs=[report_output]
        )
        
    return app

if __name__ == "__main__":
    ui = create_ui()
    ui.launch()