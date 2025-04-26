import gradio as gr
import requests
import time
from datetime import datetime
from question_banks import questions
from llm_handler import evaluate_answer
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
    questions_list = questions[role][domain][interview_type][:num_questions]
    
    # Initialize session data
    session_data = {
        "role": role,
        "domain": domain,
        "interview_type": interview_type,
        "questions": questions_list,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    interview_history.append(session_data)
    
    # Return first question
    if questions_list:
        return questions_list[0], "", "", gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)
    else:
        return "No questions available for this combination. Please try different options.", "", "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

def submit_answer_handler(role, domain, interview_type, state):
    # Debugging: Print the current state and inputs
    print(f"Role: {role}, Domain: {domain}, Interview Type: {interview_type}")
    print(f"Current answered_questions index: {state['answered_questions']}")

    # Ensure answered_questions index is incremented correctly
    current_question_index = state["answered_questions"]

    # Increment the index after answering a question
    state["answered_questions"] = current_question_index + 1
    print(f"New answered_questions index: {state['answered_questions']}")

    # Normalize role (capitalizing the first letter of each word)
    normalized_role = role.strip().title()

    # Check if the role exists in the questions dictionary
    if normalized_role not in questions:
        return f"Role '{normalized_role}' not found in the question bank."

    # Check if the domain and interview_type exist for the role
    if domain not in questions[normalized_role]:
        return f"Domain '{domain}' not found for role '{normalized_role}'."
    if interview_type not in questions[normalized_role][domain]:
        return f"Interview type '{interview_type}' not found for domain '{domain}' in role '{normalized_role}'."

    try:
        # Fetch the next question based on the incremented index
        next_question = questions[normalized_role][domain][interview_type][state["answered_questions"]]

        # Check if we have exceeded the number of available questions
        if next_question is None:  # Or any other condition for boundary checking
            return "No more questions available."

        return next_question  # Return the next question
    except KeyError:
        return "Invalid combination of inputs."


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


        def start_interview_handler(role, domain, interview_type, state):
            # Ensure state is always a dictionary
            if not isinstance(state, dict):
                state = {}  # Initialize an empty dictionary if state is not a dictionary

            # Normalize role input (capitalize for matching)
            normalized_role = role.strip().title()

            # Define the API URL (replace with your actual API endpoint)
            api_url = "https://yourapi.com/interview_questions"

            # Prepare parameters for the API call
            params = {
                "role": normalized_role,
                "domain": domain,
                "interview_type": interview_type
            }

            try:
                # Call the API to get the questions based on role, domain, and interview type
                response = requests.get(api_url, params=params)
                
                # Print out the raw response for debugging
                print(f"API Response: {response.text}")

                # Check if the response is valid
                if response.status_code != 200:
                    return (
                        f"Error: Unable to fetch interview questions. Status code: {response.status_code}.",  # Markdown 1
                        "",  # Placeholder for second markdown
                        state,  # Return the current state (updated or unchanged)
                        ""  # Placeholder for the last markdown
                    )
                
                # Try to parse the response JSON
                interview_data = response.json()

                # Check if we received valid questions data
                if not interview_data or "questions" not in interview_data:
                    return (
                        "No interview questions found for the specified role, domain, and interview type.",  # Markdown 1
                        "",  # Placeholder for second markdown
                        state,  # Return the current state (updated or unchanged)
                        ""  # Placeholder for the last markdown
                    )

                # Get the list of questions
                questions_list = interview_data["questions"]
                
                current_question_index = state.get("answered_questions", 0)
                
                if current_question_index >= len(questions_list):
                    return (
                        "No more questions available.",  # Markdown 1
                        "",  # Placeholder for second markdown
                        state,  # State remains unchanged
                        ""  # Placeholder for the last markdown
                    )

                # Otherwise, return the next question along with the updated state
                next_question = questions_list[current_question_index]
                
                state["answered_questions"] = current_question_index + 1  # Increment question index
                
                return (
                    next_question,  # Markdown 1: The next question
                    "",  # Placeholder for second markdown
                    state,  # Updated state
                    ""  # Placeholder for the last markdown
                )

            except Exception as e:
                return (
                    f"Error: An unexpected error occurred while fetching interview questions. {str(e)}",  # Markdown 1
                    "",  # Placeholder for second markdown
                    state,  # Return the current state (updated or unchanged)
                    ""  # Placeholder for the last markdown
                )



        

        def submit_answer_handler(answer, role, domain, interview_type, difficulty, state):
            if not answer:
                answer = "SKIPPED"
            
            feedback, score = evaluate_answer(role, domain, interview_type, state['current_question'], answer)
            time_taken = int(time.time() - state['start_time'])

            # Update state after answering
            state["answered_questions"] += 1

            # Prepare next question (if there are more)
            if state["answered_questions"] < state["total_questions"]:
                next_question = questions[role][domain][interview_type][state["answered_questions"]]
                next_question_number = state["answered_questions"] + 1
                progress = f"Progress: {next_question_number}/{state['total_questions']} 📈"
                question_text = f"### Question {next_question_number}: {next_question}"
                motivational = ""
            else:
                next_question = ""
                question_text = "🎉 Interview Completed!"
                progress = "✅ All Questions Answered!"
                motivational = "Good Job! 🚀 Stay awesome!"

            # Update state
            state.update({
                "current_question": next_question,
                "current_question_number": state["answered_questions"] + 1,
                "start_time": time.time()
            })

            # Display feedback only after all questions are answered
            if state["answered_questions"] == state["total_questions"]:
                return {
                    feedback_display: f"### Feedback:\n{feedback}",
                    score_display: f"### Score: {score}/10",
                    timer_display: f"⏱ Time Taken: {time_taken} seconds",
                    question_display: question_text,
                    progress_display: progress,
                    motivational_message: motivational,
                    state: state
                }

            return {
                question_display: question_text,
                progress_display: progress,
                timer_display: f"⏱ Time Taken: {time_taken} seconds",
                state: state
            }

        # Event Bindings
        start_button.click(
            start_interview_handler,
            inputs=[role, domain, interview_type, difficulty],
            outputs=[question_display, progress_display, state, motivational_message]
        )

        submit_button.click(
            submit_answer_handler,
            inputs=[answer_box, role, domain, interview_type, difficulty, state],
            outputs=[feedback_display, score_display, timer_display, question_display, progress_display, motivational_message, state]
        )

    return demo

if __name__ == "__main__":
    ui = create_ui()
    ui.launch(share=True)
