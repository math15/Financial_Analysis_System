"use client";

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { FileText, CheckCircle, Clock, TrendingUp, Upload, BarChart3, FolderOpen, FileIcon } from "lucide-react"
import { useUserStats } from "@/lib/hooks"

export default function DashboardPage() {
  const { stats, loading, error } = useUserStats();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">FinancialConsult</h1>
            </div>
            <div className="flex items-center space-x-1">
              <Link href="/dashboard">
                <Button variant="ghost" className="text-gray-600 hover:text-gray-900 text-sm">
                  📊 Dashboard
                </Button>
              </Link>
              <Link href="/upload-pdf">
                <Button variant="ghost" className="text-gray-600 hover:text-gray-900 text-sm">
                  📄 Upload PDF
                </Button>
              </Link>
              <Link href="/my-quotes">
                <Button variant="ghost" className="text-gray-600 hover:text-gray-900 text-sm">
                  📋 My Quotes
                </Button>
              </Link>
              <Link href="/compare-policies">
                <Button className="bg-blue-600 text-white hover:bg-blue-700 text-sm">🔄 Compare Policies</Button>
              </Link>
              <div className="ml-4 text-sm font-medium text-gray-900">DU</div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome back, Demo!</h1>
          <p className="text-gray-600">{"Here's an overview of your insurance quote comparisons."}</p>
        </div>

        {/* Backend Connection Status */}
        {error && (
          <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex items-center">
              <div className="text-yellow-800">
                <strong>⚠️ Backend Connection Issue:</strong> {error}
              </div>
            </div>
            <p className="text-yellow-700 text-sm mt-1">
              Make sure the backend is running on port 5000. Run: <code className="bg-yellow-100 px-1 rounded">cd backend && source venv/bin/activate && python run.py</code>
            </p>
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-white border border-gray-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Quotes</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {loading ? "..." : stats?.total_quotes || 0}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">Total uploaded quotes</p>
                </div>
                <FileText className="w-8 h-8 text-gray-400" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border border-gray-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Completed</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {loading ? "..." : stats?.completed || 0}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">Ready for comparison</p>
                </div>
                <CheckCircle className="w-8 h-8 text-green-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border border-gray-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Processing</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {loading ? "..." : stats?.processing || 0}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">Being analyzed</p>
                </div>
                <Clock className="w-8 h-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border border-gray-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Average Premium</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {loading ? "..." : stats?.average_premium || "R0"}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">Average monthly premium</p>
                </div>
                <TrendingUp className="w-8 h-8 text-cyan-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Card className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold mb-2">Upload New Quotes</h3>
                  <p className="text-blue-100 mb-4">Upload PDF quotes to start comparing insurance policies</p>
                  <Link href="/upload-pdf">
                    <Button 
                      variant="secondary" 
                      className="bg-white text-blue-600 hover:bg-blue-50"
                    >
                      <Upload className="w-4 h-4 mr-2" />
                      Upload PDFs
                    </Button>
                  </Link>
                </div>
                <Upload className="w-12 h-12 text-blue-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold mb-2">View Reports</h3>
                  <p className="text-green-100 mb-4">Generate and download detailed comparison reports</p>
                  <Link href="/compare-policies">
                    <Button 
                      variant="secondary" 
                      className="bg-white text-green-600 hover:bg-green-50"
                    >
                      <BarChart3 className="w-4 h-4 mr-2" />
                      Compare Now
                    </Button>
                  </Link>
                </div>
                <BarChart3 className="w-12 h-12 text-green-200" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Activity */}
        <Card className="bg-white border border-gray-200">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
              <Link href="/my-quotes">
                <Button variant="outline" size="sm">
                  <FolderOpen className="w-4 h-4 mr-2" />
                  View All
                </Button>
              </Link>
            </div>
            
            {loading ? (
              <div className="text-center py-8 text-gray-500">
                Loading recent activity...
              </div>
            ) : error ? (
              <div className="text-center py-8 text-gray-500">
                <FileIcon className="w-12 h-12 mx-auto text-gray-300 mb-4" />
                <p>Unable to load recent activity</p>
                <p className="text-sm">Check backend connection</p>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <FileIcon className="w-12 h-12 mx-auto text-gray-300 mb-4" />
                <p>No recent activity</p>
                <p className="text-sm">Upload some quotes to get started</p>
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
