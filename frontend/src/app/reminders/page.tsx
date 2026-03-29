'use client';

import { useEffect, useState } from 'react';
import { Bell, Plus, Check } from 'lucide-react';
import { createReminder, completeReminder, fetchReminders, getToken, type Reminder } from '@/lib/api';

export default function RemindersPage() {
    const [reminders, setReminders] = useState<Reminder[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [newTitle, setNewTitle] = useState('');
    const [newDate, setNewDate] = useState('');

    useEffect(() => {
        if (!getToken()) {
            setError('Login to manage reminders');
            setLoading(false);
            return;
        }
        load();
    }, []);

    const load = async () => {
        try {
            setLoading(true);
            const res = await fetchReminders();
            setReminders(res.reminders || []);
        } catch (err: any) {
            setError(err.message || 'Failed to load reminders');
        } finally {
            setLoading(false);
        }
    };

    const addReminder = async () => {
        if (!newTitle || !newDate) return;
        try {
            await createReminder({
                title: newTitle,
                description: '',
                reminder_type: 'custom',
                due_date: newDate,
                priority: 'medium',
                is_recurring: false,
            });
            setNewTitle('');
            setNewDate('');
            await load();
        } catch (err: any) {
            setError(err.message || 'Could not create reminder');
        }
    };

    const markDone = async (id: string) => {
        try {
            await completeReminder(id);
            await load();
        } catch (err: any) {
            setError(err.message || 'Failed to update reminder');
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                    <Bell className="h-5 w-5 text-blue-600" />
                    <h1 className="text-2xl font-bold text-gray-900">Reminders</h1>
                </div>
            </div>

            <div className="bg-white border rounded-xl p-4 shadow-sm space-y-3">
                <h2 className="text-sm font-semibold text-gray-800">Quick add</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <input
                        className="border rounded-lg p-2"
                        placeholder="Title"
                        value={newTitle}
                        onChange={(e) => setNewTitle(e.target.value)}
                    />
                    <input
                        className="border rounded-lg p-2"
                        type="date"
                        value={newDate}
                        onChange={(e) => setNewDate(e.target.value)}
                    />
                    <button
                        onClick={addReminder}
                        className="inline-flex items-center justify-center px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg"
                    >
                        <Plus className="h-4 w-4 mr-2" /> Add reminder
                    </button>
                </div>
            </div>

            {error && <p className="text-sm text-red-600">{error}</p>}
            {loading ? (
                <p className="text-gray-500">Loading reminders...</p>
            ) : reminders.length === 0 ? (
                <p className="text-gray-500">No reminders yet</p>
            ) : (
                <div className="space-y-3">
                    {reminders.map((r) => (
                        <div key={r.id} className="p-4 border rounded-lg bg-white flex items-center justify-between">
                            <div>
                                <p className="font-medium text-gray-900">{r.title}</p>
                                <p className="text-sm text-gray-500">Due {new Date(r.due_date).toLocaleDateString()}</p>
                            </div>
                            <button
                                onClick={() => markDone(r.id)}
                                className={`flex items-center px-3 py-1 rounded-lg text-sm ${r.is_completed ? 'bg-green-100 text-green-700' : 'bg-blue-50 text-blue-700'}`}
                            >
                                <Check className="h-4 w-4 mr-1" /> {r.is_completed ? 'Completed' : 'Mark done'}
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
