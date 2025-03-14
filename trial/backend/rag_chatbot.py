from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from .vector_store import DenseVectorIndexer

class RAGChatbot:
    """Handles question answering using RAG with conversation memory."""
    
    def __init__(self,
                vector_store: DenseVectorIndexer,
                model_name: str = "gpt-4-turbo-preview",
                temperature: float = 0.7,
                max_tokens: int = 1000):
        """Initialize the RAG chatbot.
        
        Args:
            vector_store: Vector store for document retrieval
            model_name: Name of the LLM to use
            temperature: Temperature for response generation
            max_tokens: Maximum tokens in response
        """
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.vector_store.as_retriever(),
            memory=self.memory,
            return_source_documents=True,
            verbose=True
        )
    
    def query(self, question: str) -> Dict[str, Any]:
        """Process a question and return an answer with sources.
        
        Args:
            question: User's question
            
        Returns:
            Dictionary containing answer and source documents
        """
        # Get response from the chain
        response = self.qa_chain({"question": question})
        
        # Extract source information
        sources = []
        for doc in response["source_documents"]:
            source_info = {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": getattr(doc, "relevance_score", None)
            }
            sources.append(source_info)
        
        return {
            "answer": response["answer"],
            "sources": sources
        }
    
    def clear_memory(self):
        """Clear the conversation memory."""
        self.memory.clear()
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the conversation history.
        
        Returns:
            List of message dictionaries with 'role' and 'content'
        """
        messages = []
        for msg in self.memory.chat_memory.messages:
            messages.append({
                "role": "user" if msg.type == "human" else "assistant",
                "content": msg.content
            })
        return messages 