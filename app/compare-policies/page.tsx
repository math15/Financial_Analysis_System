"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, Upload, Download, Search, FileText, Users } from "lucide-react"

export default function ComparePoliciesPage() {
  const [searchQuery, setSearchQuery] = useState("")

  const insuranceCompanies = [
    {
      name: "Old Mutual Insure",
      policyNumber: "-",
      clientName: "-",
      policyType: "Commercial Short-term",
      totalPremium: "Varies",
      sectionsCovered: 6,
      sectionsNotCovered: 19,
    },
    {
      name: "Santam",
      policyNumber: "-",
      clientName: "-",
      policyType: "Commercial Short-term",
      totalPremium: "Varies",
      sectionsCovered: 8,
      sectionsNotCovered: 17,
    },
    {
      name: "Bryte Insurance Company Limited",
      policyNumber: "-",
      clientName: "-",
      policyType: "Commercial Short-term",
      totalPremium: "Varies",
      sectionsCovered: 10,
      sectionsNotCovered: 15,
    },
    {
      name: "Discovery Insure",
      policyNumber: "-",
      clientName: "-",
      policyType: "Commercial Short-term",
      totalPremium: "Varies",
      sectionsCovered: 9,
      sectionsNotCovered: 16,
    },
    {
      name: "Hollard Insurance",
      policyNumber: "-",
      clientName: "-",
      policyType: "Commercial Short-term",
      totalPremium: "Varies",
      sectionsCovered: 8,
      sectionsNotCovered: 17,
    },
  ]

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
                <Button variant="ghost" className="text-gray-600 hover:text-gray-900 text-sm">
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
                  <SelectItem value="quotes">
                    <Link href="/my-quotes">My Quotes</Link>
                  </SelectItem>
                  <SelectItem value="compare">Compare Policies</SelectItem>
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
          <div className="flex items-center space-x-4 mb-4 sm:mb-0">
            <Link href="/my-quotes">
              <Button variant="ghost" className="text-gray-600 hover:text-gray-900 p-2">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Quotes
              </Button>
            </Link>
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-1">Your Uploaded Policies Comparison</h1>
              <p className="text-gray-600 text-sm sm:text-base">Analysis of your actual uploaded insurance documents</p>
            </div>
          </div>
          <div className="flex flex-col sm:flex-row gap-2 w-full sm:w-auto">
            <Link href="/upload-pdf">
              <Button variant="outline" className="w-full sm:w-auto bg-transparent">
                <Upload className="w-4 h-4 mr-2" />
                Upload More
              </Button>
            </Link>
            <Button className="bg-blue-600 text-white hover:bg-blue-700 w-full sm:w-auto">
              <Download className="w-4 h-4 mr-2" />
              Download Report
            </Button>
          </div>
        </div>

        {/* Data Source Info */}
        <Card className="bg-blue-50 border-blue-200 mb-6 sm:mb-8">
          <CardContent className="p-4 sm:p-6">
            <div className="flex items-start space-x-3">
              <FileText className="w-6 h-6 text-blue-600 mt-1 flex-shrink-0" />
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-1">Data Source: Your Uploaded Documents</h3>
                <p className="text-blue-700 text-sm mb-2">
                  <span className="font-medium">Source:</span> Your uploaded insurance policies
                </p>
                <p className="text-blue-700 text-sm mb-4">
                  <span className="font-medium">Processed:</span> Today | <span className="font-medium">Version:</span>{" "}
                  2.0
                </p>
                <div className="flex flex-wrap gap-4">
                  <div className="flex items-center space-x-2">
                    <FileText className="w-4 h-4 text-blue-600" />
                    <span className="text-sm font-medium text-gray-900">25 Sections</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Users className="w-4 h-4 text-blue-600" />
                    <span className="text-sm font-medium text-gray-900">5 Companies</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Search */}
        <Card className="bg-white border border-gray-200 mb-6 sm:mb-8">
          <CardContent className="p-4 sm:p-6">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  placeholder="Search sections..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Badge variant="secondary" className="self-start sm:self-center">
                25 sections
              </Badge>
            </div>
          </CardContent>
        </Card>

        {/* Comparison Tabs */}
        <Card className="bg-white border border-gray-200">
          <CardContent className="p-0">
            <Tabs defaultValue="policy-summary" className="w-full">
              <div className="border-b px-4 sm:px-6">
                <TabsList className="grid w-full grid-cols-3 bg-transparent h-auto p-0">
                  <TabsTrigger
                    value="policy-summary"
                    className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-blue-600 rounded-none py-4 text-sm sm:text-base"
                  >
                    Policy Summary
                  </TabsTrigger>
                  <TabsTrigger
                    value="section-summary"
                    className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-blue-600 rounded-none py-4 text-sm sm:text-base"
                  >
                    Section Summary
                  </TabsTrigger>
                  <TabsTrigger
                    value="detailed-comparison"
                    className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-blue-600 rounded-none py-4 text-sm sm:text-base"
                  >
                    Detailed Comparison
                  </TabsTrigger>
                </TabsList>
              </div>

              <TabsContent value="policy-summary" className="p-4 sm:p-6 mt-0">
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Policy Summary (Vertical Layout)</h3>
                  <p className="text-gray-600 text-sm">Companies listed vertically with their main sections</p>
                </div>

                {/* Desktop Table View */}
                <div className="hidden lg:block overflow-x-auto">
                  <table className="w-full border-collapse border border-gray-300">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="border border-gray-300 px-4 py-3 text-left font-medium text-gray-900">
                          Insurance Company
                        </th>
                        <th className="border border-gray-300 px-4 py-3 text-left font-medium text-gray-900">
                          Policy Number
                        </th>
                        <th className="border border-gray-300 px-4 py-3 text-left font-medium text-gray-900">
                          Client Name
                        </th>
                        <th className="border border-gray-300 px-4 py-3 text-left font-medium text-gray-900">
                          Policy Type
                        </th>
                        <th className="border border-gray-300 px-4 py-3 text-left font-medium text-gray-900">
                          Total Premium
                        </th>
                        <th className="border border-gray-300 px-4 py-3 text-left font-medium text-gray-900">
                          Main Sections
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {insuranceCompanies.map((company, index) => (
                        <tr key={index} className="hover:bg-gray-50">
                          <td className="border border-gray-300 px-4 py-3 font-medium text-gray-900">{company.name}</td>
                          <td className="border border-gray-300 px-4 py-3 text-gray-600">{company.policyNumber}</td>
                          <td className="border border-gray-300 px-4 py-3 text-gray-600">{company.clientName}</td>
                          <td className="border border-gray-300 px-4 py-3 text-gray-600">{company.policyType}</td>
                          <td className="border border-gray-300 px-4 py-3 text-gray-600">{company.totalPremium}</td>
                          <td className="border border-gray-300 px-4 py-3">
                            <div className="flex flex-wrap gap-2">
                              <Badge variant="secondary" className="text-xs">
                                {company.sectionsCovered} sections covered
                              </Badge>
                              <Badge variant="outline" className="text-xs">
                                {company.sectionsNotCovered} not covered
                              </Badge>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Mobile Card View */}
                <div className="lg:hidden space-y-4">
                  {insuranceCompanies.map((company, index) => (
                    <Card key={index} className="border border-gray-200">
                      <CardContent className="p-4">
                        <h4 className="font-semibold text-gray-900 mb-3">{company.name}</h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-600">Policy Type:</span>
                            <span className="text-gray-900">{company.policyType}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Total Premium:</span>
                            <span className="text-gray-900">{company.totalPremium}</span>
                          </div>
                          <div className="pt-2">
                            <div className="flex flex-wrap gap-2">
                              <Badge variant="secondary" className="text-xs">
                                {company.sectionsCovered} sections covered
                              </Badge>
                              <Badge variant="outline" className="text-xs">
                                {company.sectionsNotCovered} not covered
                              </Badge>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>

              <TabsContent value="section-summary" className="p-4 sm:p-6 mt-0">
                <div className="text-center py-12">
                  <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Section Summary</h3>
                  <p className="text-gray-600">Detailed section-by-section comparison coming soon.</p>
                </div>
              </TabsContent>

              <TabsContent value="detailed-comparison" className="p-4 sm:p-6 mt-0">
                <div className="text-center py-12">
                  <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Detailed Comparison</h3>
                  <p className="text-gray-600">In-depth policy comparison features coming soon.</p>
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
