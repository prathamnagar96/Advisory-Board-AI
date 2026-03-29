import Link from 'next/link';
import {
  BarChart3,
  FileText,
  Bell,
  MessageCircle,
  Settings,
  LogOut,
  HelpCircle
} from 'lucide-react';

export default function Sidebar({ className }: { className?: string }) {
  return (
    <aside className={`space-y-6 pt-6 ${className || ''}`}>
      {/* Navigation Menu */}
      <nav className="space-y-2">
        <Link href="/" className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors">
          <BarChart3 className="h-5 w-5" />
          <span className="text-sm font-medium">Dashboard</span>
        </Link>
        <Link href="/documents" className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors">
          <FileText className="h-5 w-5" />
          <span className="text-sm font-medium">Documents</span>
        </Link>
        <Link href="/reminders" className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors">
          <Bell className="h-5 w-5" />
          <span className="text-sm font-medium">Reminders</span>
        </Link>
        <Link href="/chat" className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors">
          <MessageCircle className="h-5 w-5" />
          <span className="text-sm font-medium">Chat Advisor</span>
        </Link>
      </nav>

      {/* Settings and Help */}
      <div className="border-t pt-4">
        <Link href="/settings" className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-500 hover:bg-gray-50 hover:text-gray-900 transition-colors">
          <Settings className="h-5 w-5" />
          <span className="text-sm">Settings</span>
        </Link>
        <Link href="/help" className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-500 hover:bg-gray-50 hover:text-gray-900 transition-colors">
          <HelpCircle className="h-5 w-5" />
          <span className="text-sm">Help & Support</span>
        </Link>
        <Link href="/logout" className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-500 hover:bg-gray-50 hover:text-gray-900 transition-colors">
          <LogOut className="h-5 w-5" />
          <span className="text-sm">Logout</span>
        </Link>
      </div>
    </aside>
  );
}