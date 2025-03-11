# Ask AI: Enterprise Document Question-Answering System

A comprehensive document ingestion, indexing, and retrieval system powered by Mistral OCR, Elasticsearch, and advanced RAG techniques.

## Overview

Ask AI is an enterprise-grade system that enables users to ask questions about their documents and receive accurate, contextual responses. The system integrates state-of-the-art technologies for document processing, indexing, and retrieval:

- **Document Processing**: Extract text and structure from various document formats
- **Advanced OCR**: Process complex documents with Mistral OCR
- **Multiple Indexing Strategies**: Combine inverted indices, vector search, and sparse encoding
- **Semantic Search**: Leverage embedding models and ELSER for semantic understanding
- **Retrieval Augmented Generation**: Generate accurate responses from document context

## Features

- **Multi-Format Document Support**: Process PDFs, Office documents, images, and more
- **Multilingual Processing**: Support for documents in multiple languages
- **Advanced Document Understanding**: Extract and comprehend text, tables, images, and mathematical expressions
- **Semantic Search**: Find relevant content based on meaning, not just keywords
- **Hybrid Search**: Combine keyword and semantic search for optimal results
- **Context-Aware Responses**: Generate responses that maintain context from previous interactions
- **Source Citations**: Provide citations to source documents for response verification
- **Scalable Architecture**: Horizontally scalable microservices architecture
- **Secure Implementation**: Authentication, authorization, and data protection

## Implementation Guide

This guide outlines the steps to implement the Ask AI system from scratch, including local development and Kubernetes deployment.

### Prerequisites

- Docker and Docker Compose for local development
- Kubernetes cluster for production deployment
- Elasticsearch cluster (7.17+ or 8.x)
- Python 3.9+
- Mistral API key (for OCR integration)

### Step 1: Local Development Setup

1. Clone the repository:

```bash
git clone https://github.com/your-org/ask-ai.git
cd ask-ai
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

4. Start local services with Docker Compose:

```bash
docker-compose up -d
```

5. Initialize Elasticsearch indices:

```bash
python -m src.scripts.initialize_indices
```

### Step 2: Document Ingestion Implementation

#### Setting up Mistral OCR

1. Configure Mistral OCR Client:

   - Obtain Mistral API key
   - Update configuration in `.env` file

2. Implement the Document Ingestion Pipeline:
   - Implement file processing for different formats
   - Configure OCR processing for complex documents
   - Implement document chunking strategies

Example OCR Configuration:

```python
extraction_config = {
    "use_ocr": True,
    "mistral_api_key": os.getenv("MISTRAL_API_KEY"),
    "use_self_hosted_ocr": False,
    "self_hosted_ocr_url": None,
    "ocr_output_format": "markdown",
    "ocr_mime_types": [
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/tiff",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
}
```

### Step 3: Elasticsearch Integration

#### Setting up Elasticsearch

1. Configure Elasticsearch Client:

```python
from elasticsearch import Elasticsearch

es_client = Elasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_URL")],
    basic_auth=(os.getenv("ELASTICSEARCH_USER"), os.getenv("ELASTICSEARCH_PASSWORD")),
    verify_certs=False if os.getenv("ELASTICSEARCH_VERIFY_CERTS", "true").lower() == "false" else True
)
```

2. Create Index Templates:

```python
# Example index template with multiple field types
index_template = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "default": {
                    "type": "standard",
                    "stopwords": "_english_"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "content": {
                "type": "text",
                "analyzer": "standard"
            },
            "content_vector": {
                "type": "dense_vector",
                "dims": 768,
                "index": true,
                "similarity": "cosine"
            },
            "metadata": {
                "properties": {
                    "source": { "type": "keyword" },
                    "author": { "type": "keyword" },
                    "created_at": { "type": "date" }
                }
            }
        }
    }
}
```

3. Configure ELSER Ingest Pipeline:

```python
elser_pipeline = {
    "description": "ELSER inference pipeline",
    "processors": [
        {
            "inference": {
                "model_id": ".elser_model_1",
                "target_field": "ml.tokens",
                "field_map": {
                    "content": "text_field"
                }
            }
        }
    ]
}
```

### Step 4: Implementing Indexing Strategies

#### 1. Inverted Index (BM25)

The default Elasticsearch text indexing with BM25 scoring:

```python
def index_document_bm25(es_client, index_name, document):
    """Index document using standard inverted index (BM25)."""
    return es_client.index(
        index=index_name,
        document=document
    )
