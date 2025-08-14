"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { FileIcon, Search, BarChart3, Plus } from "lucide-react"

export default function MyQuotesPage() {
  const [searchQuery, setSearchQuery] = useState("")

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link href="/">
                <h1 className="text-xl font-bold text-gray-900 cursor-pointer hover:text-gray-700">FinancialConsult</h1>
              </Link>
            </div>
            <div className="hidden md:flex items-center space-x-1">
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
                <Button variant="ghost" className="text-gray-600 hover:text-gray-900 text-sm bg-gray-100">
                  📋 My Quotes
                </Button>
              </Link>
              <Link href="/compare-policies">
                <Button className="bg-blue-600 text-white hover:bg-blue-700 text-sm">🔄 Compare Policies</Button>
              </Link>
              <div className="ml-4 text-sm font-medium text-gray-900">DU</div>
            </div>
            {/* Mobile Navigation */}
            <div className="md:hidden">
              <Select>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Menu" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="dashboard">
                    <Link href="/dashboard">Dashboard</Link>
                  </SelectItem>
                  <SelectItem value="upload">
                    <Link href="/upload-pdf">Upload PDF</Link>
                  </SelectItem>
                  <SelectItem value="quotes">My Quotes</SelectItem>
                  <SelectItem value="compare">
                    <Link href="/compare-policies">Compare</Link>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {/* Page Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 sm:mb-8">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">My Quotes</h1>
            <p className="text-gray-600 text-sm sm:text-base">Manage and compare your insurance quotes.</p>
          </div>
          <Link href="/upload-pdf" className="mt-4 sm:mt-0">
            <Button className="bg-black text-white hover:bg-gray-800 w-full sm:w-auto">
              <Plus className="w-4 h-4 mr-2" />
              Upload New Quote
            </Button>
          </Link>
        </div>

        {/* Real Policy Comparison Banner */}
        <Card className="bg-blue-50 border-blue-200 mb-6 sm:mb-8">
          <CardContent className="p-4 sm:p-6">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between">
              <div className="flex items-start space-x-3 mb-4 sm:mb-0">
                <BarChart3 className="w-6 h-6 text-blue-600 mt-1 flex-shrink-0" />
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">Real Policy Comparison</h3>
                  <p className="text-gray-700 text-sm">
                    View comparison of actual data extracted from your uploaded insurance policies
                  </p>
                </div>
              </div>
              <Link href="/compare-policies">
                <Button className="bg-blue-600 text-white hover:bg-blue-700 w-full sm:w-auto">
                  📊 View Your Policy Comparison
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Search and Filters */}
        <Card className="bg-white border border-gray-200 mb-6 sm:mb-8">
          <CardContent className="p-4 sm:p-6">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  placeholder="Search quotes by company or plan name..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
              <div className="flex flex-col sm:flex-row gap-4 sm:gap-2">
                <Select defaultValue="all-status">
                  <SelectTrigger className="w-full sm:w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all-status">All Status</SelectItem>
                    <SelectItem value="processing">Processing</SelectItem>
                    <SelectItem value="completed">Completed</SelectItem>
                    <SelectItem value="failed">Failed</SelectItem>
                  </SelectContent>
                </Select>
                <Select defaultValue="all-companies">
                  <SelectTrigger className="w-full sm:w-36">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all-companies">All Companies</SelectItem>
                    <SelectItem value="old-mutual">Old Mutual</SelectItem>
                    <SelectItem value="santam">Santam</SelectItem>
                    <SelectItem value="discovery">Discovery</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Insurance Quotes Section */}
        <Card className="bg-white border border-gray-200">
          <CardContent className="p-4 sm:p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Insurance Quotes</h3>

            {/* Empty State */}
            <div className="text-center py-12 sm:py-16">
              <FileIcon className="w-16 h-16 sm:w-20 sm:h-20 text-gray-300 mx-auto mb-4 sm:mb-6" />
              <h4 className="text-xl sm:text-2xl font-semibold text-gray-900 mb-3 sm:mb-4">No quotes found</h4>
              <p className="text-gray-600 mb-6 sm:mb-8 max-w-md mx-auto text-sm sm:text-base">
                Upload your first insurance quote to get started.
              </p>
              <Link href="/upload-pdf">
                <Button className="bg-black text-white hover:bg-gray-800 w-full sm:w-auto">Upload Quote</Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
