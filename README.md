This is Interview prepration chatbot.

🧠 Interview Preparation LLM Bot
AI-powered Interview Coach
Built for the [Hackathon Name] 2025 🚀

✨ Overview
The Interview Preparation LLM Bot is an intelligent assistant designed to help candidates prepare for technical, behavioral, and HR interviews.
It uses the power of OpenAI’s GPT models to generate questions, evaluate answers, and give personalized, detailed feedback — just like a real interviewer!

✅ Real-time feedback
✅ Scored evaluation
✅ Multiple interview types
✅ Interactive, simple, and fast UI

🛠️ Built With
🐍 Python 3.10+

🎨 Gradio (for web-based UI)

🧠 OpenAI API (for question answering and evaluation)

📦 dotenv (for environment variable management)

🎯 Features

Feature	Description
🎯 Personalized Interview Questions: 	Choose domain, role, and interview type
📋 Answer Evaluation: 	Immediate feedback on correctness, clarity, structure
📈 Scoring System	:  Answer rated on a scale of 1–10
🚀 Simple and Responsive:  UI	Powered by Gradio
🔐 Secure API Key Handling: 	Using .env file (no keys exposed)

🚀 How to Run Locally
Clone the repository:
  bash
    git clone https://github.com/Priyansh-Tyagi/Interview-preparation-LLM-bot.git
    cd Interview-preparation-LLM-bot
  
Create and activate a virtual environment (optional but recommended):
    python -m venv venv
    source venv/bin/activate      # Linux/Mac
    venv\Scripts\activate         # Windows
    
Install dependencies:
  pip install -r requirements.txt

Create a .env file: Inside the project root directory, create a .env file and add your OpenAI API key:
  ini
  OPENAI_API_KEY=your-api-key-here

Run the app:
  python app.py

Access the app:
The app will open automatically in your browser at http://127.0.0.1:7860/
Or it will provide a public link if you run with share=True.

🎥 Demo (Optional)
(Add a GIF or screenshot showing the bot in action here if you want extra points in hackathon!)
Example: User selecting role ➔ typing answer ➔ getting feedback.

📦 Folder Structure
graphql
Copy
Edit
Interview-preparation-LLM-bot/
│
├── app.py                # Main UI file
├── llm_handler.py         # Logic for OpenAI API calls and evaluations
├── .env                   # (your API key, NOT pushed to GitHub)
├── requirements.txt       # Python libraries needed
└── README.md              # This file


📈 Future Enhancements (Post Hackathon)
✨ Support multiple rounds of interviews

✨ Add difficulty levels (Easy / Medium / Hard)

✨ Topic-specific interview modes (DSA, ML, Web Dev, System Design)

✨ Save interview session history

✨ Deploy on HuggingFace Spaces / Render

🤝 Team
👤 Priyansh Tyagi

GitHub: @Priyansh-Tyagi

📜 License
This project is licensed under the MIT License.

🔥 Ready to Ace Your Next Interview with AI!
Let's go! 🚀
