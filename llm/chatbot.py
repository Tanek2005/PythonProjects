import os
from langchain_google_genai import ChatGoogleGenerativeAI

def main():
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDBZsUXvuiI8VbNJCtq7u7xacpQcFKXZD0"
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    while True:
        prompt = input("You: ")
        if prompt.lower() == 'exit':
            break
        response = llm.invoke(prompt)
        print(f"AI: {response.content}")

if __name__ == "__main__":
    main()
