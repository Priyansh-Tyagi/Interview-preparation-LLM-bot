# This is a simple launcher script that runs the application
# You can use this if you prefer to keep your app structure modular

from app import demo

if __name__ == "__main__":
    print("Starting Interview Preparation LLM Bot...")
    print("Opening browser interface...")
    demo.launch(share=False)  # Set share=True if you want to create a public link