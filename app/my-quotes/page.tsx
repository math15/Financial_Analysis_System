"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { FileIcon, Search, BarChart3, Plus, AlertCircle, Clock, CheckCircle } from "lucide-react"
import { useUserQuotes } from "@/lib/hooks"
import { insuranceAPI } from "@/lib/api"

export default function MyQuotesPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const { quotes, loading, error, refetch } = useUserQuotes()

  const filteredQuotes = quotes.filter(quote => 
    quote.file_names.some(name => 
      name.toLowerCase().includes(searchQuery.toLowerCase())
    )
  )

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
                    <Link href="/dashboard">📊 Dashboard</Link>
                  </SelectItem>
                  <SelectItem value="upload">
                    <Link href="/upload-pdf">📄 Upload PDF</Link>
                  </SelectItem>
                  <SelectItem value="quotes">
                    <Link href="/my-quotes">📋 My Quotes</Link>
                  </SelectItem>
                  <SelectItem value="compare">
                    <Link href="/compare-policies">🔄 Compare</Link>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">My Quotes</h1>
            <p className="text-gray-600">Manage and compare your uploaded insurance quotes.</p>
          </div>
          <div className="mt-4 sm:mt-0">
            <Link href="/upload-pdf">
            <Button className="bg-black text-white hover:bg-gray-800 w-full sm:w-auto">
              <Plus className="w-4 h-4 mr-2" />
              Upload New Quote
            </Button>
          </Link>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <Card className="bg-red-50 border border-red-200 mb-8">
            <CardContent className="p-6">
              <div className="flex items-start space-x-3">
                <AlertCircle className="w-6 h-6 text-red-600 mt-1" />
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-red-900 mb-2">Failed to Load Quotes</h3>
                  <p className="text-red-800 mb-4">{error}</p>
                  <div className="flex space-x-3">
                    <Button 
                      onClick={refetch}
                      variant="outline" 
                      className="border-red-300 text-red-700 hover:bg-red-50"
                    >
                      Try Again
                    </Button>
                  </div>
                </div>
            </div>
          </CardContent>
        </Card>
        )}

        {/* Search and Filter */}
        <Card className="bg-white border border-gray-200 mb-8">
          <CardContent className="p-6">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                    placeholder="Search by filename..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
              </div>
              <div className="sm:w-48">
                <Select defaultValue="all">
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="completed">Completed</SelectItem>
                    <SelectItem value="processing">Processing</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quotes List */}
        {loading ? (
          <Card className="bg-white border border-gray-200">
            <CardContent className="p-12 text-center">
              <div className="text-gray-500">Loading quotes...</div>
            </CardContent>
          </Card>
        ) : filteredQuotes.length === 0 ? (
        <Card className="bg-white border border-gray-200">
            <CardContent className="p-12 text-center">
              <FileIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                {quotes.length === 0 ? "No quotes uploaded yet" : "No quotes match your search"}
              </h3>
              <p className="text-gray-600 mb-6">
                {quotes.length === 0 
                  ? "Upload your first insurance quote to get started with comparisons."
                  : "Try adjusting your search terms."
                }
              </p>
              {quotes.length === 0 && (
              <Link href="/upload-pdf">
                  <Button className="bg-black text-white hover:bg-gray-800">
                    Upload Your First Quote
                  </Button>
                </Link>
              )}
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {filteredQuotes.map((quote, index) => (
              <Card key={quote.comparison_id} className="bg-white border border-gray-200 hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="flex flex-col lg:flex-row lg:justify-between lg:items-start gap-4">
                    {/* Quote Info */}
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <div className="flex items-center gap-2">
                          {quote.status === "completed" ? (
                            <CheckCircle className="w-5 h-5 text-green-500" />
                          ) : (
                            <Clock className="w-5 h-5 text-orange-500" />
                          )}
                          <span className={`text-sm font-medium ${
                            quote.status === "completed" ? "text-green-700" : "text-orange-700"
                          }`}>
                            {quote.status === "completed" ? "Ready for comparison" : "Processing"}
                          </span>
                        </div>
                      </div>
                      
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">
                        Comparison #{index + 1}
                      </h3>
                      
                      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
                        <div>
                          <span className="text-gray-600">Files:</span>
                          <p className="font-medium text-gray-900">
                            {quote.file_names.slice(0, 2).join(", ")}
                            {quote.file_names.length > 2 && ` (+${quote.file_names.length - 2} more)`}
                          </p>
                        </div>
                        <div>
                          <span className="text-gray-600">Quote Count:</span>
                          <p className="font-medium text-gray-900">{quote.quote_count} quotes</p>
                        </div>
                        <div>
                          <span className="text-gray-600">Created:</span>
                          <p className="font-medium text-gray-900">
                            {new Date(quote.created_at).toLocaleDateString()}
                          </p>
                        </div>
                        <div className="sm:col-span-2 lg:col-span-3">
                          <span className="text-gray-600">Premiums:</span>
                          <p className="font-medium text-gray-900">
                            {quote.total_premiums.join(" • ")}
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex flex-col sm:flex-row lg:flex-col gap-2 lg:w-32">
                      {quote.status === "completed" && (
                        <Link href={`/compare-policies?id=${quote.comparison_id}`}>
                          <Button 
                            className="bg-blue-600 text-white hover:bg-blue-700 w-full sm:w-auto lg:w-full"
                            size="sm"
                          >
                            <BarChart3 className="w-4 h-4 mr-2" />
                            Compare
                          </Button>
              </Link>
                      )}
                      {/* 🆕 Updated Download Report Button */}
                      {(quote as any).report_generated ? (
                        <Button 
                          onClick={() => {
                            const downloadUrl = insuranceAPI.getReportDownloadUrl((quote as any).report_filename);
                            window.open(downloadUrl, '_blank');
                          }}
                          variant="outline" 
                          size="sm"
                          className="w-full sm:w-auto lg:w-full"
                        >
                          📄 Download PDF
                        </Button>
                      ) : (
                        <Button 
                          variant="outline" 
                          size="sm"
                          className="w-full sm:w-auto lg:w-full opacity-50"
                          disabled
                        >
                          {quote.status === "processing" ? "⏳ Processing..." : "📄 No Report"}
                        </Button>
                      )}
                    </div>
            </div>
          </CardContent>
        </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
