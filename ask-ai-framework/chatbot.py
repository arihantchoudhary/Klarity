import os
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from vector_store import DenseVectorStore

class RAGChatbot:
    """RAG chatbot that uses ChromaDB for retrieval and OpenAI for generation."""
    
    def __init__(self, vector_store_path: str = "./vector_store"):
        """Initialize the chatbot.
        
        Args:
            vector_store_path: Path to the vector store directory
        """
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize vector store
        self.vector_store = DenseVectorStore(vector_store_path)
        
        # Initialize conversation history
        self.conversation_history = []
        
        # System prompt template
        self.system_prompt = """You are a helpful assistant that answers questions about Pfizer documents. 
        Use ONLY the provided context to answer questions. If you cannot find the answer in the context, 
        say "I cannot find information about that in the provided documents."
        Keep your answers concise and to the point. Always cite the source document when providing information."""
    
    def _get_relevant_context(self, query: str, n_results: int = 3) -> str:
        """Retrieve relevant context from the vector store.
        
        Args:
            query: User query
            n_results: Number of results to retrieve
            
        Returns:
            String containing relevant context
        """
        results = self.vector_store.search(query, n_results=n_results)
        
        # Format context with source information
        context_pieces = []
        for result in results:
            context = f"From {result['metadata']['file_path']}:\n{result['chunk']}"
            context_pieces.append(context)
        
        return "\n\n".join(context_pieces)
    
    def chat(self, user_input: str) -> str:
        """Process user input and generate a response.
        
        Args:
            user_input: User's question or message
            
        Returns:
            Assistant's response
        """
        # Get relevant context
        context = self._get_relevant_context(user_input)
        
        # Prepare messages for the API call
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_input}"}
        ]
        
        # Add conversation history if it exists
        messages.extend(self.conversation_history)
        
        try:
            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # You can change this to a different model
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            # Get the response content
            assistant_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.extend([
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": assistant_response}
            ])
            
            # Keep only last 6 messages in history to manage context window
            if len(self.conversation_history) > 6:
                self.conversation_history = self.conversation_history[-6:]
            
            return assistant_response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"

def main():
    """Run an interactive chat session."""
    
    # Initialize chatbot
    script_dir = Path(__file__).parent.absolute()
    vector_store_path = script_dir / 'vector_store'
    
    print("\nInitializing RAG chatbot...")
    chatbot = RAGChatbot(str(vector_store_path))
    
    print("\nChatbot ready! Type 'quit' to exit.")
    print("You can ask questions about the Pfizer documents.\n")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        response = chatbot.chat(user_input)
        print(f"\nAssistant: {response}")

if __name__ == "__main__":
    main() 