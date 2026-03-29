'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { login, registerUser } from '@/lib/api';

export default function LoginPage() {
    const router = useRouter();
    const [mode, setMode] = useState<'login' | 'register'>('login');
    const [email, setEmail] = useState('demo@demo.com');
    const [username, setUsername] = useState('demo');
    const [password, setPassword] = useState('demo123');
    const [fullName, setFullName] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            if (mode === 'login') {
                await login(username, password);
            } else {
                await registerUser({ email, username, password, full_name: fullName });
                await login(username, password);
            }
            router.push('/');
        } catch (err: any) {
            setError(err.message || 'Something went wrong');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center px-4">
            <div className="bg-white w-full max-w-md shadow-xl rounded-2xl p-8 border border-gray-100">
                <div className="text-center mb-6">
                    <div className="mx-auto w-14 h-14 rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center text-white text-2xl font-bold">
                        A
                    </div>
                    <h1 className="text-2xl font-semibold text-gray-900 mt-3">Advisory Board AI</h1>
                    <p className="text-sm text-gray-500">Secure {mode === 'login' ? 'login' : 'signup'} to continue</p>
                </div>

                <div className="flex space-x-2 mb-6 bg-gray-100 rounded-xl p-1">
                    <button
                        className={`flex-1 py-2 rounded-lg text-sm font-medium ${mode === 'login' ? 'bg-white shadow text-gray-900' : 'text-gray-500'}`}
                        onClick={() => setMode('login')}
                    >
                        Login
                    </button>
                    <button
                        className={`flex-1 py-2 rounded-lg text-sm font-medium ${mode === 'register' ? 'bg-white shadow text-gray-900' : 'text-gray-500'}`}
                        onClick={() => setMode('register')}
                    >
                        Register
                    </button>
                </div>

                <form className="space-y-4" onSubmit={handleSubmit}>
                    {mode === 'register' && (
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                            <input
                                type="text"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                                className="w-full p-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder="Your name"
                            />
                        </div>
                    )}

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full p-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="you@example.com"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="w-full p-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="demo"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full p-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="••••••••"
                            required
                        />
                    </div>

                    {error && <p className="text-sm text-red-600 bg-red-50 p-2 rounded-lg">{error}</p>}

                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-full py-3 rounded-lg text-white font-medium ${loading
                            ? 'bg-gray-400 cursor-not-allowed'
                            : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-lg'}
            `}
                    >
                        {loading ? 'Working...' : mode === 'login' ? 'Login' : 'Create account'}
                    </button>
                </form>

                <p className="text-xs text-gray-500 mt-4 text-center">
                    Demo credentials: demo@demo.com / demo123
                </p>
            </div>
        </div>
    );
}
