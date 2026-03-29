import { BarChart3, TrendingUp, ArrowDown, Wallet, PiggyBank } from 'lucide-react';

export type FinancialOverviewData = {
  totalIncome: number;
  totalDeductions: number;
  taxLiability: number;
  netIncome: number;
  assessmentYear: string;
};

export default function FinancialOverview({ data, loading }: { data?: FinancialOverviewData; loading?: boolean }) {
  const financialData = data || {
    totalIncome: 850000,
    totalDeductions: 185000,
    taxLiability: 95000,
    netIncome: 570000,
    assessmentYear: "2025-26"
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
        <Wallet className="h-5 w-5 text-blue-600" />
        Financial Overview
        {loading && <span className="text-xs font-normal text-gray-400 ml-2">Loading...</span>}
      </h2>

      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Total Income</h3>
            <p className="text-2xl font-bold text-gray-900 mt-1">₹{financialData.totalIncome.toLocaleString()}</p>
            <TrendingUp className="h-4 w-4 text-green-500 mt-2" />
          </div>

          <div className="bg-green-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Total Deductions</h3>
            <p className="text-2xl font-bold text-gray-900 mt-1">₹{financialData.totalDeductions.toLocaleString()}</p>
            <ArrowDown className="h-4 w-4 text-red-500 mt-2" />
          </div>

          <div className="bg-red-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Tax Liability</h3>
            <p className="text-2xl font-bold text-gray-900 mt-1">₹{financialData.taxLiability.toLocaleString()}</p>
            <BarChart3 className="h-4 w-4 text-indigo-500 mt-2" />
          </div>

          <div className="bg-purple-50 p-4 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Net Income</h3>
            <p className="text-2xl font-bold text-gray-900 mt-1">₹{financialData.netIncome.toLocaleString()}</p>
            <PiggyBank className="h-4 w-4 text-yellow-500 mt-2" />
          </div>
        </div>

        <div className="mt-4 pt-3 border-t border-gray-100 text-sm text-gray-500">
          Assessment Year: {financialData.assessmentYear}
        </div>
      </div>
    </div>
  );
}