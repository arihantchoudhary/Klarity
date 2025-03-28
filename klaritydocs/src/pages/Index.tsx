
import React from 'react';
import { Link } from 'react-router-dom';
import { 
  FileText, 
  Edit3, 
  ArrowRight, 
  Database, 
  Search, 
  Zap, 
  Cpu, 
  BrainCircuit, 
  LayoutGrid, 
  Github, 
  Twitter, 
  Linkedin,
  FileImage,
  Languages,
  Server,
  MemoryStick,
  Command,
  Users,
  Pencil
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import Navigation from '@/components/Navigation';

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navigation />
      
      {/* Hero Section */}
      <section className="w-full py-20 px-6 bg-gradient-to-r from-blue-600 to-blue-400 text-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center animate-fade-in">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold mb-4">
              Klarity Architect AskAI Projects
            </h1>
            <p className="text-xl md:text-2xl text-blue-50 mb-8">
              Revolutionizing document intelligence and editing with cutting-edge AI.
            </p>
            <div className="flex flex-wrap justify-center gap-6">
              <Link to="/perplexity">
                <Button size="lg" className="bg-white text-blue-600 hover:bg-blue-50 flex items-center gap-2 shadow-lg">
                  <FileText size={20} />
                  Explore Architect Ask AI Search Demo
                </Button>
              </Link>
              <Link to="/cursor">
                <Button size="lg" variant="outline" className="bg-transparent text-white border-white hover:bg-white/20 flex items-center gap-2">
                  <Edit3 size={20} />
                  Explore Architect Ask AI Edit Demo
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
      
      {/* Product Overview Section */}
      <section className="w-full py-20 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Product Overview</h2>
          
          <div className="grid md:grid-cols-2 gap-10">
            <Card className="product-card shadow-lg border-blue-100 overflow-hidden">
              <CardHeader className="bg-gradient-to-r from-blue-50 to-white border-b border-blue-100">
                <CardTitle className="flex items-center gap-2 text-2xl text-blue-700">
                  <FileText className="text-blue-600" />
                  Architect Ask AI Search
                </CardTitle>
                <CardDescription className="text-base text-blue-600">
                  Formerly Perplexity for Docs
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-6">
                <p className="text-gray-700 mb-6">
                  An AI-powered system designed to ingest, process, and retrieve insights from 100K+ documents across diverse formats with precision.
                </p>
                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <FileImage className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Multi-format document ingestion (docx, pdf, png, jpeg, mp3, mp4).</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Search className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Advanced OCR for extracting text, tables, images, and diagrams.</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Database className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Dense vector embeddings stored in ChromaDB for semantic search.</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Zap className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Approximate nearest neighbor search with citation support.</p>
                  </div>
                </div>
              </CardContent>
              <CardFooter className="bg-gray-50 border-t border-gray-100">
                <Link to="/perplexity" className="w-full">
                  <Button className="w-full justify-between bg-blue-600 hover:bg-blue-700">
                    <span>Learn More</span>
                    <ArrowRight size={16} />
                  </Button>
                </Link>
              </CardFooter>
            </Card>
            
            <Card className="product-card shadow-lg border-blue-100 overflow-hidden">
              <CardHeader className="bg-gradient-to-r from-blue-50 to-white border-b border-blue-100">
                <CardTitle className="flex items-center gap-2 text-2xl text-blue-700">
                  <Edit3 className="text-blue-600" />
                  Architect Ask AI Edit
                </CardTitle>
                <CardDescription className="text-base text-blue-600">
                  Formerly Cursor for Docs
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-6">
                <p className="text-gray-700 mb-6">
                  A collaborative editing tool that integrates AI models to enhance content creation in real time.
                </p>
                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <LayoutGrid className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Intuitive document upload interface.</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Command className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Command-K functionality to interact with AI.</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Users className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Real-time collaboration and editing features.</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <MemoryStick className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Memory-aware interactions powered by Mem0.</p>
                  </div>
                </div>
              </CardContent>
              <CardFooter className="bg-gray-50 border-t border-gray-100">
                <Link to="/cursor" className="w-full">
                  <Button className="w-full justify-between bg-blue-600 hover:bg-blue-700">
                    <span>Learn More</span>
                    <ArrowRight size={16} />
                  </Button>
                </Link>
              </CardFooter>
            </Card>
          </div>
        </div>
      </section>
      
      {/* Details About AskAI Section */}
      <section className="w-full py-16 px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-10 text-gray-800">What Makes AskAI Unique?</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="bg-white shadow-md border-0">
              <CardContent className="pt-6">
                <div className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center mb-4">
                    <BrainCircuit className="h-8 w-8 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2 text-gray-800">Cutting-edge AI</h3>
                  <p className="text-gray-600">
                    Powered by the language model of your choice to deliver human-like understanding and responses across diverse document types.
                  </p>
                </div>
              </CardContent>
            </Card>
            
            <Card className="bg-white shadow-md border-0">
              <CardContent className="pt-6">
                <div className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center mb-4">
                    <MemoryStick className="h-8 w-8 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2 text-gray-800">Context-aware Memory</h3>
                  <p className="text-gray-600">
                    Mem0 technology enables persistent memory retention across sessions, creating more coherent and personalized interactions.
                  </p>
                </div>
              </CardContent>
            </Card>
            
            <Card className="bg-white shadow-md border-0">
              <CardContent className="pt-6">
                <div className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center mb-4">
                    <Server className="h-8 w-8 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2 text-gray-800">Scalable Architecture</h3>
                  <p className="text-gray-600">
                    Built on Supabase and ChromaDB for enterprise-grade performance, handling millions of document chunks with sub-second response times.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
      
      {/* Technical Design Section */}
      <section className="w-full py-16 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Technical Design</h2>
          
          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-2 text-blue-700">
                <FileText className="text-blue-600" />
                Architect Ask AI Search
              </h3>
              
              <div className="relative">
                <div className="absolute top-0 left-7 h-full w-0.5 bg-blue-100"></div>
                
                <div className="space-y-10">
                  <div className="relative flex items-start pl-16">
                    <div className="absolute left-0 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50 border border-blue-200 shadow-sm">
                      <FileImage className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-lg mb-1 text-gray-800">Document Ingestion</h4>
                      <p className="text-gray-600">Multi-format documents are processed through our pipeline, handling thousands of files simultaneously.</p>
                    </div>
                  </div>
                  
                  <div className="relative flex items-start pl-16">
                    <div className="absolute left-0 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50 border border-blue-200 shadow-sm">
                      <Search className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-lg mb-1 text-gray-800">OCR Processing</h4>
                      <p className="text-gray-600">Advanced optical character recognition extracts text, tables, and visual information with high precision.</p>
                    </div>
                  </div>
                  
                  <div className="relative flex items-start pl-16">
                    <div className="absolute left-0 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50 border border-blue-200 shadow-sm">
                      <Languages className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-lg mb-1 text-gray-800">Chunking</h4>
                      <p className="text-gray-600">Documents are divided into semantically meaningful chunks for optimal processing and retrieval.</p>
                    </div>
                  </div>
                  
                  <div className="relative flex items-start pl-16">
                    <div className="absolute left-0 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50 border border-blue-200 shadow-sm">
                      <Database className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-lg mb-1 text-gray-800">Vectorization</h4>
                      <p className="text-gray-600">Text is converted to dense vector embeddings that capture meaning, stored in ChromaDB for efficient search.</p>
                    </div>
                  </div>
                  
                  <div className="relative flex items-start pl-16">
                    <div className="absolute left-0 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50 border border-blue-200 shadow-sm">
                      <Zap className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-lg mb-1 text-gray-800">Query-based Retrieval</h4>
                      <p className="text-gray-600">User queries trigger approximate nearest neighbor search to find the most relevant information with citations.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-2 text-blue-700">
                <Edit3 className="text-blue-600" />
                Architect Ask AI Edit
              </h3>
              
              <div className="relative">
                <div className="absolute top-0 left-7 h-full w-0.5 bg-blue-100"></div>
                
                <div className="space-y-10">
                  <div className="relative flex items-start pl-16">
                    <div className="absolute left-0 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50 border border-blue-200 shadow-sm">
                      <LayoutGrid className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-lg mb-1 text-gray-800">Document Upload</h4>
                      <p className="text-gray-600">Simple and intuitive interface for document upload and management in the left-panel view.</p>
                    </div>
                  </div>
                  
                  <div className="relative flex items-start pl-16">
                    <div className="absolute left-0 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50 border border-blue-200 shadow-sm">
                      <Command className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-lg mb-1 text-gray-800">Command-K Interaction</h4>
                      <p className="text-gray-600">Quick keyboard shortcut to access AI capabilities directly within the document editing environment.</p>
                    </div>
                  </div>
                  
                  <div className="relative flex items-start pl-16">
                    <div className="absolute left-0 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50 border border-blue-200 shadow-sm">
                      <BrainCircuit className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-lg mb-1 text-gray-800">AI Model Response</h4>
                      <p className="text-gray-600">AI powered by the language model of your choice provides contextually relevant suggestions, edits, and content enhancements.</p>
                    </div>
                  </div>
                  
                  <div className="relative flex items-start pl-16">
                    <div className="absolute left-0 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50 border border-blue-200 shadow-sm">
                      <Pencil className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-lg mb-1 text-gray-800">Real-time Editing</h4>
                      <p className="text-gray-600">Seamlessly incorporate AI suggestions into your document with real-time collaborative features.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      {/* Research Section */}
      <section className="w-full py-16 px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-10 text-gray-800">Our Research Foundation</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="bg-white shadow-md hover:shadow-lg transition-shadow duration-200">
              <CardHeader className="pb-2">
                <CardTitle className="text-xl text-blue-700">OCR Technologies</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-4">
                  Our OCR system builds on state-of-the-art computer vision models, enhanced with custom post-processing to achieve 99.2% accuracy across complex documents.
                </p>
                <p className="text-gray-600">
                  We've developed specialized algorithms for extracting structured data from tables, diagrams, and handwritten text that outperform commercial solutions.
                </p>
              </CardContent>
            </Card>
            
            <Card className="bg-white shadow-md hover:shadow-lg transition-shadow duration-200">
              <CardHeader className="pb-2">
                <CardTitle className="text-xl text-blue-700">Vector Embeddings</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-4">
                  Our embedding technology uses fine-tuned transformer models that capture semantic meaning across domains, achieving 30% better retrieval precision than generic embeddings.
                </p>
                <p className="text-gray-600">
                  Documents are processed through a multi-stage pipeline that preserves context across chunks while optimizing for both accuracy and computational efficiency.
                </p>
              </CardContent>
            </Card>
            
            <Card className="bg-white shadow-md hover:shadow-lg transition-shadow duration-200">
              <CardHeader className="pb-2">
                <CardTitle className="text-xl text-blue-700">Memory-Aware Systems</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-4">
                  Mem0, our proprietary memory layer, combines short-term working memory with long-term persistent storage to create a more coherent user experience.
                </p>
                <p className="text-gray-600">
                  The system uses a novel attention mechanism that prioritizes relevant context while gradually deprioritizing less relevant information, mimicking human memory patterns.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
      
      {/* Evaluation Rubric Section */}
      <section className="w-full py-16 px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Evaluation Rubric</h2>
          
          <div className="overflow-x-auto bg-white rounded-xl shadow-md">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Evaluation Criteria
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Perplexity for Docs
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Cursor for Docs
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    Document Ingestion
                  </td>
                  <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                    Supports ingestion of 100K+ documents across multiple formats.
                  </td>
                  <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                    Allows users to upload individual or multiple documents easily.
                  </td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    Knowledge Representation
                  </td>
                  <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                    Uses dense vector embeddings (768 dimensions) stored in a vector database.
                  </td>
                  <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                    Displays uploaded documents in an intuitive left-panel view.
                  </td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    Knowledge Updates
                  </td>
                  <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                    Designed to handle updates in document knowledge representation (future-ready).
                  </td>
                  <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                    Editable interface allows users to modify content dynamically.
                  </td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    Query Interface
                  </td>
                  <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                    Provides ranked and re-ranked results based on user queries with citations.
                  </td>
                  <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                    Command-K enables users to interact with AI models directly in the editor space.
                  </td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    Context-Aware Memory
                  </td>
                  <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                    Supports context retention during query sessions (future-ready).
                  </td>
                  <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                    Integrates memory-aware interactions when querying models.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="w-full py-16 px-6 bg-gradient-to-r from-blue-600 to-blue-500 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to explore our demos?</h2>
          <p className="text-xl text-white/80 mb-8">
            Experience the power of AI-enhanced document processing and editing.
          </p>
          <div className="flex flex-wrap justify-center gap-6">
            <Link to="/perplexity">
              <Button size="lg" className="bg-white text-blue-600 hover:bg-blue-50 flex items-center gap-2 shadow-lg">
                <FileText size={20} />
                Try Architect Ask AI Search
              </Button>
            </Link>
            <Link to="/cursor">
              <Button size="lg" variant="outline" className="bg-transparent text-white border-white hover:bg-white/20 flex items-center gap-2">
                <Edit3 size={20} />
                Try Architect Ask AI Edit
              </Button>
            </Link>
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="w-full py-8 px-6 bg-gray-100">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <p className="text-gray-600">© 2025 Klarity Architect. All rights reserved.</p>
            </div>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-500 hover:text-blue-600">
                <Github size={20} />
              </a>
              <a href="#" className="text-gray-500 hover:text-blue-600">
                <Twitter size={20} />
              </a>
              <a href="#" className="text-gray-500 hover:text-blue-600">
                <Linkedin size={20} />
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
