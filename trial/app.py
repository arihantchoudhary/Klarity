from flask import Flask, request, jsonify, send_from_directory
import os
import random
import time

app = Flask(__name__)

# Mock data for demonstration purposes
RESPONSES = {
    "How does CoT decoding reveal reasoning abilities obscured by standard greedy decoding?": 
        "CoT decoding reveals reasoning abilities by examining alternative decoding paths beyond the most likely one predicted by standard greedy decoding. While greedy decoding only follows the highest probability tokens at each step, CoT decoding considers multiple potential reasoning paths by analyzing the model's confidence across different token possibilities. This technique shows that language models often contain implicit reasoning capabilities that are 'hidden' because greedy decoding prioritizes the most likely next token rather than complete coherent reasoning chains. By identifying paths where the model has high confidence in its reasoning, CoT decoding can surface these latent abilities without requiring explicit prompting, demonstrating that LLMs have inherent reasoning capabilities that standard inference methods often fail to utilize.",
    
    "What are the differences between STaR and traditional prompting techniques?": 
        "STaR (Self-Taught Reasoner) differs from traditional prompting in several key ways: 1) STaR iteratively improves model reasoning through self-refinement, while traditional prompting uses fixed templates; 2) STaR generates its own rationales which are then used to improve future performance, creating a feedback loop, whereas traditional prompting doesn't involve model-generated improvement; 3) STaR explicitly focuses on improving reasoning paths rather than just final answers; 4) STaR can generalize reasoning strategies across problem types, while traditional prompting often requires task-specific engineering. Essentially, STaR creates an iterative learning cycle where the model teaches itself to reason better using its own generated explanations, rather than relying on human-designed prompts or demonstrations.",
    
    "How does chain-of-thought reasoning enhance computational power?": 
        "Chain-of-thought reasoning enhances computational power by enabling transformer models to solve problems beyond their theoretical complexity limits. As shown in the research, constant-precision transformers are limited to ACO complexity (a subset of P), but when augmented with chain-of-thought reasoning, they can achieve NC1-completeness (problems solvable by circuits with polylogarithmic depth). This computational power boost happens because CoT allows models to break complex problems into simpler sub-problems and solve them sequentially, effectively simulating a more powerful computational model through its intermediate reasoning steps. By externalizing reasoning in a step-by-step format, transformers can overcome their inherent limitations, similar to how humans use working memory and intermediate calculations to solve problems beyond what we could compute in a single step. This indicates that reasoning capabilities fundamentally expand what these neural architectures can compute."
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    sources = data.get('sources', [])
    
    # Simulate processing time
    time.sleep(1.5)
    
    # If the message matches one of our prepared responses, use it
    if message in RESPONSES:
        response = RESPONSES[message]
    else:
        # Otherwise generate a generic response
        response = generate_response(message, sources)
    
    return jsonify({"response": response})

def generate_response(message, sources):
    """Generate a response based on the message and selected sources."""
    
    # This is a very basic response generator for demonstration
    # In a real application, this would likely use an LLM or similar technology
    
    source_text = ""
    if sources:
        source_text = f" based on {len(sources)} selected sources"
    
    responses = [
        f"Analyzing your question about '{message[:30]}...'{source_text}. The research suggests that chain-of-thought reasoning emerges naturally in large language models when examining alternative decoding paths rather than just the greedy path. This indicates that reasoning capabilities are inherent in these models but often remain hidden during standard inference procedures.",
        
        f"Regarding '{message[:30]}...'{source_text}, the papers demonstrate that transformer models with chain-of-thought reasoning can theoretically achieve computational capabilities beyond their standard precision limitations, particularly moving from ACO complexity to NC1-completeness for certain problem classes.",
        
        f"Your question about '{message[:30]}...'{source_text} relates to how models can be trained to generate rationales during the training process. The STaR method described in the first paper shows how iteratively refining models using their own generated rationales can significantly improve reasoning performance on complex tasks."
    ]
    
    return random.choice(responses)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
