'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Upload, Trash2, FileText, Search } from 'lucide-react';
import { deleteDocument, fetchDocuments, uploadDocument, getToken } from '@/lib/api';

type Doc = {
  id: string;
  filename: string;
  file_type: string;
  size: number;
  processed: boolean;
  upload_timestamp: string;
};

export default function DocumentsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [documents, setDocuments] = useState<Doc[]>([]);

  useEffect(() => {
    if (!getToken()) {
      setError('Login to upload and view documents');
      setLoading(false);
      return;
    }
    loadDocs();
  }, []);

  const loadDocs = async () => {
    try {
      setLoading(true);
      const res = await fetchDocuments();
      setDocuments(res.documents || []);
    } catch (err: any) {
      setError(err.message || 'Could not load documents');
    } finally {
      setLoading(false);
    }
  };

  const filteredDocuments = documents.filter(doc =>
    doc.filename.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setUploading(true);
    try {
      await uploadDocument(selectedFile);
      setSelectedFile(null);
      await loadDocs();
    } catch (err: any) {
      setError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (docId: string) => {
    try {
      await deleteDocument(docId);
      await loadDocs();
    } catch (err: any) {
      setError(err.message || 'Delete failed');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Document Management</h1>
        <div className="flex items-center space-x-3 mt-4 lg:mt-0">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search documents..."
            className="w-full lg:w-48 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
            className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-colors flex items-center space-x-2 text-sm font-medium disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            <Upload className="h-4 w-4" />
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      </div>

      {/* Upload Section */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload New Document</h2>
        <div className="space-y-4">
          <label className="flex flex-col space-y-2">
            <span className="text-sm font-medium text-gray-700">Select File</span>
            <input
              type="file"
              accept=".pdf,.jpg,.jpeg,.png,.doc,.docx,.txt"
              onChange={handleFileChange}
              className="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            {selectedFile && (
              <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <FileText className="h-5 w-5 text-blue-500" />
                <div>
                  <p className="text-sm font-medium text-gray-900">{selectedFile.name}</p>
                  <p className="text-xs text-gray-500">
                    {(selectedFile.size / 1024).toFixed(1)} KB
                  </p>
                </div>
              </div>
            )}
          </label>

          <button
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
            className={`w-full px-4 py-3 rounded-lg text-white font-medium ${!selectedFile || uploading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-colors'
              }`}
          >
            {uploading ? 'Uploading...' : 'Upload Document'}
          </button>
        </div>
      </div>

      {/* Documents List */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
          <FileText className="h-5 w-5 text-blue-600" />
          My Documents ({filteredDocuments.length})
        </h2>

        {error && <p className="text-sm text-red-600 mb-2">{error}</p>}
        {loading ? (
          <div className="text-gray-500">Loading documents...</div>
        ) : filteredDocuments.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">No documents found</p>
            {searchQuery && (
              <p className="mt-2 text-sm text-gray-400">
                Try adjusting your search filter
              </p>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            {filteredDocuments.map((doc) => (
              <div key={doc.id} className="p-4 border rounded-lg flex items-start space-x-4">
                <div className="w-10 h-10 flex items-center justify-center rounded-lg bg-blue-50 flex-shrink-0">
                  {doc.file_type.startsWith('image/') ? (
                    <img
                      src={`/placeholder.png`} // In real app, would be thumbnail
                      alt="Preview"
                      className="h-6 w-6 object-cover rounded"
                    />
                  ) : (
                    <FileText className="h-5 w-5 text-blue-500" />
                  )}
                </div>
                <div className="flex-1 space-y-2">
                  <div className="flex justify-between items-start">
                    <h3 className="text-sm font-medium text-gray-900">{doc.filename}</h3>
                    <span className={`px-2 py-0.5 text-xs rounded ${doc.processed ? 'bg-green-50 text-green-800' : 'bg-yellow-50 text-yellow-800'
                      }`}>
                      {doc.processed ? 'Processed' : 'Pending'}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500">
                    {(doc.size / 1024).toFixed(1)} KB •
                    {new Date(doc.upload_timestamp).toLocaleDateString()}
                  </p>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <button
                    onClick={() => {/* View document */ }}
                    className="p-1 rounded hover:bg-gray-100 text-gray-500"
                  >
                    <Search className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(doc.id)}
                    className="p-1 rounded hover:bg-red-50 hover:text-red-600 text-red-500"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}