import os
import logging
from typing import List, Dict, Optional
from openai import OpenAI
from vector_store import DenseVectorIndexer

logger = logging.getLogger(__name__)

class RAGChatbot:
    """Handles question answering using RAG with conversation memory."""
    
    def __init__(self, vector_store: DenseVectorIndexer, model: str = "gpt-4-turbo-preview"):
        """Initialize the RAG chatbot.
        
        Args:
            vector_store: Vector store for document retrieval
            model: OpenAI model to use for chat
        """
        self.vector_store = vector_store
        self.model = model
        self.client = OpenAI()
        self.chat_history = []
        
        # System prompt template
        self.system_prompt = """You are a helpful AI assistant that answers questions based on the provided context. 
        Your responses should:
        1. Be based ONLY on the information in the provided context
        2. Cite the specific parts of the context you used
        3. Say "I don't know" if the context doesn't contain the relevant information
        4. Be clear and concise
        5. Use bullet points and formatting for better readability when appropriate"""
    
    def _get_relevant_context(self, query: str, k: int = 5) -> str:
        """Get relevant context from the vector store.
        
        Args:
            query: User query
            k: Number of relevant chunks to retrieve
            
        Returns:
            Formatted context string
        """
        results = self.vector_store.similarity_search(query, k=k)
        
        if not results:
            return ""
        
        # Format context with source information
        context_parts = []
        for i, result in enumerate(results, 1):
            text = result['text']
            metadata = result['metadata']
            source = metadata.get('source', 'Unknown') if metadata else 'Unknown'
            context_parts.append(f"[{i}] From {source}:\n{text}\n")
        
        return "\n".join(context_parts)
    
    def query(self, user_input: str) -> Dict:
        """Process a user query and generate a response.
        
        Args:
            user_input: User's question or message
            
        Returns:
            Dictionary containing the response and any additional information
        """
        try:
            # Get relevant context
            context = self._get_relevant_context(user_input)
            
            if not context:
                return {
                    "response": "I don't have any relevant information to answer your question.",
                    "sources_used": []
                }
            
            # Prepare messages for the chat
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_input}"}
            ]
            
            # Add relevant chat history (last 3 exchanges)
            for msg in self.chat_history[-6:]:
                messages.append(msg)
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract response text
            response_text = response.choices[0].message.content
            
            # Update chat history
            self.chat_history.extend([
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": response_text}
            ])
            
            # Keep only last 10 exchanges in history
            if len(self.chat_history) > 20:
                self.chat_history = self.chat_history[-20:]
            
            return {
                "response": response_text,
                "sources_used": context.split("\n\n")
            }
        
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "response": "I encountered an error while processing your request. Please try again.",
                "error": str(e)
            }
    
    def get_chat_history(self) -> List[Dict]:
        """Get the chat history.
        
        Returns:
            List of chat messages
        """
        return self.chat_history
    
    def clear_memory(self) -> None:
        """Clear the chat history."""
        self.chat_history = [] 