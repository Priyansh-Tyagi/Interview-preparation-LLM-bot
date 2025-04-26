import gradio as gr
import os
from openai import OpenAI  # Updated import
from dotenv import load_dotenv
import json
import time

# Load environment variables
load_dotenv()

# Configure OpenAI client - updated for v1.0+
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System message to define the interview bot behavior
SYSTEM_MESSAGE = """You are an AI interview preparation assistant specialized in helping candidates prepare for job interviews.
Your role is to:
1. Ask relevant interview questions based on the job role provided
2. Evaluate candidate responses
3. Provide constructive feedback on content, delivery, and confidence
4. Offer sample answers when appropriate
5. Give tips for improvement
6. Simulate a realistic interview experience

Maintain a professional but encouraging tone. Challenge the candidate with realistic questions without being too harsh in feedback."""

def generate_interview_response(message, chat_history, job_role):
    """Process user input and generate interview response based on job role"""
    if not os.getenv("OPENAI_API_KEY"):
        return "Error: OpenAI API key not found. Please check your .env file."
    
    try:
        # Format the chat history for the API
        formatted_history = []
        for user_msg, bot_msg in chat_history:
            formatted_history.append({"role": "user", "content": user_msg})
            if bot_msg:  # Only append if bot message exists
                formatted_history.append({"role": "assistant", "content": bot_msg})
        
        # Add system message with job role context
        context_message = SYSTEM_MESSAGE
        if job_role:
            context_message += f"\n\nThe candidate is preparing for a {job_role} position. Tailor your questions and feedback accordingly."
        
        # Prepare the messages for the API call
        messages = [
            {"role": "system", "content": context_message},
            *formatted_history,
            {"role": "user", "content": message}
        ]
        
        # Call the OpenAI API - updated for v1.0+
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        
        # Updated response access for v1.0+
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

def save_conversation(chat_history, job_role):
    """Save the conversation to a file"""
    if not chat_history:
        return "No conversation to save."
    
    # Create directory if it doesn't exist
    os.makedirs("saved_interviews", exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    role_slug = job_role.lower().replace(" ", "_") if job_role else "general"
    filename = f"saved_interviews/interview_{role_slug}_{timestamp}.json"
    
    # Format data for saving
    convo_data = {
        "job_role": job_role,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "conversation": chat_history
    }
    
    # Save to file
    with open(filename, "w") as f:
        json.dump(convo_data, f, indent=2)
    
    return f"Conversation saved to {filename}"

# Create the Gradio interface
with gr.Blocks(css="footer {visibility: hidden}") as demo:
    gr.Markdown("# 🤖 Interview Preparation Assistant")
    gr.Markdown("Practice for your job interviews with an AI assistant that provides feedback and guidance.")
    
    with gr.Row():
        with gr.Column(scale=3):
            job_role = gr.Textbox(
                label="Job Role/Position", 
                placeholder="E.g., Software Engineer, Product Manager, Data Scientist",
                info="Enter the job role you're interviewing for to get tailored questions"
            )
    
    chatbot = gr.Chatbot(
        label="Interview Simulation",
        height=500
    )
    
    with gr.Row():
        message = gr.Textbox(
            label="Your Response",
            placeholder="Type your answer here...",
            lines=3
        )
    
    with gr.Row():
        submit_btn = gr.Button("Submit", variant="primary")
        clear_btn = gr.Button("Clear Conversation")
        save_btn = gr.Button("Save Interview")
    
    save_output = gr.Textbox(label="Save Status", visible=False)
    
    def user(message, chat_history, job_role):
        # Return immediately to display user message
        return "", chat_history + [[message, None]], job_role
    
    def bot(chat_history, job_role):
        # Process the last user message
        user_message = chat_history[-1][0]
        bot_response = generate_interview_response(user_message, chat_history[:-1], job_role)
        chat_history[-1][1] = bot_response
        return chat_history
    
    # Handle initial greeting when job role is entered
    def start_interview(job_role, chat_history):
        if not job_role:
            return chat_history
        if not chat_history:  # Only trigger if chat is empty
            greeting = f"Hello! I'll be your interview preparation assistant for the {job_role} position. Let's start with a common question: Tell me about yourself and why you're interested in this role."
            return [[None, greeting]]
        return chat_history
    
    # Connect the components with their events
    job_role.change(
        start_interview,
        [job_role, chatbot],
        [chatbot]
    )
    
    submit_btn.click(
        user,
        [message, chatbot, job_role],
        [message, chatbot, job_role],
        queue=False
    ).then(
        bot,
        [chatbot, job_role],
        [chatbot]
    )
    
    message.submit(
        user,
        [message, chatbot, job_role],
        [message, chatbot, job_role],
        queue=False
    ).then(
        bot,
        [chatbot, job_role],
        [chatbot]
    )
    
    clear_btn.click(
        lambda: ([], ""),
        None,
        [chatbot, job_role]
    )
    
    save_btn.click(
        save_conversation,
        [chatbot, job_role],
        [save_output]
    ).then(
        lambda: gr.update(visible=True),
        None,
        [save_output]
    )

    # Example questions for different job roles
    with gr.Accordion("Example Questions to Ask", open=False):
        gr.Markdown("""
        - Tell me about your experience with [specific technology]
        - How do you handle tight deadlines?
        - Describe a challenging project you worked on
        - What are your strengths and weaknesses?
        - Why do you want to work for our company?
        - How do you stay updated with industry trends?
        """)

# Launch the app
if __name__ == "__main__":
    demo.launch()