```

#### 2. Vector Indexing

For semantic similarity using dense vector embeddings:

```python
def index_document_with_vector(es_client, index_name, document, embedding_model):
    """Index document with vector embeddings."""
    # Generate embeddings
    text = document["content"]
    embeddings = embedding_model.embed(text)

    # Add embeddings to document
    document["content_vector"] = embeddings

    # Index document
    return es_client.index(
        index=index_name,
        document=document
    )
```

#### 3. Sparse Vector Indexing (ELSER)

Using Elasticsearch ELSER for sparse vector indexing:

```python
def index_document_with_elser(es_client, index_name, document, pipeline_name="elser-pipeline"):
    """Index document with ELSER sparse embeddings."""
    return es_client.index(
        index=index_name,
        document=document,
        pipeline=pipeline_name
    )
```

#### 4. Hybrid Indexing

Use all indexing strategies together:

```python
def index_document_hybrid(es_client, index_name, document, embedding_model, pipeline_name="elser-pipeline"):
    """Index document using hybrid approach."""
    # Generate embeddings
    text = document["content"]
    embeddings = embedding_model.embed(text)

    # Add embeddings to document
    document["content_vector"] = embeddings

    # Index with ELSER pipeline
    return es_client.index(
        index=index_name,
        document=document,
        pipeline=pipeline_name
    )
```

### Step 5: Implementing Search Strategies

#### 1. BM25 Keyword Search

```python
def search_bm25(es_client, index_name, query_text, size=10):
    """Perform BM25 keyword search."""
    query = {
        "query": {
            "match": {
                "content": {
                    "query": query_text,
                    "operator": "OR"
                }
            }
        },
        "size": size
    }
    return es_client.search(index=index_name, body=query)
```

#### 2. Vector Search

```python
def search_vector(es_client, index_name, query_vector, size=10):
    """Perform vector similarity search."""
    query = {
        "query": {
            "knn": {
                "content_vector": {
                    "vector": query_vector,
                    "k": size
                }
            }
        },
        "size": size
    }
    return es_client.search(index=index_name, body=query)
```

#### 3. ELSER Semantic Search

```python
def search_elser(es_client, index_name, query_text, size=10, pipeline_name="elser-pipeline"):
    """Perform semantic search using ELSER."""
    # First, process the query text through the ELSER pipeline
    processed_query = es_client.ingest.simulate(
        body={
            "pipeline": {
                "processors": [
                    {
                        "inference": {
                            "model_id": ".elser_model_1",
                            "target_field": "ml.tokens",
                            "field_map": {
                                "query_text": "text_field"
                            }
                        }
                    }
                ]
            },
            "docs": [
                {
                    "_source": {
                        "query_text": query_text
                    }
                }
            ]
        }
    )

    # Extract the processed tokens
    tokens = processed_query["docs"][0]["doc"]["_source"]["ml"]["tokens"]

    # Perform the search using the tokens
    query = {
        "query": {
            "terms_set": {
                "ml.tokens": {
                    "terms": tokens,
                    "minimum_should_match_script": {
                        "source": "params.num_terms / 2",
                        "params": {
                            "num_terms": len(tokens)
                        }
                    }
                }
            }
        },
        "size": size
    }
    return es_client.search(index=index_name, body=query)
```

#### 4. Hybrid Search (RRF)

```python
def search_hybrid_rrf(es_client, index_name, query_text, query_vector, size=10):
    """Perform hybrid search using RRF (Reciprocal Rank Fusion)."""
    query = {
        "query": {
            "rank_features": {
                "fields": [
                    {
                        "field": "content",
                        "query": query_text,
                        "method": "bm25",
                        "weight": 0.5
                    },
                    {
                        "field": "content_vector",
                        "query": query_vector,
                        "method": "knn",
                        "weight": 0.5
                    }
                ]
            }
        },
        "size": size
    }
    return es_client.search(index=index_name, body=query)
