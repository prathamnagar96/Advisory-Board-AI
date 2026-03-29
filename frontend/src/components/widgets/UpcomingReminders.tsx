import { Bell, Calendar, CheckCircle, AlertTriangle } from 'lucide-react';

export interface ReminderItem {
  id: string;
  title: string;
  description: string;
  dueDate: string;
  priority: 'low' | 'medium' | 'high';
  type: string;
}

const fallbackReminders: ReminderItem[] = [
  {
    id: "rem_001",
    title: "File Income Tax Return",
    description: "File your annual income tax return for FY 2023-24",
    dueDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
    priority: "high",
    type: "tax_filing"
  },
  {
    id: "rem_002",
    title: "Submit Investment Proofs",
    description: "Submit Section 80C investment proofs to employer",
    dueDate: new Date(Date.now() + 15 * 24 * 60 * 60 * 1000).toISOString(),
    priority: "high",
    type: "compliance"
  }
];

const getPriorityColor = (priority: 'low' | 'medium' | 'high') => {
  switch (priority) {
    case 'low': return 'bg-green-50 text-green-800';
    case 'medium': return 'bg-yellow-50 text-yellow-800';
    case 'high': return 'bg-red-50 text-red-800';
    default: return 'bg-gray-50 text-gray-800';
  }
};

const getTypeIcon = (type: string) => {
  switch (type) {
    case 'tax_filing': return Bell;
    case 'tax_payment': return AlertTriangle;
    case 'investment_review': return Calendar;
    case 'compliance': return CheckCircle;
    default: return Bell;
  }
};

export default function UpcomingReminders({ reminders, loading }: { reminders?: ReminderItem[]; loading?: boolean }) {
  const upcomingReminders = reminders && reminders.length ? reminders : fallbackReminders;
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
        <Bell className="h-5 w-5 text-blue-600" />
        Upcoming Reminders
        {loading && <span className="text-xs text-gray-400 ml-2">Loading...</span>}
      </h2>

      <div className="space-y-4">
        {upcomingReminders.map((reminder) => (
          <div key={reminder.id} className="p-4 border rounded-lg">
            {(() => {
              const ReminderIcon = getTypeIcon(reminder.type);
              return (
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 flex items-center justify-center rounded-full bg-blue-50 flex-shrink-0">
                    <ReminderIcon className="h-4 w-4 text-blue-600" />
                  </div>
                  <div className="flex-1 space-y-2">
                    <div className="flex justify-between items-start">
                      <h3 className="text-sm font-medium text-gray-900">{reminder.title}</h3>
                      <span className={`px-2 py-0.5 text-xs rounded ${getPriorityColor(reminder.priority)}`}>
                        {reminder.priority}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500">{reminder.description}</p>
                    <div className="flex items-center text-xs text-gray-500 space-x-3">
                      <Calendar className="h-4 w-4" />
                      <span>{new Date(reminder.dueDate).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
              );
            })()}
          </div>
        ))}
      </div>

      {upcomingReminders.length === 0 && (
        <div className="text-center py-8">
          <p className="text-gray-500">No upcoming reminders</p>
        </div>
      )}
    </div>
  );
}