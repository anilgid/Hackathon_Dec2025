import asyncio
from backend.services.llm_interface import LLMFactory, Message

class RootAgent:
    def __init__(self):
        # Initialize LLM interface from environment configuration
        try:
            self.llm = LLMFactory.create_llm()
            self.use_llm = True
        except (ValueError, ImportError) as e:
            print(f"Warning: Could not initialize LLM ({e}). Using dummy mode.")
            self.llm = None
            self.use_llm = False

    async def process_request(self, user_input: str) -> str:
        """
        Processes the user input and returns a response.
        Uses configured LLM if available, otherwise falls back to dummy mode.
        """
        if self.use_llm and self.llm:
            try:
                # Create message history for LLM
                messages = [
                    Message(role="system", content="You are a helpful AI assistant."),
                    Message(role="user", content=user_input)
                ]
                
                # Get LLM response
                response = await self.llm.generate_response(messages)
                return response
            except Exception as e:
                print(f"Error calling LLM: {e}")
                return f"Sorry, I encountered an error: {str(e)}"
        else:
            # Fallback to dummy mode
            await asyncio.sleep(1)
            return f"Echo from Root Agent (Dummy Mode): You said '{user_input}'"
