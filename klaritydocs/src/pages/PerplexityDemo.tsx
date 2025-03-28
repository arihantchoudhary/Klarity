
import React, { useState, useEffect } from 'react';
import { Book, FileText, Image, Search, Send, ChevronRight, ChevronLeft, Database, Cpu, FileSearch, Network } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import Navigation from '@/components/Navigation';
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from '@/components/ui/carousel';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';

type MessageType = {
  id: string;
  sender: 'user' | 'ai';
  content: React.ReactNode;
  timestamp: Date;
  citations?: {
    source: string;
    page: number;
  }[];
};

type DocumentType = {
  id: string;
  name: string;
  type: 'pdf' | 'docx' | 'image' | 'spreadsheet';
  icon: React.ElementType;
};

type TestCaseType = {
  id: string;
  name: string;
  description: string;
  query: string;
};

type WorkflowStepType = {
  id: string;
  title: string;
  description: string;
  icon: React.ElementType;
};

const PerplexityDemo = () => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<MessageType[]>([
    {
      id: '1',
      sender: 'ai',
      content: 'Welcome to Architect Ask AI Search. I can help you find information from your documents. What would you like to know?',
      timestamp: new Date(),
    },
  ]);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isWalkthroughActive, setIsWalkthroughActive] = useState(false);
  const [isWorkflowOpen, setIsWorkflowOpen] = useState(true);
  const [selectedTestCase, setSelectedTestCase] = useState<TestCaseType | null>(null);

  const documents: DocumentType[] = [
    { id: '1', name: 'Financial_Report_Q4.pdf', type: 'pdf', icon: FileText },
    { id: '2', name: 'Product_Roadmap.docx', type: 'docx', icon: FileText },
    { id: '3', name: 'Organizational_Chart.png', type: 'image', icon: Image },
    { id: '4', name: 'Revenue_Data.xlsx', type: 'spreadsheet', icon: FileText },
    { id: '5', name: 'Marketing_Strategy.pdf', type: 'pdf', icon: FileText },
    { id: '6', name: 'Customer_Feedback_Q3.pdf', type: 'pdf', icon: FileText },
    { id: '7', name: 'Annual_Forecast_2023.xlsx', type: 'spreadsheet', icon: FileText },
    { id: '8', name: 'Executive_Summary.docx', type: 'docx', icon: FileText },
    { id: '9', name: 'Market_Analysis.pdf', type: 'pdf', icon: FileText },
    { id: '10', name: 'Team_Structure.png', type: 'image', icon: Image },
  ];

  const testCases: TestCaseType[] = [
    { 
      id: '1', 
      name: 'Revenue Data', 
      description: 'Retrieve Q4 revenue data from financial reports', 
      query: 'What was our Q4 revenue?' 
    },
    { 
      id: '2', 
      name: 'Organization Structure', 
      description: 'Get insights about our organizational structure', 
      query: 'Show me the organizational chart' 
    },
    { 
      id: '3', 
      name: 'Product Roadmap', 
      description: 'Review key milestones in our product roadmap', 
      query: 'What are the key milestones in our product roadmap?' 
    },
    { 
      id: '4', 
      name: 'Marketing Strategy', 
      description: 'Learn about our marketing strategy and budget allocation', 
      query: 'Explain our marketing strategy and budget allocation' 
    },
    { 
      id: '5', 
      name: 'Customer Feedback', 
      description: 'Analyze customer feedback from Q3', 
      query: 'What was the main customer feedback in Q3?' 
    },
    { 
      id: '6', 
      name: 'Annual Forecast', 
      description: 'Get insights from our 2023 forecast', 
      query: 'What does our 2023 forecast predict?' 
    },
    { 
      id: '7', 
      name: 'Executive Summary', 
      description: 'Read the executive summary highlights', 
      query: 'What are the key points in the executive summary?' 
    },
    { 
      id: '8', 
      name: 'Market Analysis', 
      description: 'Get market analysis insights', 
      query: 'What does our market analysis show?' 
    },
    { 
      id: '9', 
      name: 'Team Structure', 
      description: 'Learn about our team hierarchy', 
      query: 'How is our team structured?' 
    },
    { 
      id: '10', 
      name: 'Financial Comparison', 
      description: 'Compare Q3 and Q4 financial performance', 
      query: 'Compare our Q3 and Q4 financial performance' 
    }
  ];

  const workflowSteps: WorkflowStepType[] = [
    { 
      id: '1', 
      title: 'Document Ingestion', 
      description: 'Documents in multiple formats (PDF, DOCX, images) are uploaded and processed through our ingestion pipeline.', 
      icon: FileText 
    },
    { 
      id: '2', 
      title: 'OCR Processing', 
      description: 'Text, tables, images, and diagrams are extracted from documents using advanced OCR technology.', 
      icon: FileSearch 
    },
    { 
      id: '3', 
      title: 'Chunking', 
      description: 'Documents are broken down into smaller, semantically meaningful chunks for efficient processing.', 
      icon: Database 
    },
    { 
      id: '4', 
      title: 'Vectorization', 
      description: '768-dimensional dense vector embeddings are created to represent each chunk numerically.', 
      icon: Cpu 
    },
    { 
      id: '5', 
      title: 'Query Retrieval', 
      description: 'Approximate nearest neighbor search finds the most relevant chunks to answer user queries.', 
      icon: Network 
    }
  ];

  const handleSendQuery = () => {
    if (!query.trim()) return;

    const newUserMessage: MessageType = {
      id: Date.now().toString(),
      sender: 'user',
      content: query,
      timestamp: new Date(),
    };

    let aiResponse: MessageType;

    // Hardcoded responses based on query
    if (query.toLowerCase().includes('revenue') || query.toLowerCase().includes('q4')) {
      aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        content: (
          <div>
            <p>The revenue from Q4 2022 was $2.3M, representing a 15% increase from Q3.</p>
            <p>This exceeded the projected target of $2.1M by approximately 9.5%.</p>
            <p>Key contributors to this growth were:</p>
            <ul className="list-disc pl-5 mt-2">
              <li>New enterprise clients (42% of growth)</li>
              <li>Expansion of existing accounts (31% of growth)</li>
              <li>Improved retention rates (27% of growth)</li>
            </ul>
          </div>
        ),
        timestamp: new Date(),
        citations: [
          { source: 'Financial_Report_Q4.pdf', page: 3 },
          { source: 'Revenue_Data.xlsx', page: 1 },
        ],
      };
    } else if (query.toLowerCase().includes('chart') || query.toLowerCase().includes('organization')) {
      aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        content: (
          <div>
            <p>The organizational chart shows a hierarchical structure with 5 departments:</p>
            <ul className="list-disc pl-5 mt-2">
              <li>Engineering (32 team members)</li>
              <li>Marketing (18 team members)</li>
              <li>Sales (24 team members)</li>
              <li>Finance (12 team members)</li>
              <li>HR (8 team members)</li>
            </ul>
            <p className="mt-2">Each department has a VP who reports directly to the CEO. The Engineering department is further divided into 4 sub-teams: Frontend, Backend, DevOps, and QA.</p>
          </div>
        ),
        timestamp: new Date(),
        citations: [
          { source: 'Organizational_Chart.png', page: 1 },
          { source: 'Team_Structure.png', page: 1 },
        ],
      };
    } else if (query.toLowerCase().includes('roadmap') || query.toLowerCase().includes('product')) {
      aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        content: (
          <div>
            <p>The product roadmap outlines key milestones for Q1-Q4 2023:</p>
            <ul className="list-disc pl-5 mt-2">
              <li>Q1: API Integration Enhancement (completed)</li>
              <li>Q2: Mobile App Release (completed)</li>
              <li>Q3: Enterprise Security Features (in progress, 85% complete)</li>
              <li>Q4: AI-Powered Analytics Dashboard (planning phase)</li>
            </ul>
            <p className="mt-2">The highest priority for Q4 is the AI Analytics Dashboard, with an estimated delivery date of November 15, 2023.</p>
          </div>
        ),
        timestamp: new Date(),
        citations: [
          { source: 'Product_Roadmap.docx', page: 2 },
          { source: 'Executive_Summary.docx', page: 5 },
        ],
      };
    } else if (query.toLowerCase().includes('marketing') || query.toLowerCase().includes('strategy')) {
      aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        content: (
          <div>
            <p>The marketing strategy focuses on three primary channels with the following budget allocation:</p>
            <ul className="list-disc pl-5 mt-2">
              <li>Content marketing (40% of budget, $480K)</li>
              <li>Paid advertising (35% of budget, $420K)</li>
              <li>Partner co-marketing (25% of budget, $300K)</li>
            </ul>
            <p className="mt-2">The primary KPIs are lead generation (target: 1500/month), conversion rate (target: 3.5%), and customer acquisition cost (target: $380).</p>
          </div>
        ),
        timestamp: new Date(),
        citations: [
          { source: 'Marketing_Strategy.pdf', page: 5 },
          { source: 'Annual_Forecast_2023.xlsx', page: 12 },
        ],
      };
    } else if (query.toLowerCase().includes('feedback') || query.toLowerCase().includes('customer')) {
      aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        content: (
          <div>
            <p>Q3 customer feedback highlights show:</p>
            <ul className="list-disc pl-5 mt-2">
              <li>Overall satisfaction score: 8.7/10 (up from 8.2 in Q2)</li>
              <li>Most praised feature: New dashboard interface (mentioned by 68% of respondents)</li>
              <li>Top improvement request: Enhanced mobile experience (mentioned by 43% of respondents)</li>
            </ul>
            <p className="mt-2">Based on this feedback, the product team has prioritized mobile UX improvements for Q4.</p>
          </div>
        ),
        timestamp: new Date(),
        citations: [
          { source: 'Customer_Feedback_Q3.pdf', page: 7 },
          { source: 'Executive_Summary.docx', page: 3 },
        ],
      };
    } else if (query.toLowerCase().includes('forecast') || query.toLowerCase().includes('2023')) {
      aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        content: (
          <div>
            <p>The 2023 annual forecast predicts:</p>
            <ul className="list-disc pl-5 mt-2">
              <li>Total revenue: $9.8M (22% YoY growth)</li>
              <li>Gross margin: 72% (up from 68% in 2022)</li>
              <li>Customer growth: 35% (reaching ~780 total customers)</li>
              <li>Churn rate: 5% (down from 7.5% in 2022)</li>
            </ul>
            <p className="mt-2">The forecast indicates we will exceed our annual growth targets if Q4 performance continues as projected.</p>
          </div>
        ),
        timestamp: new Date(),
        citations: [
          { source: 'Annual_Forecast_2023.xlsx', page: 3 },
          { source: 'Financial_Report_Q4.pdf', page: 12 },
        ],
      };
    } else if (query.toLowerCase().includes('executive') || query.toLowerCase().includes('summary')) {
      aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        content: (
          <div>
            <p>Key points from the executive summary:</p>
            <ul className="list-disc pl-5 mt-2">
              <li>YTD performance is 8% above projections</li>
              <li>Customer retention has improved to 93%</li>
              <li>The Series B funding round ($18M) closed successfully in Q3</li>
              <li>International expansion into EMEA is on track for Q1 2024</li>
            </ul>
            <p className="mt-2">The board has approved the proposed 2024 budget with a focus on scaling operations and expanding the sales team.</p>
          </div>
        ),
        timestamp: new Date(),
        citations: [
          { source: 'Executive_Summary.docx', page: 1 },
          { source: 'Annual_Forecast_2023.xlsx', page: 18 },
        ],
      };
    } else if (query.toLowerCase().includes('market') || query.toLowerCase().includes('analysis')) {
      aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        content: (
          <div>
            <p>Our market analysis shows:</p>
            <ul className="list-disc pl-5 mt-2">
              <li>Total addressable market (TAM): $4.2B with 14% CAGR</li>
              <li>Current market share: 2.3% (up from 1.8% last year)</li>
              <li>Top competitor market share: 18% (Company X), 12% (Company Y)</li>
              <li>Fastest growing segment: Mid-market enterprises (22% growth)</li>
            </ul>
            <p className="mt-2">The analysis suggests focusing on the mid-market segment while developing enterprise features to capture larger accounts in 2024.</p>
          </div>
        ),
        timestamp: new Date(),
        citations: [
          { source: 'Market_Analysis.pdf', page: 4 },
          { source: 'Executive_Summary.docx', page: 7 },
        ],
      };
    } else if (query.toLowerCase().includes('team') || query.toLowerCase().includes('structure')) {
      aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        content: (
          <div>
            <p>Our team structure consists of:</p>
            <ul className="list-disc pl-5 mt-2">
              <li>Leadership team: CEO, CTO, CFO, CMO, COO</li>
              <li>Engineering (32): Frontend (10), Backend (12), DevOps (6), QA (4)</li>
              <li>Sales (24): Direct (16), Channel (8)</li>
              <li>Marketing (18): Content (6), Digital (5), Product (4), Brand (3)</li>
              <li>Finance & HR (20): Finance (12), HR (8)</li>
            </ul>
            <p className="mt-2">The planned expansion for Q1 2024 will add 18 new positions, primarily in Engineering and Sales.</p>
          </div>
        ),
        timestamp: new Date(),
        citations: [
          { source: 'Team_Structure.png', page: 1 },
          { source: 'Organizational_Chart.png', page: 1 },
        ],
      };
    } else if (query.toLowerCase().includes('compare') || (query.toLowerCase().includes('q3') && query.toLowerCase().includes('q4'))) {
      aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        content: (
          <div>
            <p>Comparing Q3 and Q4 financial performance:</p>
            <table className="min-w-full bg-white mt-3 border border-gray-200">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border p-2 text-left">Metric</th>
                  <th className="border p-2 text-left">Q3 2022</th>
                  <th className="border p-2 text-left">Q4 2022</th>
                  <th className="border p-2 text-left">Change</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border p-2">Revenue</td>
                  <td className="border p-2">$2.0M</td>
                  <td className="border p-2">$2.3M</td>
                  <td className="border p-2 text-green-600">+15%</td>
                </tr>
                <tr>
                  <td className="border p-2">Gross Margin</td>
                  <td className="border p-2">67%</td>
                  <td className="border p-2">71%</td>
                  <td className="border p-2 text-green-600">+4%</td>
                </tr>
                <tr>
                  <td className="border p-2">New Customers</td>
                  <td className="border p-2">42</td>
                  <td className="border p-2">58</td>
                  <td className="border p-2 text-green-600">+38%</td>
                </tr>
                <tr>
                  <td className="border p-2">CAC</td>
                  <td className="border p-2">$420</td>
                  <td className="border p-2">$390</td>
                  <td className="border p-2 text-green-600">-7%</td>
                </tr>
              </tbody>
            </table>
            <p className="mt-3">Q4 showed significant improvements across all key metrics, with the most notable gain in new customer acquisition.</p>
          </div>
        ),
        timestamp: new Date(),
        citations: [
          { source: 'Financial_Report_Q4.pdf', page: 8 },
          { source: 'Revenue_Data.xlsx', page: 5 },
        ],
      };
    } else {
      aiResponse = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        content: (
          <div>
            <p>I couldn't find specific information related to your query in the uploaded documents.</p>
            <p className="mt-2">Please try asking about one of these topics:</p>
            <ul className="list-disc pl-5 mt-1">
              <li>Q4 revenue data</li>
              <li>Organizational chart</li>
              <li>Product roadmap</li>
              <li>Marketing strategy</li>
              <li>Customer feedback</li>
              <li>Annual forecast</li>
              <li>Executive summary</li>
              <li>Market analysis</li>
              <li>Team structure</li>
              <li>Financial comparison between Q3 and Q4</li>
            </ul>
          </div>
        ),
        timestamp: new Date(),
      };
    }

    setMessages([...messages, newUserMessage, aiResponse]);
    setQuery('');
  };

  const handleTestCaseClick = (testCase: TestCaseType) => {
    setSelectedTestCase(testCase);
    setQuery(testCase.query);
    
    if (isWalkthroughActive) {
      // Reset the walkthrough to start fresh with the new test case
      setCurrentStepIndex(0);
    }
  };

  const startWalkthrough = () => {
    setIsWalkthroughActive(true);
    setCurrentStepIndex(0);
    if (selectedTestCase) {
      setQuery(selectedTestCase.query);
    } else if (testCases.length > 0) {
      setSelectedTestCase(testCases[0]);
      setQuery(testCases[0].query);
    }
  };

  const nextWalkthroughStep = () => {
    if (currentStepIndex < workflowSteps.length - 1) {
      setCurrentStepIndex(currentStepIndex + 1);
    } else {
      // If we're at the last step, send the query
      handleSendQuery();
      setIsWalkthroughActive(false);
      setCurrentStepIndex(0);
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Effect to handle keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Command+K to start walkthrough
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        startWalkthrough();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [selectedTestCase]);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navigation />
      
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-500 py-12 px-6 text-white">
        <div className="max-w-5xl mx-auto text-center">
          <h1 className="text-3xl md:text-4xl font-bold mb-3">Architect Ask AI Search</h1>
          <p className="text-lg md:text-xl text-blue-100 max-w-3xl mx-auto">
            Explore how we retrieve insights from over 100K+ documents with precision and context.
          </p>
        </div>
      </div>
      
      {/* Test Cases Carousel */}
      <div className="py-6 px-4 md:px-6 max-w-6xl mx-auto w-full">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Example Queries</h2>
        <Carousel className="w-full">
          <CarouselContent>
            {testCases.map((testCase) => (
              <CarouselItem key={testCase.id} className="md:basis-1/2 lg:basis-1/3">
                <Card 
                  className={`h-full ${selectedTestCase?.id === testCase.id ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-200'}`}
                  onClick={() => handleTestCaseClick(testCase)}
                >
                  <CardContent className="p-4 cursor-pointer h-full flex flex-col">
                    <h3 className="font-medium text-blue-700">{testCase.name}</h3>
                    <p className="text-sm text-gray-600 mt-1 mb-2 flex-grow">{testCase.description}</p>
                    <div className="text-xs bg-gray-100 p-2 rounded-md text-gray-700">
                      "{testCase.query}"
                    </div>
                  </CardContent>
                </Card>
              </CarouselItem>
            ))}
          </CarouselContent>
          <div className="flex justify-end mt-4 space-x-2">
            <CarouselPrevious className="position-static" />
            <CarouselNext className="position-static" />
          </div>
        </Carousel>
      </div>
      
      <div className="flex flex-col md:flex-row flex-1 max-w-6xl mx-auto w-full px-4 md:px-6">
        {/* Left Sidebar - Document List */}
        <div className="w-full md:w-64 bg-white border border-gray-200 rounded-lg p-4 mb-4 md:mb-0 md:mr-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Documents</h2>
            <Button variant="outline" size="sm" className="text-xs">
              Upload
            </Button>
          </div>
          
          <div className="space-y-2 max-h-[500px] overflow-y-auto">
            {documents.map((doc) => (
              <div 
                key={doc.id} 
                className="flex items-center p-2 rounded-md hover:bg-gray-100 cursor-pointer"
              >
                <doc.icon className="h-4 w-4 mr-2 text-gray-500" />
                <span className="text-sm text-gray-700 truncate">{doc.name}</span>
              </div>
            ))}
          </div>
        </div>
        
        {/* Main Content - Chat Interface */}
        <div className="flex-1 flex flex-col md:mx-0 order-2 md:order-2">
          <div className="bg-white border border-gray-200 rounded-lg p-4 mb-4">
            <Collapsible open={isWorkflowOpen} onOpenChange={setIsWorkflowOpen}>
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-800">How It Works</h2>
                <CollapsibleTrigger asChild>
                  <Button variant="ghost" size="sm">
                    {isWorkflowOpen ? 'Hide' : 'Show'}
                  </Button>
                </CollapsibleTrigger>
              </div>
              
              <CollapsibleContent className="mt-3">
                <div className="flex flex-wrap md:flex-nowrap gap-2 md:gap-4 relative">
                  {workflowSteps.map((step, index) => (
                    <div 
                      key={step.id} 
                      className={`flex-1 p-3 rounded-lg border ${
                        isWalkthroughActive && currentStepIndex === index 
                          ? 'border-blue-500 bg-blue-50' 
                          : 'border-gray-200'
                      }`}
                    >
                      <div className="flex items-center mb-2">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-2 ${
                          isWalkthroughActive && currentStepIndex === index 
                            ? 'bg-blue-500 text-white' 
                            : 'bg-gray-100 text-gray-500'
                        }`}>
                          <step.icon className="h-4 w-4" />
                        </div>
                        <h3 className="font-medium text-sm">{step.title}</h3>
                      </div>
                      <p className="text-xs text-gray-600">{step.description}</p>
                    </div>
                  ))}
                  
                  {/* Connecting lines between steps */}
                  <div className="hidden md:flex absolute top-1/2 left-0 right-0 z-0 transform -translate-y-1/2">
                    <div className="h-px bg-gray-300 w-full"></div>
                  </div>
                </div>
                
                {!isWalkthroughActive && (
                  <div className="mt-4 text-center">
                    <Button onClick={startWalkthrough} className="bg-blue-600 text-white hover:bg-blue-700">
                      Start Interactive Walkthrough
                    </Button>
                    <p className="text-xs text-gray-500 mt-2">Or press Command+K (Ctrl+K) to start</p>
                  </div>
                )}
                
                {isWalkthroughActive && (
                  <div className="mt-4 flex justify-between items-center">
                    <p className="text-sm text-gray-700">
                      <span className="font-medium">Step {currentStepIndex + 1}/{workflowSteps.length}:</span> {workflowSteps[currentStepIndex].title}
                    </p>
                    <Button onClick={nextWalkthroughStep}>
                      {currentStepIndex < workflowSteps.length - 1 ? 'Next Step' : 'Complete & Send Query'}
                      <ChevronRight className="h-4 w-4 ml-1" />
                    </Button>
                  </div>
                )}
              </CollapsibleContent>
            </Collapsible>
          </div>
          
          {/* Messages Container */}
          <div className="flex-1 bg-white border border-gray-200 rounded-lg p-4 mb-4 overflow-y-auto max-h-[400px]">
            <div className="space-y-4">
              {messages.map((message) => (
                <div 
                  key={message.id} 
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div 
                    className={`max-w-md p-4 rounded-lg ${
                      message.sender === 'user' 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-white border border-gray-200'
                    }`}
                  >
                    <div className={message.sender === 'user' ? 'text-white' : 'text-gray-800'}>
                      {message.content}
                      
                      {/* Citations */}
                      {message.citations && message.citations.length > 0 && (
                        <div className={`mt-3 pt-2 border-t ${message.sender === 'user' ? 'border-blue-400' : 'border-gray-200'} text-xs ${message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'}`}>
                          <p className="font-semibold mb-1">Sources:</p>
                          {message.citations.map((citation, index) => (
                            <p key={index} className="flex items-center">
                              <FileText className="h-3 w-3 mr-1" />
                              {citation.source}, Page {citation.page}
                            </p>
                          ))}
                        </div>
                      )}
                    </div>
                    <div 
                      className={`text-xs mt-1 ${
                        message.sender === 'user' ? 'text-white/70' : 'text-gray-500'
                      }`}
                    >
                      {formatTime(message.timestamp)}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Input Area */}
          <div className="sticky bottom-0 bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center gap-2">
              <Input
                type="text"
                placeholder="Ask a question about your documents..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendQuery()}
                className="flex-1"
              />
              <Button onClick={handleSendQuery} className="bg-blue-600 hover:bg-blue-700">
                <Send className="h-4 w-4 mr-1" />
                Ask
              </Button>
            </div>
          </div>
        </div>
        
        {/* Right Sidebar - Evaluation Criteria */}
        <div className="hidden lg:block w-64 ml-4 order-3">
          <div className="bg-white border border-gray-200 rounded-lg p-4 mb-4">
            <h3 className="font-medium text-gray-800 mb-3">Evaluation Criteria</h3>
            <div className="space-y-3 text-sm">
              {/* Table based on your evaluation criteria */}
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-1/2">Criteria</TableHead>
                    <TableHead className="w-1/2">Implementation</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow>
                    <TableCell className="font-medium">Document Ingestion</TableCell>
                    <TableCell>100K+ documents with Supabase Graph DB</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="font-medium">Knowledge Representation</TableCell>
                    <TableCell>Dense vector embeddings in ChromaDB</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="font-medium">Knowledge Updates</TableCell>
                    <TableCell>Dynamic updates when docs change</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="font-medium">Query Interface</TableCell>
                    <TableCell>ANN search with citations</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="font-medium">Context-Aware Memory</TableCell>
                    <TableCell>Mem0 memory layer integration</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </div>
          </div>
          
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <h3 className="font-medium text-gray-800 mb-3">Search Context</h3>
            <div className="space-y-3">
              <Card className="shadow-sm">
                <CardContent className="p-3">
                  <div className="flex items-center gap-2 text-sm">
                    <Search className="h-3.5 w-3.5 text-gray-500" />
                    <span className="text-gray-700">All documents</span>
                  </div>
                </CardContent>
              </Card>
              <Card className="shadow-sm">
                <CardContent className="p-3">
                  <div className="flex items-center gap-2 text-sm">
                    <Book className="h-3.5 w-3.5 text-gray-500" />
                    <span className="text-gray-700">Last 12 months</span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
      
      {/* Detailed Explanations Section */}
      <div className="max-w-6xl mx-auto w-full px-4 md:px-6 py-8 bg-white border border-gray-200 rounded-lg mt-8 mb-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">How Our Technology Works</h2>
        
        <div className="space-y-8">
          <div>
            <h3 className="text-lg font-semibold text-blue-700 mb-2">Document Ingestion</h3>
            <p className="text-gray-700">
              Our system supports ingestion of over 100,000 documents across multiple formats (PDF, DOCX, PNG, etc.) 
              using Supabase Graph DB. The ingestion pipeline processes documents in parallel, handling up to 1,000 
              pages per minute with advanced OCR and image recognition. Each document goes through a standardization 
              process to ensure consistent data extraction regardless of source format.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-blue-700 mb-2">Knowledge Representation</h3>
            <p className="text-gray-700">
              We use 768-dimensional dense vector embeddings stored in ChromaDB to represent document chunks. 
              Each vector captures the semantic meaning of text, enabling us to find related information even 
              when exact keywords aren't present. Our custom embedding model has been fine-tuned on domain-specific 
              data to enhance retrieval accuracy for business documents, technical specifications, and financial reports.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-blue-700 mb-2">Knowledge Updates</h3>
            <p className="text-gray-700">
              When documents are modified, our system automatically detects changes and updates the corresponding 
              vector representations. The differential update mechanism only re-processes changed sections, making 
              updates nearly instantaneous. This ensures that users always receive the most current information, 
              with version control tracking to maintain historical context when needed.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-blue-700 mb-2">Query Interface</h3>
            <p className="text-gray-700">
              Our query system uses approximate nearest neighbor (ANN) search to find the most relevant document 
              chunks for user questions. Results undergo a multi-stage ranking process, with primary retrieval 
              followed by cross-attention re-ranking to improve precision. All responses include citations with 
              source documents and page numbers, enabling users to verify information and explore related context.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-blue-700 mb-2">Context-Aware Memory</h3>
            <p className="text-gray-700">
              The Mem0 memory layer retains context across user interactions, creating a more coherent conversation 
              experience. This allows for follow-up questions without restating context, clarification requests, and 
              personalized responses based on user history. The system maintains both short-term session memory and 
              longer-term user preferences, continuously improving as it learns from interactions.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PerplexityDemo;
