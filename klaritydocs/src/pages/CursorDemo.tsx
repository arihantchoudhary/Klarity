import React, { useState, useRef } from 'react';
import { 
  Command, 
  File, 
  FolderPlus, 
  Sparkles, 
  ListPlus, 
  Clipboard, 
  Calendar, 
  Package, 
  Bold,
  Italic,
  Underline,
  AlignLeft,
  AlignCenter,
  AlignRight,
  List,
  ListOrdered,
  ChevronRight,
  ChevronLeft,
  FileText,
  Globe,
  Palette,
  Wand2
} from 'lucide-react';
import Navigation from '@/components/Navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { Card, CardContent } from '@/components/ui/card';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { toast } from "sonner";

type DocumentType = {
  id: string;
  name: string;
  dateModified: string;
  selected?: boolean;
};

type CommandType = {
  id: string;
  name: string;
  icon: React.ElementType;
  description: string;
};

type TestCaseType = {
  id: string;
  title: string;
  description: string;
  icon: React.ElementType;
  prompt: string;
  result: React.ReactNode;
};

const CursorDemo = () => {
  const [documents, setDocuments] = useState<DocumentType[]>([
    { id: '1', name: 'Quarterly Report.docx', dateModified: '2023-06-15', selected: true },
    { id: '2', name: 'Meeting Notes.docx', dateModified: '2023-06-10' },
    { id: '3', name: 'Product Specs.pdf', dateModified: '2023-05-22' },
  ]);
  
  const [editorContent, setEditorContent] = useState<React.ReactNode>( 
    <div className="space-y-3">
      <h1 className="text-xl font-bold">Quarterly Report: Q2 2023</h1>
      <p>This document provides an overview of our company's performance in Q2 2023.</p>
      <h2 className="text-lg font-semibold mt-4">Executive Summary</h2>
      <p>
        The second quarter of 2023 saw significant growth in our key markets. Revenue 
        increased by 15% compared to Q1, driven primarily by the launch of our new 
        product line.
      </p>
      <p className="text-sm text-gray-500 italic">
        Type /command to access AI assistance features.
      </p>
    </div>
  );
  
  const [showCommandMenu, setShowCommandMenu] = useState(false);
  const [commandInput, setCommandInput] = useState('');
  const [currentTestCase, setCurrentTestCase] = useState<string | null>(null);
  const editorRef = useRef<HTMLDivElement>(null);

  const formatOptions = [
    { id: 'bold', icon: Bold, label: 'Bold' },
    { id: 'italic', icon: Italic, label: 'Italic' },
    { id: 'underline', icon: Underline, label: 'Underline' },
    { id: 'align-left', icon: AlignLeft, label: 'Align Left' },
    { id: 'align-center', icon: AlignCenter, label: 'Align Center' },
    { id: 'align-right', icon: AlignRight, label: 'Align Right' },
    { id: 'bullet-list', icon: List, label: 'Bullet List' },
    { id: 'numbered-list', icon: ListOrdered, label: 'Numbered List' },
  ];
  
  const commands: CommandType[] = [
    { id: '1', name: 'Summarize', icon: Clipboard, description: 'Create a concise summary of the document' },
    { id: '2', name: 'Generate Key Points', icon: ListPlus, description: 'Extract the most important points' },
    { id: '3', name: 'Create Calendar Event', icon: Calendar, description: 'Generate a calendar event from document' },
    { id: '4', name: 'Expand Section', icon: Package, description: 'Elaborate on the selected section' },
    { id: '5', name: 'Translate', icon: Globe, description: 'Translate the document to another language' },
    { id: '6', name: 'Change Tone', icon: Palette, description: 'Adjust the tone of your document' },
    { id: '7', name: 'Improve Writing', icon: Wand2, description: 'Enhance clarity and readability' },
    { id: '8', name: 'Format Document', icon: FileText, description: 'Apply consistent formatting to document' },
  ];

  const testCases: TestCaseType[] = [
    { 
      id: '1', 
      title: 'Summarize Document', 
      icon: Clipboard,
      description: 'Create a concise summary of the entire document',
      prompt: '/summarize',
      result: (
        <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
          <h3 className="font-medium text-gray-800 flex items-center">
            <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
            AI-Generated Summary
          </h3>
          <p className="text-sm mt-2">
            In Q2 2023, the company experienced robust 15% revenue growth compared to Q1, 
            primarily attributed to the launch of a new product line. The quarter 
            was marked by market expansion and strong performance across key business segments.
          </p>
        </div>
      )
    },
    { 
      id: '2', 
      title: 'Generate Key Points', 
      icon: ListPlus,
      description: 'Extract the most important points from the document',
      prompt: '/key points',
      result: (
        <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
          <h3 className="font-medium text-gray-800 flex items-center">
            <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
            AI-Generated Key Points
          </h3>
          <ul className="text-sm mt-2 list-disc pl-5 space-y-1">
            <li>15% revenue growth in Q2 compared to previous quarter</li>
            <li>New product line launch was the primary growth driver</li>
            <li>Significant expansion in key markets</li>
            <li>Positive trajectory expected to continue in Q3</li>
          </ul>
        </div>
      )
    },
    { 
      id: '3', 
      title: 'Expand Content', 
      icon: Package,
      description: 'Elaborate on a selected section with more details',
      prompt: '/expand',
      result: (
        <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
          <h3 className="font-medium text-gray-800 flex items-center">
            <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
            AI-Generated Expansion
          </h3>
          <div className="text-sm mt-2 space-y-2">
            <p>
              The second quarter of 2023 marked a significant milestone in our company's growth trajectory. 
              We witnessed a remarkable 15% increase in revenue compared to Q1, bringing our total quarterly 
              revenue to $28.5 million.
            </p>
            <p>
              This growth was primarily fueled by the successful launch of our NextGen product line, which 
              exceeded initial sales projections by 22%. The product received overwhelmingly positive feedback 
              from customers, with a satisfaction rating of 4.8/5.
            </p>
            <p>
              Key markets, particularly in North America and Europe, showed exceptional performance with 
              year-over-year growth rates of 18% and 14% respectively. Our expansion into APAC is proceeding 
              according to plan, with new partnerships established in Singapore and Australia.
            </p>
          </div>
        </div>
      )
    },
    { 
      id: '4', 
      title: 'Translate Text', 
      icon: Globe,
      description: 'Translate the document to another language',
      prompt: '/translate to Spanish',
      result: (
        <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
          <h3 className="font-medium text-gray-800 flex items-center">
            <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
            AI-Generated Translation (Spanish)
          </h3>
          <div className="text-sm mt-2">
            <h1 className="text-xl font-bold">Informe Trimestral: Q2 2023</h1>
            <p>Este documento proporciona una visión general del rendimiento de nuestra empresa en el segundo trimestre de 2023.</p>
            <h2 className="text-lg font-semibold mt-4">Resumen Ejecutivo</h2>
            <p>
              El segundo trimestre de 2023 vio un crecimiento significativo en nuestros mercados clave. 
              Los ingresos aumentaron un 15% en comparación con el primer trimestre, impulsados principalmente 
              por el lanzamiento de nuestra nueva línea de productos.
            </p>
          </div>
        </div>
      )
    },
    { 
      id: '5', 
      title: 'Change Tone', 
      icon: Palette,
      description: 'Adjust the tone of your document',
      prompt: '/change tone to formal',
      result: (
        <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
          <h3 className="font-medium text-gray-800 flex items-center">
            <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
            AI-Generated Formal Tone
          </h3>
          <div className="text-sm mt-2">
            <h1 className="text-xl font-bold">Quarterly Report: Q2 2023</h1>
            <p>This document presents a comprehensive analysis of the organization's performance during the second quarter of 2023.</p>
            <h2 className="text-lg font-semibold mt-4">Executive Summary</h2>
            <p>
              The second quarter of fiscal year 2023 demonstrated substantial growth across key market segments. 
              Revenue exhibited a 15% increase relative to the first quarter, primarily attributable to the 
              strategic introduction of our new product portfolio.
            </p>
          </div>
        </div>
      )
    },
    { 
      id: '6', 
      title: 'Improve Writing', 
      icon: Wand2,
      description: 'Enhance clarity and readability of your document',
      prompt: '/improve writing',
      result: (
        <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
          <h3 className="font-medium text-gray-800 flex items-center">
            <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
            AI-Enhanced Writing
          </h3>
          <div className="text-sm mt-2">
            <h1 className="text-xl font-bold">Quarterly Report: Q2 2023</h1>
            <p>This comprehensive report details our company's performance during Q2 2023.</p>
            <h2 className="text-lg font-semibold mt-4">Executive Summary</h2>
            <p>
              Our company experienced remarkable growth across key markets in the second quarter of 2023. 
              Revenue surged by 15% compared to Q1, primarily driven by our successful new product line launch, 
              which exceeded all expectations. This strong performance positions us well for continued expansion 
              in the upcoming quarters.
            </p>
          </div>
        </div>
      )
    },
    { 
      id: '7', 
      title: 'Format Document', 
      icon: FileText,
      description: 'Apply consistent formatting to your document',
      prompt: '/format document',
      result: (
        <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
          <h3 className="font-medium text-gray-800 flex items-center">
            <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
            AI-Formatted Document
          </h3>
          <div className="text-sm mt-2 space-y-4">
            <h1 className="text-2xl font-bold text-gray-800 border-b pb-2">Quarterly Report: Q2 2023</h1>
            <p className="text-gray-700 leading-relaxed">This document provides an overview of our company's performance in Q2 2023.</p>
            <h2 className="text-xl font-semibold text-gray-800 mt-6">Executive Summary</h2>
            <p className="text-gray-700 leading-relaxed">
              The second quarter of 2023 saw significant growth in our key markets. Revenue 
              increased by 15% compared to Q1, driven primarily by the launch of our new 
              product line.
            </p>
          </div>
        </div>
      )
    },
    { 
      id: '8', 
      title: 'Create Calendar Event', 
      icon: Calendar,
      description: 'Generate a calendar event from document content',
      prompt: '/create calendar event',
      result: (
        <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
          <h3 className="font-medium text-gray-800 flex items-center">
            <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
            AI-Generated Calendar Event
          </h3>
          <div className="text-sm mt-2 p-3 border border-gray-300 rounded bg-white">
            <div className="flex justify-between items-center">
              <h4 className="font-semibold">Q2 Performance Review</h4>
              <Calendar className="h-4 w-4 text-gray-500" />
            </div>
            <div className="mt-2 text-gray-600">
              <p><span className="font-medium">Date:</span> July 15, 2023</p>
              <p><span className="font-medium">Time:</span> 10:00 AM - 11:30 AM</p>
              <p><span className="font-medium">Location:</span> Conference Room A</p>
              <p className="mt-2"><span className="font-medium">Description:</span> Review Q2 2023 performance results and discuss growth strategies for Q3.</p>
            </div>
          </div>
        </div>
      )
    },
    { 
      id: '9', 
      title: 'Generate Table', 
      icon: ListPlus,
      description: 'Create a structured table from document data',
      prompt: '/generate table of revenue',
      result: (
        <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
          <h3 className="font-medium text-gray-800 flex items-center">
            <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
            AI-Generated Revenue Table
          </h3>
          <div className="text-sm mt-2 overflow-x-auto">
            <table className="min-w-full border border-gray-300">
              <thead className="bg-gray-100">
                <tr>
                  <th className="border border-gray-300 px-4 py-2">Quarter</th>
                  <th className="border border-gray-300 px-4 py-2">Revenue (in millions)</th>
                  <th className="border border-gray-300 px-4 py-2">Growth (%)</th>
                  <th className="border border-gray-300 px-4 py-2">Primary Driver</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-gray-300 px-4 py-2">Q1 2023</td>
                  <td className="border border-gray-300 px-4 py-2">$24.8</td>
                  <td className="border border-gray-300 px-4 py-2">8%</td>
                  <td className="border border-gray-300 px-4 py-2">Market expansion</td>
                </tr>
                <tr className="bg-blue-50">
                  <td className="border border-gray-300 px-4 py-2">Q2 2023</td>
                  <td className="border border-gray-300 px-4 py-2">$28.5</td>
                  <td className="border border-gray-300 px-4 py-2">15%</td>
                  <td className="border border-gray-300 px-4 py-2">New product line</td>
                </tr>
                <tr>
                  <td className="border border-gray-300 px-4 py-2">Q3 2023 (projected)</td>
                  <td className="border border-gray-300 px-4 py-2">$32.2</td>
                  <td className="border border-gray-300 px-4 py-2">13%</td>
                  <td className="border border-gray-300 px-4 py-2">APAC expansion</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )
    },
    { 
      id: '10', 
      title: 'Smart Formatting', 
      icon: Wand2,
      description: 'Apply intelligent formatting based on content type',
      prompt: '/smart format',
      result: (
        <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
          <h3 className="font-medium text-gray-800 flex items-center">
            <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
            AI Smart Formatting
          </h3>
          <div className="text-sm mt-2 space-y-4">
            <div className="p-4 bg-gradient-to-r from-blue-50 to-white border-l-4 border-blue-500 rounded">
              <h1 className="text-2xl font-bold text-blue-800">Quarterly Report: Q2 2023</h1>
              <p className="text-gray-600 italic text-sm">Generated on June 15, 2023</p>
            </div>
            
            <div className="p-3">
              <p className="text-gray-700 leading-relaxed">This document provides an overview of our company's performance in Q2 2023.</p>
            </div>
            
            <div className="p-4 bg-gray-50 border-l-4 border-gray-500 rounded">
              <h2 className="text-xl font-semibold text-gray-800">Executive Summary</h2>
              <p className="text-gray-700 leading-relaxed mt-2">
                The second quarter of 2023 saw <span className="font-semibold text-green-600">significant growth</span> in our key markets. Revenue 
                increased by <span className="font-semibold text-green-600">15%</span> compared to Q1, driven primarily by the launch of our new 
                product line.
              </p>
            </div>
          </div>
        </div>
      )
    }
  ];
  
  const handleDocumentSelect = (id: string) => {
    setDocuments(
      documents.map(doc => ({
        ...doc,
        selected: doc.id === id,
      }))
    );
    
    if (id === '1') {
      setEditorContent(
        <div className="space-y-3">
          <h1 className="text-xl font-bold">Quarterly Report: Q2 2023</h1>
          <p>This document provides an overview of our company's performance in Q2 2023.</p>
          <h2 className="text-lg font-semibold mt-4">Executive Summary</h2>
          <p>
            The second quarter of 2023 saw significant growth in our key markets. Revenue 
            increased by 15% compared to Q1, driven primarily by the launch of our new 
            product line.
          </p>
          <p className="text-sm text-gray-500 italic">
            Type /command to access AI assistance features.
          </p>
        </div>
      );
      setCurrentTestCase(null);
    } else if (id === '2') {
      setEditorContent(
        <div className="space-y-3">
          <h1 className="text-xl font-bold">Meeting Notes: Product Team</h1>
          <p><strong>Date:</strong> June 10, 2023</p>
          <p><strong>Attendees:</strong> John, Sarah, Michael, Lisa</p>
          <h2 className="text-lg font-semibold mt-4">Agenda</h2>
          <ul className="list-disc pl-5">
            <li>Q2 Product Roadmap Review</li>
            <li>Feature Prioritization</li>
            <li>Customer Feedback Discussion</li>
          </ul>
          <p className="text-sm text-gray-500 italic">
            Type /command to access AI assistance features.
          </p>
        </div>
      );
      setCurrentTestCase(null);
    } else if (id === '3') {
      setEditorContent(
        <div className="space-y-3">
          <h1 className="text-xl font-bold">Product Specifications: NextGen Platform</h1>
          <p>This document outlines the technical specifications for our upcoming NextGen platform release.</p>
          <h2 className="text-lg font-semibold mt-4">Technical Requirements</h2>
          <ul className="list-disc pl-5">
            <li>Cloud-native architecture</li>
            <li>Real-time data processing capabilities</li>
            <li>Enterprise-grade security features</li>
            <li>Mobile-responsive interface</li>
          </ul>
          <p className="text-sm text-gray-500 italic">
            Type /command to access AI assistance features.
          </p>
        </div>
      );
      setCurrentTestCase(null);
    }
  };
  
  const handleEditorFocus = () => {
    if (editorRef.current) {
      editorRef.current.focus();
    }
  };

  const handleFormatClick = (formatId: string) => {
    toast(`Applied ${formatId} formatting`, {
      description: "Document formatting has been updated",
    });
  };
  
  const executeCommand = (command: CommandType) => {
    setShowCommandMenu(false);
    
    if (command.name === 'Summarize') {
      toast.success("Generating document summary");
      setTimeout(() => {
        setEditorContent(
          <div className="space-y-3">
            <h1 className="text-xl font-bold">Quarterly Report: Q2 2023</h1>
            <p>This document provides an overview of our company's performance in Q2 2023.</p>
            <h2 className="text-lg font-semibold mt-4">Executive Summary</h2>
            <p>
              The second quarter of 2023 saw significant growth in our key markets. Revenue 
              increased by 15% compared to Q1, driven primarily by the launch of our new 
              product line.
            </p>
            
            <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
              <h3 className="font-medium text-gray-800 flex items-center">
                <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
                AI-Generated Summary
              </h3>
              <p className="text-sm mt-2">
                In Q2 2023, the company experienced robust 15% revenue growth compared to Q1, 
                primarily attributed to the successful launch of a new product line. The quarter 
                was marked by market expansion and strong performance across key business segments.
              </p>
            </div>
            
            <p className="text-sm text-gray-500 italic">
              Type /command to access AI assistance features.
            </p>
          </div>
        );
      }, 500);
    } else if (command.name === 'Generate Key Points') {
      toast.success("Generating key points");
      setTimeout(() => {
        setEditorContent(
          <div className="space-y-3">
            <h1 className="text-xl font-bold">Quarterly Report: Q2 2023</h1>
            <p>This document provides an overview of our company's performance in Q2 2023.</p>
            <h2 className="text-lg font-semibold mt-4">Executive Summary</h2>
            <p>
              The second quarter of 2023 saw significant growth in our key markets. Revenue 
              increased by 15% compared to Q1, driven primarily by the launch of our new 
              product line.
            </p>
            
            <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
              <h3 className="font-medium text-gray-800 flex items-center">
                <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
                AI-Generated Key Points
              </h3>
              <ul className="text-sm mt-2 list-disc pl-5 space-y-1">
                <li>15% revenue growth in Q2 compared to previous quarter</li>
                <li>New product line launch was the primary growth driver</li>
                <li>Significant expansion in key markets</li>
                <li>Positive trajectory expected to continue in Q3</li>
              </ul>
            </div>
            
            <p className="text-sm text-gray-500 italic">
              Type /command to access AI assistance features.
            </p>
          </div>
        );
      }, 500);
    } else if (command.name === 'Expand Section') {
      toast.success("Expanding document section");
      setTimeout(() => {
        setEditorContent(
          <div className="space-y-3">
            <h1 className="text-xl font-bold">Quarterly Report: Q2 2023</h1>
            <p>This document provides an overview of our company's performance in Q2 2023.</p>
            <h2 className="text-lg font-semibold mt-4">Executive Summary</h2>
            <p>
              The second quarter of 2023 saw significant growth in our key markets. Revenue 
              increased by 15% compared to Q1, driven primarily by the launch of our new 
              product line.
            </p>
            
            <div className="bg-gray-50 p-3 border border-gray-200 rounded-md mt-2">
              <h3 className="font-medium text-gray-800 flex items-center">
                <Sparkles className="h-4 w-4 text-architect-purple mr-2" />
                AI-Generated Expansion
              </h3>
              <div className="text-sm mt-2 space-y-2">
                <p>
                  The second quarter of 2023 marked a significant milestone in our company's growth trajectory. 
                  We witnessed a remarkable 15% increase in revenue compared to Q1, bringing our total quarterly 
                  revenue to $28.5 million.
                </p>
                <p>
                  This growth was primarily fueled by the successful launch of our NextGen product line, which 
                  exceeded initial sales projections by 22%. The product received overwhelmingly positive feedback 
                  from customers, with a satisfaction rating of 4.8/5.
                </p>
                <p>
                  Key markets, particularly in North America and Europe, showed exceptional performance with 
                  year-over-year growth rates of 18% and 14% respectively. Our expansion into APAC is proceeding 
                  according to plan, with new partnerships established in Singapore and Australia.
                </p>
              </div>
            </div>
            
            <p className="text-sm text-gray-500 italic">
              Type /command to access AI assistance features.
            </p>
          </div>
        );
      }, 500);
    } else {
      toast.success(`Executing: ${command.name}`);
      setTimeout(() => {
        const testCase = testCases.find(test => test.title === command.name);
        if (testCase) {
          handleRunTestCase(testCase.id);
        }
      }, 300);
    }
  };

  const handleRunTestCase = (testCaseId: string) => {
    setCurrentTestCase(testCaseId);
    const testCase = testCases.find(test => test.id === testCaseId);
    
    if (testCase) {
      toast.success(`Running test case: ${testCase.title}`);
      
      setEditorContent(
        <div className="space-y-3">
          <h1 className="text-xl font-bold">Quarterly Report: Q2 2023</h1>
          <p>This document provides an overview of our company's performance in Q2 2023.</p>
          <h2 className="text-lg font-semibold mt-4">Executive Summary</h2>
          <p>
            The second quarter of 2023 saw significant growth in our key markets. Revenue 
            increased by 15% compared to Q1, driven primarily by the launch of our new 
            product line.
          </p>
          
          <div className="p-2 bg-blue-50 border border-blue-200 rounded text-blue-800">
            <span className="font-mono">{testCase.prompt}</span>
          </div>
        </div>
      );
      
      setTimeout(() => {
        setEditorContent(
          <div className="space-y-3">
            <h1 className="text-xl font-bold">Quarterly Report: Q2 2023</h1>
            <p>This document provides an overview of our company's performance in Q2 2023.</p>
            <h2 className="text-lg font-semibold mt-4">Executive Summary</h2>
            <p>
              The second quarter of 2023 saw significant growth in our key markets. Revenue 
              increased by 15% compared to Q1, driven primarily by the launch of our new 
              product line.
            </p>
            
            {testCase.result}
            
            <p className="text-sm text-gray-500 italic mt-4">
              Type /command to access AI assistance features.
            </p>
          </div>
        );
      }, 800);
    }
  };

  const handleNavigateTestCase = (direction: 'prev' | 'next') => {
    if (!currentTestCase) {
      handleRunTestCase('1');
      return;
    }
    
    const currentIndex = testCases.findIndex(test => test.id === currentTestCase);
    if (currentIndex === -1) return;
    
    let newIndex;
    if (direction === 'next') {
      newIndex = (currentIndex + 1) % testCases.length;
    } else {
      newIndex = (currentIndex - 1 + testCases.length) % testCases.length;
    }
    
    handleRunTestCase(testCases[newIndex].id);
  };
  
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navigation />
      
      <div className="flex-1 flex flex-col">
        <div className="bg-white border-b border-gray-200 py-8 px-6">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-3xl font-bold text-architect-navy">Architect Ask AI Edit Demo</h1>
            <p className="text-lg text-gray-600 mt-2">
              Experience real-time document editing powered by advanced AI.
            </p>
          </div>
        </div>

        <div className="bg-white border-b border-gray-200 py-4 px-6 shadow-sm">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-xl font-semibold text-architect-navy">Test Cases</h2>
              <div className="flex space-x-2">
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={() => handleNavigateTestCase('prev')}
                  className="h-8"
                >
                  <ChevronLeft className="h-4 w-4 mr-1" />
                  Previous
                </Button>
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={() => handleNavigateTestCase('next')}
                  className="h-8"
                >
                  Next
                  <ChevronRight className="h-4 w-4 ml-1" />
                </Button>
              </div>
            </div>
            <div className="flex overflow-x-auto pb-3 scrollbar-hide">
              <div className="flex space-x-3">
                {testCases.map(testCase => (
                  <div 
                    key={testCase.id}
                    onClick={() => handleRunTestCase(testCase.id)}
                    className={`flex-shrink-0 flex flex-col items-center w-32 p-3 rounded-lg cursor-pointer border transition-all ${
                      currentTestCase === testCase.id 
                        ? 'border-architect-purple bg-architect-lightPurple text-architect-purple' 
                        : 'border-gray-200 hover:bg-gray-50 text-gray-700'
                    }`}
                  >
                    <testCase.icon className={`h-6 w-6 mb-2 ${
                      currentTestCase === testCase.id ? 'text-architect-purple' : 'text-gray-500'
                    }`} />
                    <span className="text-xs font-medium text-center line-clamp-2">{testCase.title}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      
        <div className="flex flex-1 overflow-hidden">
          <div className="w-64 bg-white border-r border-gray-200 overflow-y-auto">
            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-medium text-gray-700">Documents</h2>
                <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                  <FolderPlus className="h-4 w-4" />
                </Button>
              </div>
              
              <div className="space-y-1">
                {documents.map(doc => (
                  <div
                    key={doc.id}
                    className={`flex items-center px-2 py-1.5 rounded-md text-sm cursor-pointer ${
                      doc.selected ? 'bg-architect-lightPurple text-architect-purple' : 'text-gray-700 hover:bg-gray-100'
                    }`}
                    onClick={() => handleDocumentSelect(doc.id)}
                  >
                    <File className="h-4 w-4 mr-2 flex-shrink-0" />
                    <span className="truncate">{doc.name}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <Separator />
            
            <div className="p-4">
              <h3 className="text-xs font-medium text-gray-500 mb-3">RECENT UPLOADS</h3>
              
              <Collapsible className="w-full">
                <CollapsibleTrigger className="flex items-center text-sm text-gray-700 hover:text-gray-900">
                  <span className="flex-1 text-left">Yesterday</span>
                </CollapsibleTrigger>
                <CollapsibleContent className="pt-1 pl-2">
                  <div className="space-y-1">
                    <div className="flex items-center px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded cursor-pointer">
                      <File className="h-3 w-3 mr-2 flex-shrink-0" />
                      <span className="truncate">Sales Forecast.xlsx</span>
                    </div>
                    <div className="flex items-center px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded cursor-pointer">
                      <File className="h-3 w-3 mr-2 flex-shrink-0" />
                      <span className="truncate">Client Presentation.pptx</span>
                    </div>
                  </div>
                </CollapsibleContent>
              </Collapsible>
            </div>
          </div>
          
          <div className="flex-1 flex flex-col overflow-hidden">
            <div className="bg-white border-b border-gray-200 p-2">
              <div className="flex flex-wrap items-center gap-1">
                {formatOptions.map(option => (
                  <Button 
                    key={option.id}
                    variant="ghost" 
                    size="sm" 
                    className="h-8 w-8 p-0"
                    onClick={() => handleFormatClick(option.label)}
                  >
                    <option.icon className="h-4 w-4" />
                  </Button>
                ))}
              </div>
            </div>
            
            <div className="flex-1 overflow-auto p-6" onClick={handleEditorFocus}>
              <div 
                className="max-w-3xl mx-auto bg-white shadow-sm border border-gray-200 rounded-lg p-6 min-h-[500px] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                contentEditable={true}
                ref={editorRef}
                suppressContentEditableWarning={true}
              >
                {editorContent}
              </div>
            </div>
            
            {showCommandMenu && (
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg shadow-xl border border-gray-200 w-80 z-50">
                <div className="p-2 border-b border-gray-100">
                  <div className="flex items-center gap-2 px-3 py-1.5">
                    <Command className="h-4 w-4 text-gray-400" />
                    <Input
                      value={commandInput}
                      onChange={(e) => setCommandInput(e.target.value)}
                      className="flex-1 border-none shadow-none focus-visible:ring-0 h-7 px-0 py-0"
                      placeholder="Type a command..."
                    />
                  </div>
                </div>
                <div className="p-1 max-h-60 overflow-auto">
                  {commands
                    .filter(cmd => 
                      commandInput ? cmd.name.toLowerCase().includes(commandInput.toLowerCase()) : true
                    )
                    .map(command => (
                      <div
                        key={command.id}
                        className="flex items-center gap-2 px-3 py-1.5 text-sm rounded-md hover:bg-gray-100 cursor-pointer"
                        onClick={() => executeCommand(command)}
                      >
                        <command.icon className="h-4 w-4 text-gray-500" />
                        <div className="flex-1">
                          <div className="font-medium">{command.name}</div>
                          <div className="text-xs text-gray-500">{command.description}</div>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            )}
          </div>
          
          <div className="hidden md:block w-64 bg-white border-l border-gray-200 p-4 overflow-y-auto">
            <h2 className="text-sm font-medium text-gray-700 mb-3">AI Assistant</h2>
            
            <Card className="shadow-sm mb-4">
              <CardContent className="p-3">
                <h3 className="text-xs font-medium flex items-center text-gray-800">
                  <Sparkles className="h-3.5 w-3.5 text-architect-purple mr-1.5" />
                  Using Commands
                </h3>
                <div className="mt-2 text-xs">
                  <p className="text-gray-600 mb-2">
                    Type <span className="font-mono bg-gray-100 px-1 rounded text-gray-800">/</span> in the editor to access AI commands.
                  </p>
                  <p className="text-gray-600">
                    You can also use <span className="font-mono bg-gray-100 px-1 rounded text-gray-800">Cmd+K</span> or <span className="font-mono bg-gray-100 px-1 rounded text-gray-800">Ctrl+K</span> to open the command menu.
                  </p>
                </div>
              </CardContent>
            </Card>
            
            <Card className="shadow-sm">
              <CardContent className="p-3">
                <h3 className="text-xs font-medium flex items-center text-gray-800">
                  <Sparkles className="h-3.5 w-3.5 text-architect-purple mr-1.5" />
                  Suggested Actions
                </h3>
                <div className="mt-2 text-xs space-y-1.5">
                  {commands.slice(0, 4).map(command => (
                    <div 
                      key={command.id}
                      className="flex items-center gap-1.5 text-gray-700 hover:text-architect-purple cursor-pointer"
                      onClick={() => executeCommand(command)}
                    >
                      <command.icon className="h-3 w-3" />
                      <span>{command.name}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
            
            {currentTestCase && (
              <Card className="shadow-sm mt-4">
                <CardContent className="p-3">
                  <h3 className="text-xs font-medium flex items-center text-gray-800">
                    <Sparkles className="h-3.5 w-3.5 text-architect-purple mr-1.5" />
                    Current Test Case
                  </h3>
                  <div className="mt-2 text-xs">
                    <p className="font-medium">
                      {testCases.find(t => t.id === currentTestCase)?.title}
                    </p>
                    <p className="text-gray-600 mt-1">
                      {testCases.find(t => t.id === currentTestCase)?.description}
                    </p>
                    <div className="mt-2 pt-2 border-t border-gray-100">
                      <p className="text-gray-500 text-xs">
                        Try typing: <span className="font-mono bg-gray-100 px-1 rounded text-gray-800">
                          {testCases.find(t => t.id === currentTestCase)?.prompt}
                        </span>
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CursorDemo;
