import gradio as gr
import time
import json
from datetime import datetime
import random
from llm_handler import get_llm_response, evaluate_answer
from question_banks import questions
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
    questions = questions(role, domain, interview_type, num_questions)
    
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

import gradio as gr
import time

import gradio as gr
import time

import gradio as gr
import time

def create_ui():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:  # Lighter and modern color palette
        gr.Markdown("# 🎯 Interview Preparation Bot")
        gr.Markdown("Practice job interview questions with instant AI feedback!")

        # Define the row for the input fields
        with gr.Row():
            role = gr.Textbox(label="Role (e.g., Software Engineer)", placeholder="e.g., Software Engineer")
            domain = gr.Dropdown(
                choices=["Web Development", "Machine Learning", "System Design", "Data Science"],
                label="Domain",
                value="Web Development",
                interactive=True
            )

        # Dropdowns for interview type and difficulty
        with gr.Row():
            interview_type = gr.Dropdown(
                choices=["Behavioral", "Technical"], label="Interview Type", value="Technical"
            )
            difficulty = gr.Dropdown(
                choices=["Easy", "Medium", "Hard"], label="Difficulty", value="Medium"
            )

        start_button = gr.Button("Start Interview 🚀", variant="primary")

        # Display area for questions, feedback, score, etc.
        question_display = gr.Markdown("")  # Question Display
        answer_box = gr.Textbox(label="Your Answer", placeholder="Type your answer here...")
        submit_button = gr.Button("Submit Answer ✅")

        # Feedback, score, and progress display
        feedback_display = gr.Markdown("")  # For feedback (to be shown later)
        score_display = gr.Markdown("")  # For score (to be shown later)
        timer_display = gr.Markdown("")  # Timer display
        progress_display = gr.Markdown("")  # Progress display (e.g., Question 1 of 5)

        motivational_message = gr.Markdown("")  # Motivational message at the end

        # State variable to track progress
        state = gr.State({
            "current_question": "",
            "current_question_number": 0,
            "total_questions": 5,
            "start_time": None,
            "answered_questions": 0,  # Number of answered questions
            "correct_answers": 0
        })

        # Functions
        def start_interview(role, domain, interview_type, difficulty):
            first_question = generate_question(role, domain, interview_type, difficulty)
            return {
                question_display: f"### Question 1: {first_question}",
                progress_display: f"Progress: 1/5 📈",
                state: {
                    "current_question": first_question,
                    "current_question_number": 1,
                    "total_questions": 5,
                    "start_time": time.time(),
                    "answered_questions": 0,
                    "correct_answers": 0
                },
                motivational_message: ""
            }

        def submit_answer(answer, role, domain, interview_type, difficulty, data):
            if not answer:
                answer = "SKIPPED"
            
            feedback, score = evaluate_answer(role, domain, interview_type, data['current_question'], answer)
            time_taken = int(time.time() - data['start_time'])

            # Update state after answering
            data["answered_questions"] += 1

            # Prepare next question (if there are more)
            if data["answered_questions"] < data["total_questions"]:
                next_question = generate_question(role, domain, interview_type, difficulty)
                next_question_number = data["answered_questions"] + 1
                progress = f"Progress: {next_question_number}/5 📈"
                question_text = f"### Question {next_question_number}: {next_question}"
                motivational = ""
            else:
                next_question = ""
                question_text = "🎉 Interview Completed!"
                progress = "✅ All Questions Answered!"
                motivational = "Good Job! 🚀 Stay awesome!"

            # Update state
            data.update({
                "current_question": next_question,
                "current_question_number": data["answered_questions"] + 1,
                "start_time": time.time()
            })

            # Display feedback only after all questions are answered
            if data["answered_questions"] == data["total_questions"]:
                return {
                    feedback_display: f"### Feedback:\n{feedback}",
                    score_display: f"### Score: {score}/10",
                    timer_display: f"⏱ Time Taken: {time_taken} seconds",
                    question_display: question_text,
                    progress_display: progress,
                    motivational_message: motivational,
                    state: data
                }

            return {
                question_display: question_text,
                progress_display: progress,
                timer_display: f"⏱ Time Taken: {time_taken} seconds",
                state: data
            }

        # Event Bindings
        start_button.click(
            start_interview,
            inputs=[role, domain, interview_type, difficulty],
            outputs=[question_display, progress_display, state, motivational_message]
        )

        submit_button.click(
            submit_answer,
            inputs=[answer_box, role, domain, interview_type, difficulty, state],
            outputs=[feedback_display, score_display, timer_display, question_display, progress_display, motivational_message, state]
        )

    return demo

if __name__ == "__main__":
    ui = create_ui()
    ui.launch(share=True)