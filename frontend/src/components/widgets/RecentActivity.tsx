import { Clock, MessageCircle, FileText, CheckCircle, AlertTriangle } from 'lucide-react';

export type ActivityType = 'query' | 'document' | 'reminder';

export interface RecentActivityItem {
  id: string;
  type: ActivityType;
  title: string;
  timestamp: string; // ISO string
  metadata?: Record<string, any>;
}

const fallbackActivities: RecentActivityItem[] = [
  {
    id: "act_001",
    type: "query",
    title: "Asked about Section 80C deductions for ELSS investments",
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    metadata: { risk_level: "LOW", confidence: "HIGH" }
  },
  {
    id: "act_002",
    type: "document",
    title: "Uploaded Form 16 from ABC Company",
    timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
    metadata: { pages: 2, processed: true }
  }
];

const getActivityIcon = (type: ActivityType) => {
  switch (type) {
    case 'query': return MessageCircle;
    case 'document': return FileText;
    case 'reminder': return CheckCircle;
    default: return AlertTriangle;
  }
};

const getActivityTypeColor = (type: ActivityType) => {
  switch (type) {
    case 'query': return 'border-blue-500 bg-blue-50';
    case 'document': return 'border-green-500 bg-green-50';
    case 'reminder': return 'border-purple-500 bg-purple-50';
    default: return 'border-gray-500 bg-gray-50';
  }
};

export default function RecentActivity({ activities, loading }: { activities?: RecentActivityItem[]; loading?: boolean }) {
  const recentActivities = activities && activities.length ? activities : fallbackActivities;
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
        <Clock className="h-5 w-5 text-blue-600" />
        Recent Activity
        {loading && <span className="text-xs text-gray-400 ml-2">Loading...</span>}
      </h2>

      <div className="space-y-4">
        {recentActivities.map((activity) => (
          <div key={activity.id} className="p-3 border-l-4 rounded-r-md">
            {(() => {
              const ActivityIcon = getActivityIcon(activity.type);
              return (
                <div className="flex items-start space-x-3">
                  <div className={`w-8 h-8 flex items-center justify-center rounded-full ${getActivityTypeColor(activity.type)} flex-shrink-0`}>
                    <ActivityIcon className="h-4 w-4 text-blue-600" />
                  </div>
                  <div className="flex-1 space-y-1">
                    <h3 className="text-sm font-medium text-gray-900">{activity.title}</h3>
                    <p className="text-xs text-gray-500">
                      {new Date(activity.timestamp).toLocaleString()}
                    </p>
                    {activity.metadata && (
                      <div className="mt-1 text-xs text-gray-400 flex flex-wrap gap-2">
                        {Object.entries(activity.metadata).map(([key, value]) => (
                          <span key={key} className="px-2 py-0.5 text-xs rounded bg-gray-100">
                            {key}: {String(value)}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              );
            })()}
          </div>
        ))}
      </div>

      <div className="mt-4 pt-3 border-t border-gray-100 text-sm text-gray-500 text-center">
        Showing last {recentActivities.length} activities
      </div>
    </div>
  );
}