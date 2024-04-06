import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
anthropic_key = os.getenv("anthropic_key")


class LLMClient:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def create_message(self, content, max_tokens=1024, model="claude-3-opus-20240229"):
        try:
            message = self.client.messages.create(
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": content}],
                model=model,
            )
            return message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


# Usage example, now encapsulated in a class
if __name__ == "__main__":
    llm_client = LLMClient(api_key=anthropic_key)
    message_content = llm_client.create_message("Hello, Claude")
    print(message_content)
