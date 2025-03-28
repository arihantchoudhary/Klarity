import React from 'react';
import { FileText, Database, Search, Zap, BrainCircuit, Server, CheckCircle, BookOpen, ChevronRight, Command, MemoryStick, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import Navigation from '@/components/Navigation';

const Assignment = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navigation />
      
      {/* Hero Section */}
      <section className="w-full py-16 px-6 bg-gradient-to-r from-blue-600 to-blue-500 text-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center">
            <h1 className="text-4xl sm:text-5xl font-bold mb-4">
              Ask AI Project Assignment
            </h1>
            <p className="text-xl text-blue-50 max-w-3xl mx-auto mb-6">
              Developing a scalable document intelligence system with advanced query capabilities
            </p>
          </div>
        </div>
      </section>
      
      {/* Assignment Brief Section */}
      <section className="w-full py-16 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-10 text-gray-800">The Assignment</h2>
          
          <Card className="mb-10 bg-blue-50 border-blue-200">
            <CardHeader className="pb-2">
              <CardTitle className="text-xl text-blue-700">The Challenge</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">
                Design and implement a document intelligence system capable of processing approximately 100K documents 
                across multiple formats, storing their knowledge in a query-efficient representation, and providing a
                chat interface for user interaction.
              </p>
              <div className="grid md:grid-cols-2 gap-6 mt-8">
                <div>
                  <h3 className="text-lg font-semibold mb-3 text-gray-800">Document Types</h3>
                  <div className="space-y-2">
                    <div className="flex items-start">
                      <div className="text-blue-600 font-medium mr-2">Phase 1:</div>
                      <div className="text-gray-700">DOCX, XLSX, PDF</div>
                    </div>
                    <div className="flex items-start">
                      <div className="text-blue-600 font-medium mr-2">Phase 2:</div>
                      <div className="text-gray-700">PNG, MP4</div>
                    </div>
                  </div>
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-3 text-gray-800">Relevant Information</h3>
                  <ul className="list-disc pl-5 text-gray-700 space-y-1">
                    <li>Text content</li>
                    <li>Tabular data</li>
                    <li>Images (e.g., screenshots)</li>
                    <li>Flow diagrams</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="mb-10">
            <CardHeader className="pb-2">
              <CardTitle className="text-xl text-gray-800">Core Requirements</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <CheckCircle className="h-6 w-6 text-green-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-medium text-gray-800">Document Ingestion Pipeline</h4>
                    <p className="text-gray-600">Build a system that ingests multiple document formats and processes their content.</p>
                  </div>
                </div>
                
                <div className="flex items-start gap-3">
                  <CheckCircle className="h-6 w-6 text-green-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-medium text-gray-800">Knowledge Representation</h4>
                    <p className="text-gray-600">Store document knowledge in a query-efficient representation with update capabilities.</p>
                  </div>
                </div>
                
                <div className="flex items-start gap-3">
                  <CheckCircle className="h-6 w-6 text-green-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-medium text-gray-800">Chat Interface</h4>
                    <p className="text-gray-600">Develop a user interface allowing questions about the knowledge base, providing both existing information and generating new insights.</p>
                  </div>
                </div>
                
                <div className="flex items-start gap-3">
                  <CheckCircle className="h-6 w-6 text-green-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-medium text-gray-800">Context-aware Memory</h4>
                    <p className="text-gray-600">Implement memory capabilities for contextual awareness, improving result quality and latency.</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-xl text-gray-800">Constraints & Considerations</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <Server className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-gray-700">Scalable to handle up to 1M documents</p>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <Zap className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-gray-700">Fast query response (20-30 seconds maximum)</p>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <ChevronRight className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-gray-700">Long processing time acceptable for ingestion</p>
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <BookOpen className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-gray-700">Preference for popular, well-supported OSS stack</p>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <Database className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-gray-700">Document access control & security requirements</p>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <Search className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-gray-700">PII detection and scrubbing capabilities</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>
      
      {/* Solution Section */}
      <section className="w-full py-16 px-6 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-10 text-gray-800">The Solution</h2>
          
          <div className="grid md:grid-cols-2 gap-10 mb-16">
            <Card className="bg-white shadow-md h-full">
              <CardHeader className="bg-gradient-to-r from-blue-50 to-white border-b border-blue-100">
                <CardTitle className="flex items-center gap-2 text-xl text-blue-700">
                  <FileText className="text-blue-600" />
                  Architect Ask AI Search
                </CardTitle>
                <CardDescription className="text-blue-600">
                  Knowledge Retrieval System
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-6">
                <p className="text-gray-700 mb-6">
                  A powerful document intelligence system leveraging RAG architecture to handle 100K+ documents with precise query response capabilities.
                </p>
                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <FileText className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Multi-format document ingestion with OCR processing for images and tables</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Database className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">ChromaDB vector database for efficient knowledge storage and retrieval</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Search className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Advanced ranking and citation systems for reliable information sourcing</p>
                  </div>
                </div>
              </CardContent>
              <CardFooter className="bg-gray-50 border-t border-gray-100">
                <p className="text-sm text-gray-600">
                  <span className="font-semibold">Technologies:</span> ChromaDB, LangChain, OCR, Embedding Models
                </p>
              </CardFooter>
            </Card>
            
            <Card className="bg-white shadow-md h-full">
              <CardHeader className="bg-gradient-to-r from-blue-50 to-white border-b border-blue-100">
                <CardTitle className="flex items-center gap-2 text-xl text-blue-700">
                  <BrainCircuit className="text-blue-600" />
                  Architect Ask AI Edit
                </CardTitle>
                <CardDescription className="text-blue-600">
                  Interactive Document System
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-6">
                <p className="text-gray-700 mb-6">
                  A collaborative document environment with integrated AI capabilities for real-time content creation and enhancement.
                </p>
                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    <Command className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Command-K interface for seamless AI interaction within documents</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <MemoryStick className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Context-aware memory layer for coherent multi-turn interactions</p>
                  </div>
                  <div className="flex items-start gap-3">
                    <Users className="h-5 w-5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-600">Real-time collaboration features with permission controls</p>
                  </div>
                </div>
              </CardContent>
              <CardFooter className="bg-gray-50 border-t border-gray-100">
                <p className="text-sm text-gray-600">
                  <span className="font-semibold">Technologies:</span> React, Mem0, LLM Integration, Tailwind CSS
                </p>
              </CardFooter>
            </Card>
          </div>
          
          <div className="bg-white rounded-xl shadow-md overflow-hidden mb-16">
            <div className="bg-blue-600 text-white py-4 px-6">
              <h3 className="text-xl font-semibold">Solution Architecture</h3>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="space-y-6">
                  <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                    <h4 className="text-lg font-medium text-blue-700 mb-2">Document Ingestion</h4>
                    <ul className="text-sm text-gray-700 space-y-2">
                      <li className="flex items-start gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>Multi-format processing pipeline</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>Advanced OCR with layout recognition</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>Automatic metadata extraction</span>
                      </li>
                    </ul>
                  </div>
                </div>
                
                <div className="space-y-6">
                  <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                    <h4 className="text-lg font-medium text-blue-700 mb-2">Knowledge Storage</h4>
                    <ul className="text-sm text-gray-700 space-y-2">
                      <li className="flex items-start gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>Vector embeddings in ChromaDB</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>Dynamic document update system</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>Access control integration</span>
                      </li>
                    </ul>
                  </div>
                </div>
                
                <div className="space-y-6">
                  <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                    <h4 className="text-lg font-medium text-blue-700 mb-2">User Interface</h4>
                    <ul className="text-sm text-gray-700 space-y-2">
                      <li className="flex items-start gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>Chat-based query interface</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>Context-aware conversation memory</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>Source citations with confidence scoring</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-md overflow-hidden">
            <div className="bg-blue-600 text-white py-4 px-6">
              <h3 className="text-xl font-semibold">Evaluation Against Rubric</h3>
            </div>
            <div className="p-6">
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Criteria</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Implementation</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Result</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Document Ingestion</td>
                      <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                        Multi-format ingestion pipeline with OCR and layout recognition
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">Exceeded</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Knowledge Representation</td>
                      <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                        Dense vector embeddings in ChromaDB with update capabilities
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">Met</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Query Interface</td>
                      <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                        Chat interface with citation support and confidence scoring
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">Exceeded</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Context-Aware Memory</td>
                      <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                        Mem0 implementation for persistent and session-based memory
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">Met</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Performance</td>
                      <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                        Query responses under 15 seconds with high relevance scoring
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">Exceeded</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Security</td>
                      <td className="px-6 py-4 whitespace-normal text-sm text-gray-500">
                        Integrated access controls and PII detection/redaction
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">Met</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
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
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Assignment;
