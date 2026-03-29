import Link from 'next/link';
import { Menu, Sun, Moon, User, Bell, Settings } from 'lucide-react';

export default function Header({ className }: { className?: string }) {
  return (
    <header className={`flex items-center justify-between ${className || ''}`}>
      {/* Logo and Brand */}
      <div className="flex items-center space-x-4">
        <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
          <span className="text-white text-xl">A</span>
        </div>
        <div>
          <h2 className="text-xl font-bold text-gray-900">Advisory Board AI</h2>
          <p className="text-sm text-gray-500">Your Personal Financial Advisor</p>
        </div>
      </div>

      {/* Navigation and User Controls */}
      <div className="flex items-center space-x-4">
        <Link href="/dashboard" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-100">
          Dashboard
        </Link>
        <Link href="/documents" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-100">
          Documents
        </Link>
        <Link href="/reminders" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-100">
          Reminders
        </Link>

        {/* User Profile and Actions */}
        <div className="relative">
          <button className="flex items-center space-x-2 bg-gray-50 px-3 py-2 rounded-md hover:bg-gray-100 transition-colors">
            <User className="h-4 w-4 text-gray-600" />
            <span className="text-sm font-medium text-gray-900">Welcome</span>
            <svg className="h-4 w-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          {/* Dropdown menu would go here in a full implementation */}
        </div>
      </div>
    </header>
  );
}