# llm_handler.py
import os
import openai
import json

#load env
from dotenv import load_dotenv
load_dotenv()

# Set up your API key (in production, use environment variables)
from openai import OpenAI

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_llm_response(prompt, max_tokens=500):
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

    
    # For demo purposes - in case you simulate the response without API (unreachable here now)
    # return "This is a simulated LLM response. In a real implementation, this would use an LLM API like OpenAI, Claude, or another model."

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
        # In case parsing fails badly, return a fallback
        feedback = (
            "Your answer demonstrates good knowledge of the topic. "
            "Consider adding more specific examples to strengthen your points. "
            "Also, try to structure your answer using the STAR method (Situation, Task, Action, Result) for clearer communication."
        )
        score = 7
        return feedback, score