```

### Step 6: Setting up RAG with LangChain

#### Basic RAG Implementation

```python
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import ElasticsearchStore
from langchain.llms import OpenAI

def setup_rag():
    # Initialize embeddings model
    embeddings = OpenAIEmbeddings()

    # Initialize Elasticsearch vector store
    vector_store = ElasticsearchStore(
        es_url=os.getenv("ELASTICSEARCH_URL"),
        index_name="documents",
        embedding=embeddings,
        es_user=os.getenv("ELASTICSEARCH_USER"),
        es_password=os.getenv("ELASTICSEARCH_PASSWORD")
    )

    # Create the retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    # Define the prompt template
    template = """
    You are an AI assistant that answers questions based on context information.

    Context:
    {context}

    Question: {question}

    Answer the question using only the provided context. If you don't know the answer based on the context, say "I don't have enough information to answer this question."

    Answer:
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    # Initialize the LLM
    llm = OpenAI(temperature=0)

    # Create the RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain
```

#### Advanced RAG with Hybrid Search

```python
from langchain.retrievers import ElasticsearchRetriever
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

def setup_advanced_rag():
    # Initialize embeddings model
    embeddings = OpenAIEmbeddings()

    # Initialize Elasticsearch hybrid retriever
    retriever = ElasticsearchRetriever(
        client=es_client,
        index_name="documents",
        query_field="content",
        vector_field="content_vector",
        embedding=embeddings,
        hybrid_search=True,
        hybrid_ratio=0.7  # 70% vector, 30% BM25
    )

    # Initialize conversation memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    # Initialize the LLM
    llm = OpenAI(temperature=0.2)

    # Create the conversational RAG chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )

    return qa_chain
```

### Step 7: API Development

Create RESTful APIs to interact with the system:

```python
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Ask AI API")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Document upload endpoint
@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme)
):
    """Upload a document for processing and indexing."""
    try:
        # Read file content
        content = await file.read()

        # Process document asynchronously
        task_id = await process_document_async(content, file.filename, file.content_type)

        return {"message": "Document upload initiated", "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Query model
class Query(BaseModel):
    text: str
    conversation_id: Optional[str] = None
    search_strategy: str = "hybrid"  # "bm25", "vector", "elser", "hybrid"
    max_results: int = 5

# Question answering endpoint
@app.post("/ask")
async def ask_question(
    query: Query,
    token: str = Depends(oauth2_scheme)
):
    """Ask a question about your documents."""
    try:
        # Get response from RAG system
        response, sources = await generate_response(
            query.text,
            query.conversation_id,
            query.search_strategy,
            query.max_results
        )

        return {
            "answer": response,
            "sources": sources,
            "conversation_id": query.conversation_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Step 8: Web Interface Development

Create a React-based web interface for interacting with the system:

```jsx
// Example React component for the chat interface
import React, { useState, useEffect } from "react";
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  List,
  ListItem,
} from "@mui/material";

function ChatInterface() {
  const [question, setQuestion] = useState("");
  const [conversation, setConversation] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);

    // Add user question to conversation
    const newConversation = [
      ...conversation,
      { role: "user", content: question },
    ];
    setConversation(newConversation);

    try {
      // Call the API
      const response = await fetch("/api/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          text: question,
          conversation_id: conversationId,
          search_strategy: "hybrid",
          max_results: 5,
        }),
      });

      const data = await response.json();

      // Update conversation with AI response
      setConversation([
        ...newConversation,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
        },
      ]);

      // Update conversation ID if needed
      if (!conversationId && data.conversation_id) {
        setConversationId(data.conversation_id);
      }
    } catch (error) {
      console.error("Error:", error);
      // Add error message to conversation
      setConversation([
        ...newConversation,
        {
          role: "system",
          content: "Sorry, an error occurred. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
      setQuestion("");
    }
  };

  return (
    <Container maxWidth="md">
      <Paper
        elevation={3}
        sx={{
          p: 3,
          my: 4,
          height: "70vh",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Typography variant="h5" gutterBottom>
          Ask AI
        </Typography>

        <List sx={{ flexGrow: 1, overflow: "auto", mb: 2 }}>
          {conversation.map((message, index) => (
            <ListItem
              key={index}
              sx={{
                justifyContent:
                  message.role === "user" ? "flex-end" : "flex-start",
                mb: 1,
              }}
            >
              <Paper
                elevation={1}
                sx={{
                  p: 2,
                  maxWidth: "80%",
                  backgroundColor:
                    message.role === "user" ? "#e3f2fd" : "#f5f5f5",
                }}
              >
                <Typography variant="body1">{message.content}</Typography>

                {message.sources && (
                  <Typography
                    variant="caption"
                    sx={{ display: "block", mt: 1 }}
                  >
                    Sources: {message.sources.map((s) => s.title).join(", ")}
                  </Typography>
                )}
              </Paper>
            </ListItem>
          ))}
        </List>

        <div style={{ display: "flex" }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Ask a question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            disabled={loading}
            onKeyPress={(e) => e.key === "Enter" && sendQuestion()}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={sendQuestion}
            disabled={loading || !question.trim()}
            sx={{ ml: 1 }}
          >
            Send
          </Button>
        </div>
      </Paper>
    </Container>
  );
}

export default ChatInterface;
```

### Step 9: Kubernetes Deployment

#### 1. Create Kubernetes Configuration Files

First, create a namespace for your deployment:

```yaml
# kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ask-ai
```

Create deployments for each microservice:

```yaml
# kubernetes/ingestion.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: document-ingestion
  namespace: ask-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: document-ingestion
  template:
    metadata:
      labels:
        app: document-ingestion
    spec:
      containers:
        - name: document-ingestion
          image: your-registry/ask-ai-ingestion:latest
          ports:
            - containerPort: 8000
          env:
            - name: ELASTICSEARCH_URL
              valueFrom:
                secretKeyRef:
                  name: elasticsearch-credentials
                  key: url
            - name: ELASTICSEARCH_USER
              valueFrom:
                secretKeyRef:
                  name: elasticsearch-credentials
                  key: username
            - name: ELASTICSEARCH_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: elasticsearch-credentials
                  key: password
            - name: MISTRAL_API_KEY
              valueFrom:
                secretKeyRef:
                  name: mistral-credentials
                  key: api-key
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "1Gi"
              cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: document-ingestion
  namespace: ask-ai
spec:
  selector:
    app: document-ingestion
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
```

Create similar deployment files for other microservices.

#### 2. Configure Secrets

Store sensitive information in Kubernetes secrets:

```yaml
# kubernetes/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: elasticsearch-credentials
  namespace: ask-ai
type: Opaque
data:
  url: <base64-encoded-url>
  username: <base64-encoded-username>
  password: <base64-encoded-password>
---
apiVersion: v1
kind: Secret
metadata:
  name: mistral-credentials
  namespace: ask-ai
type: Opaque
data:
  api-key: <base64-encoded-api-key>
```

#### 3. Set Up Ingress

Create an ingress resource to expose your application:

```yaml
# kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ask-ai-ingress
  namespace: ask-ai
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  rules:
    - host: ask-ai.your-domain.com
      http:
        paths:
          - path: /api/ingestion
            pathType: Prefix
            backend:
              service:
                name: document-ingestion
                port:
                  number: 80
          - path: /api/query
            pathType: Prefix
            backend:
              service:
                name: query-processing
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-interface
                port:
                  number: 80
  tls:
    - hosts:
        - ask-ai.your-domain.com
      secretName: tls-secret
```

#### 4. Set Up Monitoring

Create monitoring resources for your application:

```yaml
# kubernetes/monitoring.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ask-ai-monitor
  namespace: ask-ai
spec:
  selector:
    matchLabels:
      app: ask-ai
  endpoints:
    - port: metrics
      interval: 15s
```

#### 5. Horizontal Pod Autoscaling

Configure automatic scaling based on resource usage:

```yaml
# kubernetes/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: document-ingestion-hpa
  namespace: ask-ai
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: document-ingestion
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

#### 6. Deploy to Kubernetes

Apply all configuration files:

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/secrets.yaml
kubectl apply -f kubernetes/ingestion.yaml
kubectl apply -f kubernetes/knowledge-representation.yaml
kubectl apply -f kubernetes/query-processing.yaml
kubectl apply -f kubernetes/response-generation.yaml
kubectl apply -f kubernetes/web-interface.yaml
kubectl apply -f kubernetes/ingress.yaml
kubectl apply -f kubernetes/monitoring.yaml
kubectl apply -f kubernetes/hpa.yaml
```

### Step 10: Integration with Elasticsearch Labs Notebooks

You can leverage the Elasticsearch Labs notebooks for various components of your system:

#### 1. Document Chunking

Use the document chunking notebooks to implement advanced chunking strategies:

- Implement `Document Chunking with Ingest Pipelines` for server-side chunking
- Use `Document Chunking with LangChain Splitters` for client-side chunking

#### 2. RAG Implementation

Adapt the RAG notebooks to enhance your implementation:

- Use `chatbot.ipynb` as a reference for implementing conversational features
- Implement `question-answering.ipynb` to build a robust QA system

#### 3. Semantic Search

Enhance your semantic search capabilities:

- Use the `hybrid-search.ipynb` notebook to improve search accuracy
- Implement ELSER for better semantic understanding using `ELSER.ipynb`

#### 4. Multilingual Support

Add multilingual support using the `multilingual.ipynb` notebook.

## Maintenance and Operations

### CI/CD Pipeline

Set up a CI/CD pipeline for continuous deployment:

1. Set up a GitHub Actions workflow:

```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Login to Container Registry
        uses: docker/login-action@v1
        with:
          registry: your-registry
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Build and push Docker images
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: your-registry/ask-ai:latest

      - name: Set up Kubernetes CLI
        uses: azure/setup-kubectl@v1

      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f kubernetes/
```

### Monitoring and Logging

Set up monitoring and logging for your application:

1. Use Prometheus and Grafana for metrics:

   - Monitor API latency
   - Track document ingestion rate
   - Measure search accuracy

2. Set up ELK stack for logging:
   - Collect application logs
   - Monitor error rates
   - Track user queries

## Performance Tuning

### Elasticsearch Performance Tuning

1. Index Settings:

```json
{
  "index": {
    "refresh_interval": "5s",
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "mapping": {
      "total_fields": {
        "limit": 2000
      }
    }
  }
}
```

2. Bulk Indexing Configuration:

```python
def bulk_index_documents(es_client, index_name, documents, chunk_size=1000):
    """Efficiently index documents in bulk."""
    actions = []
    for doc in documents:
        actions.append({
            "_index": index_name,
            "_source": doc
        })

        if len(actions) >= chunk_size:
            helpers.bulk(es_client, actions)
            actions = []

    if actions:
        helpers.bulk(es_client, actions)
```

## Security Considerations

1. Data Encryption:

   - Encrypt data in transit using TLS
   - Encrypt sensitive data at rest

2. Authentication & Authorization:

   - Implement OAuth2 for authentication
   - Use RBAC for authorization
   - Apply document-level security in Elasticsearch

3. PII Handling:
   - Implement PII detection and redaction
   - Set up audit logging for compliance

## Future Enhancements

1. Multimodal Support:

   - Add support for image understanding
   - Implement video content extraction

2. Advanced RAG Techniques:

   - Implement query rewriting
   - Add self-querying retrieval
   - Implement multi-query expansion

3. Integration with Enterprise Systems:
   - Connect with document management systems
   - Integrate with CRM and ERP systems

## Troubleshooting

Common issues and solutions:

1. Elasticsearch Connection Issues:

   - Check network connectivity
   - Verify credentials
   - Ensure proper SSL configuration

2. OCR Processing Failures:

   - Check Mistral API key validity
   - Verify supported document formats
   - Monitor rate limits

3. Search Quality Issues:
   - Adjust chunk size
   - Tune vector similarity thresholds
   - Balance hybrid search weights
