import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Database, Trash2, RefreshCw, AlertCircle } from 'lucide-react'

interface MemoryItem {
  id: string
  text: string
  metadata: {
    filename?: string
    chunk_id?: string
    type?: string
    agent_id?: string
    timestamp?: string
    [key: string]: any
  }
  filename?: string
  chunk_id?: string
}

const MemoryViewer: React.FC = () => {
  const [memories, setMemories] = useState<MemoryItem[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [deletingId, setDeletingId] = useState<string | null>(null)

  useEffect(() => {
    loadMemories()
  }, [])

  const loadMemories = async () => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await axios.get('/api/memory')
      setMemories(response.data)
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Failed to load memories')
    } finally {
      setIsLoading(false)
    }
  }

  const deleteMemory = async (id: string) => {
    setDeletingId(id)
    try {
      await axios.delete(`/api/memory/${id}`)
      setMemories(prev => prev.filter(memory => memory.id !== id))
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Failed to delete memory')
    } finally {
      setDeletingId(null)
    }
  }

  const clearAllMemories = async () => {
    if (!confirm('Are you sure you want to clear all memories? This action cannot be undone.')) {
      return
    }

    setIsLoading(true)
    try {
      await axios.delete('/api/memory')
      setMemories([])
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Failed to clear memories')
    } finally {
      setIsLoading(false)
    }
  }

  const formatTimestamp = (timestamp?: string) => {
    if (!timestamp) return 'Unknown'
    try {
      return new Date(timestamp).toLocaleString()
    } catch {
      return 'Invalid date'
    }
  }

  const truncateText = (text: string, maxLength: number = 200) => {
    if (text.length <= maxLength) return text
    return text.substring(0, maxLength) + '...'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Database className="w-6 h-6 text-blue-500" />
            <h2 className="text-lg font-medium text-gray-900">Memory Store</h2>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={loadMemories}
              disabled={isLoading}
              className="flex items-center px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
            <button
              onClick={clearAllMemories}
              disabled={isLoading || memories.length === 0}
              className="flex items-center px-3 py-2 text-sm bg-red-100 text-red-700 rounded-md hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50"
            >
              <Trash2 className="w-4 h-4 mr-2" />
              Clear All
            </button>
          </div>
        </div>
        
        <p className="text-sm text-gray-600 mt-2">
          {memories.length} memories stored in the vector database
        </p>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-2 text-red-600 mb-2">
            <AlertCircle className="w-5 h-5" />
            <h3 className="text-lg font-medium">Error</h3>
          </div>
          <p className="text-sm text-gray-600">{error}</p>
        </div>
      )}

      {/* Loading */}
      {isLoading && memories.length === 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            <span className="ml-2 text-gray-600">Loading memories...</span>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && memories.length === 0 && !error && (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-center py-8">
            <Database className="w-12 h-12 mx-auto text-gray-300 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Memories</h3>
            <p className="text-gray-600">
              Upload some documents or start chatting to populate the memory store.
            </p>
          </div>
        </div>
      )}

      {/* Memories List */}
      {memories.length > 0 && (
        <div className="space-y-4">
          {memories.map((memory) => (
            <div key={memory.id} className="bg-white rounded-lg shadow p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {memory.metadata.type || 'document'}
                    </span>
                    {memory.filename && (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                        {memory.filename}
                      </span>
                    )}
                    {memory.chunk_id && (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        {memory.chunk_id}
                      </span>
                    )}
                  </div>
                  
                  <p className="text-sm text-gray-900 mb-2">
                    {truncateText(memory.text)}
                  </p>
                  
                  <div className="text-xs text-gray-500 space-y-1">
                    <p>ID: {memory.id}</p>
                    {memory.metadata.timestamp && (
                      <p>Created: {formatTimestamp(memory.metadata.timestamp)}</p>
                    )}
                    {memory.metadata.agent_id && (
                      <p>Agent: {memory.metadata.agent_id}</p>
                    )}
                  </div>
                </div>
                
                <button
                  onClick={() => deleteMemory(memory.id)}
                  disabled={deletingId === memory.id}
                  className="ml-4 p-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50"
                >
                  {deletingId === memory.id ? (
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-red-500"></div>
                  ) : (
                    <Trash2 className="w-4 h-4" />
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default MemoryViewer