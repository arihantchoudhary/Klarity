
import React from 'react';
import { Link } from 'react-router-dom';
import { FileText, Edit3, Check, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import Navigation from '@/components/Navigation';

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navigation />
      
      {/* Hero Section */}
      <section className="w-full py-16 px-6 bg-gradient-to-r from-architect-navy to-architect-darkPurple text-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center animate-fade-in">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold mb-4">
              Architect: Revolutionizing Document Intelligence
            </h1>
            <p className="text-xl md:text-2xl text-gray-200 mb-8">
              Welcome to Architect – Explore Perplexity for Docs and Cursor for Docs
            </p>
            <p className="text-lg md:text-xl text-gray-300 max-w-3xl mx-auto mb-10">
              Harnessing AI to transform document processing and knowledge retrieval.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link to="/perplexity">
                <Button size="lg" className="bg-white text-architect-navy hover:bg-gray-100 flex items-center gap-2">
                  <FileText size={20} />
                  Explore Perplexity for Docs
                </Button>
              </Link>
              <Link to="/cursor">
                <Button size="lg" variant="outline" className="bg-transparent text-white border-white hover:bg-white/10 flex items-center gap-2">
                  <Edit3 size={20} />
                  Explore Cursor for Docs
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
      
      {/* Overview Section */}
      <section className="w-full py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Our Products</h2>
          
          <div className="grid md:grid-cols-2 gap-8">
            <Card className="product-card">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-2xl">
                  <FileText className="text-architect-purple" />
                  Perplexity for Docs
                </CardTitle>
                <CardDescription className="text-base">
                  AI-powered document intelligence
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 mb-4">
                  An AI-powered system designed to ingest, process, and retrieve insights from 100K+ documents across diverse formats. With cutting-edge OCR, vector embeddings, and citation handling, it delivers precise answers to user queries.
                </p>
              </CardContent>
              <CardFooter>
                <Link to="/perplexity" className="w-full">
                  <Button className="w-full justify-between">
                    <span>Explore Demo</span>
                    <ArrowRight size={16} />
                  </Button>
                </Link>
              </CardFooter>
            </Card>
            
            <Card className="product-card">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-2xl">
                  <Edit3 className="text-architect-purple" />
                  Cursor for Docs
                </CardTitle>
                <CardDescription className="text-base">
                  AI-enhanced document editing
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 mb-4">
                  A collaborative document editing tool that integrates AI models to enhance content creation. Upload documents, interact with AI through commands, and seamlessly enrich your content.
                </p>
              </CardContent>
              <CardFooter>
                <Link to="/cursor" className="w-full">
                  <Button className="w-full justify-between">
                    <span>Explore Demo</span>
                    <ArrowRight size={16} />
                  </Button>
                </Link>
              </CardFooter>
            </Card>
          </div>
        </div>
      </section>
      
      {/* Features Section */}
      <section className="w-full py-16 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-16">Key Features</h2>
          
          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <FileText className="text-architect-purple" />
                Perplexity for Docs
              </h3>
              
              <div className="space-y-4">
                <div className="feature-card">
                  <h4 className="font-semibold text-lg mb-2">Multi-format Document Ingestion</h4>
                  <p className="text-gray-600">Support for docx, pdf, png, jpeg, mp3, mp4 and more.</p>
                </div>
                
                <div className="feature-card">
                  <h4 className="font-semibold text-lg mb-2">Advanced OCR</h4>
                  <p className="text-gray-600">Extract text, tables, images, and diagrams with high accuracy.</p>
                </div>
                
                <div className="feature-card">
                  <h4 className="font-semibold text-lg mb-2">Dense Vector Embeddings</h4>
                  <p className="text-gray-600">768 dimensions stored in a vector database for semantic search.</p>
                </div>
                
                <div className="feature-card">
                  <h4 className="font-semibold text-lg mb-2">Query-based Retrieval</h4>
                  <p className="text-gray-600">Advanced ranking and re-ranking algorithms.</p>
                </div>
                
                <div className="feature-card">
                  <h4 className="font-semibold text-lg mb-2">Citation Support</h4>
                  <p className="text-gray-600">Every answer includes sources with page references.</p>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Edit3 className="text-architect-purple" />
                Cursor for Docs
              </h3>
              
              <div className="space-y-4">
                <div className="feature-card">
                  <h4 className="font-semibold text-lg mb-2">Document Upload Interface</h4>
                  <p className="text-gray-600">Intuitive left panel display of uploaded documents.</p>
                </div>
                
                <div className="feature-card">
                  <h4 className="font-semibold text-lg mb-2">Central Editor Space</h4>
                  <p className="text-gray-600">Real-time interaction with AI models while editing.</p>
                </div>
                
                <div className="feature-card">
                  <h4 className="font-semibold text-lg mb-2">Command-K Functionality</h4>
                  <p className="text-gray-600">Quick access to AI models to enhance content creation.</p>
                </div>
                
                <div className="feature-card">
                  <h4 className="font-semibold text-lg mb-2">AI-Enhanced Editing</h4>
                  <p className="text-gray-600">Summarize, expand, or enhance your content with AI assistance.</p>
                </div>
                
                <div className="feature-card">
                  <h4 className="font-semibold text-lg mb-2">Collaborative Features</h4>
                  <p className="text-gray-600">Share and collaborate on documents with team members.</p>
                </div>
              </div>
            </div>
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
      <section className="w-full py-16 px-6 bg-architect-purple text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to explore our demos?</h2>
          <p className="text-xl text-white/80 mb-8">
            Experience the power of AI-enhanced document processing and editing.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link to="/perplexity">
              <Button size="lg" className="bg-white text-architect-purple hover:bg-gray-100 flex items-center gap-2">
                <FileText size={20} />
                Try Perplexity for Docs
              </Button>
            </Link>
            <Link to="/cursor">
              <Button size="lg" variant="outline" className="bg-transparent text-white border-white hover:bg-white/10 flex items-center gap-2">
                <Edit3 size={20} />
                Try Cursor for Docs
              </Button>
            </Link>
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="w-full py-6 px-6 bg-gray-100">
        <div className="max-w-6xl mx-auto text-center text-gray-600">
          <p>© 2023 Architect. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
