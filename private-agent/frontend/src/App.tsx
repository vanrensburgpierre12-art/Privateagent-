import React, { useState } from 'react'
import Chat from './components/Chat'
import Upload from './components/Upload'
import MemoryViewer from './components/MemoryViewer'
import { MessageSquare, Upload as UploadIcon, Database, Settings } from 'lucide-react'

type Tab = 'chat' | 'upload' | 'memory' | 'settings'

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('chat')

  const tabs = [
    { id: 'chat' as Tab, label: 'Chat', icon: MessageSquare },
    { id: 'upload' as Tab, label: 'Upload', icon: UploadIcon },
    { id: 'memory' as Tab, label: 'Memory', icon: Database },
    { id: 'settings' as Tab, label: 'Settings', icon: Settings },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                Private Agent Platform
              </h1>
            </div>
            <div className="flex space-x-1">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      activeTab === tab.id
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-4 h-4 mr-2" />
                    {tab.label}
                  </button>
                )
              })}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'chat' && <Chat />}
        {activeTab === 'upload' && <Upload />}
        {activeTab === 'memory' && <MemoryViewer />}
        {activeTab === 'settings' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Settings</h2>
            <p className="text-gray-600">
              Settings panel coming soon. For now, you can configure the system via environment variables.
            </p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App