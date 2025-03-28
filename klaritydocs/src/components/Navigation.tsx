
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutGrid, FileText, Edit3 } from 'lucide-react';
import { Button } from './ui/button';

const Navigation = () => {
  const location = useLocation();
  
  return (
    <nav className="w-full bg-white shadow-sm py-4 px-6">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between">
        <Link to="/" className="flex items-center space-x-2 mb-4 sm:mb-0">
          <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-architect-purple text-white">
            <LayoutGrid size={20} />
          </div>
          <span className="text-xl font-bold text-architect-navy">Architect</span>
        </Link>
        
        <div className="flex flex-wrap items-center justify-center space-x-2 sm:space-x-4">
          <Link to="/">
            <Button 
              variant={location.pathname === '/' ? "default" : "ghost"}
              className="flex items-center space-x-1"
            >
              <LayoutGrid size={16} />
              <span>Home</span>
            </Button>
          </Link>
          
          <Link to="/perplexity">
            <Button 
              variant={location.pathname === '/perplexity' ? "default" : "ghost"}
              className="flex items-center space-x-1"
            >
              <FileText size={16} />
              <span>Perplexity</span>
            </Button>
          </Link>
          
          <Link to="/cursor">
            <Button 
              variant={location.pathname === '/cursor' ? "default" : "ghost"}
              className="flex items-center space-x-1"
            >
              <Edit3 size={16} />
              <span>Cursor</span>
            </Button>
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
