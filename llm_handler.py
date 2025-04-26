import os
import openai
import random

# Load local question_bank for demo
from question_banks import questions

# Set up environment variables and OpenAI client
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_question(role, domain, interview_type, difficulty, topic):
    """
    Pick a random question based on topic and difficulty.
    If unavailable, fallback to LLM.
    """
    # Fetch questions based on the topic and difficulty from the question bank
    topic_data = questions.get(topic, {})
    difficulty_questions = topic_data.get(difficulty, [])
    
    # If questions are found for the given difficulty, return a random one
    if difficulty_questions:
        return random.choice(difficulty_questions)
    else:
        # If no questions are found, generate a question via LLM
        prompt = f"Generate a {difficulty} level {topic} interview question for a {role} in a {domain} {interview_type} interview."
        return get_llm_response(prompt)


def get_llm_response(prompt, max_tokens=500):
    """Generate a response using OpenAI API."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert interviewer helping candidates prepare for job interviews."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting LLM response: {str(e)}"

def evaluate_answer(role, domain, interview_type, question, answer):
    """Evaluate the user's answer and provide feedback"""
    if answer == "SKIPPED":
        return "Question was skipped.", 0
    
    prompt = f"""
    You are an expert {role} interviewer specializing in {domain} topics.
    
    The candidate is answering a {interview_type} interview question:
    
    Question: {question}
    
    Candidate's Answer: {answer}
    
    Please evaluate this answer based on the following criteria:
    1. Correctness: Is the answer technically accurate?
    2. Completeness: Does it cover all important aspects?
    3. Clarity: Is it well-articulated and easy to understand?
    4. Structure: Is the answer well-organized?
    
    First, provide constructive feedback (2-3 paragraphs).
    Then, rate the answer on a scale of 1-10.
    
    Format your response as:
    FEEDBACK: [Your feedback here]
    SCORE: [Score]/10
    """
    
    response = get_llm_response(prompt)
    
    # Parse response
    try:
        feedback_parts = response.split("SCORE:")
        
        if len(feedback_parts) > 1:
            feedback = feedback_parts[0].replace("FEEDBACK:", "").strip()
            score_str = feedback_parts[1].strip()
            score = int(score_str.split("/")[0])
        else:
            feedback = response
            score = 5  # Default score if parsing fails
            
        return feedback, score
    
    except Exception as e:
        feedback = (
            "Your answer demonstrates good knowledge of the topic. "
            "Consider adding more specific examples to strengthen your points. "
            "Also, try to structure your answer using the STAR method (Situation, Task, Action, Result) for clearer communication."
        )
        score = 7
        return feedback, score
