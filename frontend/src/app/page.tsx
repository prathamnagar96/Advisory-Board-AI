'use client';

import { useEffect, useState } from 'react';
import Header from '@/components/layout/Header';
import Sidebar from '@/components/layout/Sidebar';
import FinancialOverview, { FinancialOverviewData } from '@/components/widgets/FinancialOverview';
import QuickStats, { QuickStatsData } from '@/components/widgets/QuickStats';
import RecentActivity, { RecentActivityItem } from '@/components/widgets/RecentActivity';
import UpcomingReminders, { ReminderItem } from '@/components/widgets/UpcomingReminders';
import TaxTips from '@/components/widgets/TaxTips';
import ChatInterface from '@/components/ChatInterface';
import { fetchDashboard, fetchHealthScore } from '@/lib/api';
import { getToken } from '@/lib/api';
import Link from 'next/link';

export default function Home() {
  const [financialOverview, setFinancialOverview] = useState<FinancialOverviewData | null>(null);
  const [quickStats, setQuickStats] = useState<QuickStatsData | null>(null);
  const [activities, setActivities] = useState<RecentActivityItem[]>([]);
  const [reminders, setReminders] = useState<ReminderItem[]>([]);
  const [healthScore, setHealthScore] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      setError('Please login to see your live data');
      setLoading(false);
      return;
    }

    async function load() {
      try {
        const dashboard = await fetchDashboard();
        setFinancialOverview({
          totalIncome: dashboard.financial_overview.total_income,
          totalDeductions: dashboard.financial_overview.total_deductions,
          taxLiability: dashboard.financial_overview.tax_liability,
          netIncome: dashboard.financial_overview.net_income,
          assessmentYear: dashboard.financial_overview.assessment_year,
        });
        setQuickStats({
          documentsUploaded: dashboard.quick_stats.documents_uploaded,
          queriesAsked: dashboard.quick_stats.queries_asked,
          remindersPending: dashboard.quick_stats.reminders_pending,
          taxSavingsEstimate: dashboard.quick_stats.tax_savings_estimate,
        });
        setActivities(dashboard.recent_activities || []);
        setReminders(
          (dashboard.upcoming_reminders || []).map((r: any) => ({
            id: r.id,
            title: r.title,
            description: r.description,
            dueDate: r.due_date,
            priority: r.priority,
            type: r.type,
          }))
        );

        const score = await fetchHealthScore();
        setHealthScore(score);
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="min-h-screen flex bg-gray-50">
      <Sidebar className="w-64 bg-white border-r border-gray-200" />

      <div className="flex-1 flex flex-col">
        <Header className="h-16 bg-white border-b border-gray-200 flex items-center px-6" />

        <div className="flex-1 overflow-y-auto">
          <div className="mx-auto w-full max-w-7xl p-6 lg:p-10 space-y-6">
            {error && (
              <div className="bg-amber-50 border border-amber-200 text-amber-800 p-3 rounded-lg flex items-center justify-between">
                <span>{error}</span>
                <Link href="/login" className="text-sm font-semibold text-blue-600 underline">Go to login</Link>
              </div>
            )}

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
              <div className="xl:col-span-2">
                <FinancialOverview data={financialOverview || undefined} loading={loading} />
              </div>
              <QuickStats data={quickStats || undefined} loading={loading} />
            </div>

            {healthScore && (
              <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-500 text-white rounded-2xl shadow-lg p-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div>
                  <p className="text-sm uppercase tracking-wide opacity-80">Financial health score</p>
                  <p className="text-4xl font-bold">{healthScore.score}/100</p>
                  <p className="text-sm opacity-90 mt-1">{healthScore.level} • updated {new Date(healthScore.assessment_date).toLocaleTimeString()}</p>
                  <div className="mt-3 flex flex-wrap gap-2 text-xs">
                    {Object.entries(healthScore.factors || {}).map(([k, v]) => (
                      <span key={k} className="bg-white/15 px-3 py-1 rounded-full">{k.replace('_', ' ')}: {v}</span>
                    ))}
                  </div>
                </div>
                <div className="text-left md:text-right w-full md:w-auto">
                  <p className="text-sm mb-2">Top tips</p>
                  <ul className="space-y-2 text-sm">
                    {healthScore.recommendations?.map((tip: string, idx: number) => (
                      <li key={idx} className="bg-white/15 px-3 py-2 rounded-lg">{tip}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <RecentActivity activities={activities} loading={loading} />
              <UpcomingReminders reminders={reminders} loading={loading} />
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <TaxTips />
              <ChatInterface className="h-[460px]" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}