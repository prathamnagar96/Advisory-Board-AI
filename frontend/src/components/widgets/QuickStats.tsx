import { Activity, Folder, AlertTriangle, TrendingUp, MessageCircle } from 'lucide-react';

export type QuickStatsData = {
  documentsUploaded: number;
  queriesAsked: number;
  remindersPending: number;
  taxSavingsEstimate: number;
};

export default function QuickStats({ data, loading }: { data?: QuickStatsData; loading?: boolean }) {
  const stats = data || {
    documentsUploaded: 12,
    queriesAsked: 28,
    remindersPending: 5,
    taxSavingsEstimate: 42000
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
        <Activity className="h-5 w-5 text-blue-600" />
        Quick Stats
        {loading && <span className="text-xs font-normal text-gray-400 ml-2">Loading...</span>}
      </h2>

      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Documents Uploaded</h3>
            <p className="text-2xl font-bold text-gray-900 mt-1">{stats.documentsUploaded}</p>
            <Folder className="h-4 w-4 text-indigo-500 mt-2" />
          </div>

          <div className="bg-green-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Queries Asked</h3>
            <p className="text-2xl font-bold text-gray-900 mt-1">{stats.queriesAsked}</p>
            <MessageCircle className="h-4 w-4 text-green-500 mt-2" />
          </div>

          <div className="bg-yellow-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Reminders Pending</h3>
            <p className="text-2xl font-bold text-gray-900 mt-1">{stats.remindersPending}</p>
            <AlertTriangle className="h-4 w-4 text-amber-500 mt-2" />
          </div>

          <div className="bg-purple-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Tax Savings Estimate</h3>
            <p className="text-2xl font-bold text-gray-900 mt-1">₹{stats.taxSavingsEstimate.toLocaleString()}</p>
            <TrendingUp className="h-4 w-4 text-purple-500 mt-2" />
          </div>
        </div>
      </div>
    </div>
  );
}