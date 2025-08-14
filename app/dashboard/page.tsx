import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { FileText, CheckCircle, Clock, TrendingUp, Upload, BarChart3, FolderOpen, FileIcon } from "lucide-react"

export default function DashboardPage() {
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

        {/* Stats Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-white border border-gray-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Quotes</p>
                  <p className="text-3xl font-bold text-gray-900">0</p>
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
                  <p className="text-3xl font-bold text-gray-900">0</p>
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
                  <p className="text-3xl font-bold text-gray-900">0</p>
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
                  <p className="text-3xl font-bold text-gray-900">R0</p>
                  <p className="text-xs text-gray-500 mt-1">Average monthly premium</p>
                </div>
                <TrendingUp className="w-8 h-8 text-cyan-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Action Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <Card className="bg-white border border-gray-200">
            <CardContent className="p-6">
              <div className="flex items-start space-x-4">
                <Upload className="w-6 h-6 text-gray-600 mt-1" />
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload New Quote</h3>
                  <p className="text-gray-600 text-sm mb-4">Upload a new insurance quote PDF to start comparison</p>
                  <Link href="/upload-pdf">
                    <Button className="bg-black text-white hover:bg-gray-800 w-full">
                      <Upload className="w-4 h-4 mr-2" />
                      Upload PDF
                    </Button>
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border border-gray-200">
            <CardContent className="p-6">
              <div className="flex items-start space-x-4">
                <BarChart3 className="w-6 h-6 text-gray-600 mt-1" />
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Policy Comparison</h3>
                  <p className="text-gray-600 text-sm mb-4">Compare real insurance policy data side-by-side</p>
                  <Link href="/compare-policies">
                    <Button className="bg-blue-600 text-white hover:bg-blue-700 w-full">🔄 Compare Policies</Button>
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border border-gray-200">
            <CardContent className="p-6">
              <div className="flex items-start space-x-4">
                <FolderOpen className="w-6 h-6 text-gray-600 mt-1" />
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">My Quotes</h3>
                  <p className="text-gray-600 text-sm mb-4">Manage all your uploaded quotes and documents</p>
                  <Link href="/my-quotes">
                    <Button variant="outline" className="w-full bg-transparent">
                      Manage Quotes
                    </Button>
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Activity */}
        <Card className="bg-white border border-gray-200">
          <CardContent className="p-6">
            <div className="flex items-center space-x-2 mb-4">
              <Clock className="w-5 h-5 text-gray-600" />
              <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
            </div>
            <p className="text-gray-600 text-sm mb-8">Your latest quote uploads and processing status</p>

            <div className="text-center py-12">
              <FileIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h4 className="text-lg font-medium text-gray-900 mb-2">No quotes yet</h4>
              <p className="text-gray-600 mb-6">Upload your first insurance quote to get started with comparisons.</p>
              <Link href="/upload-pdf">
                <Button className="bg-black text-white hover:bg-gray-800">Upload Your First Quote</Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
