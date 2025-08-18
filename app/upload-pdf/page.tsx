"use client"

import type React from "react"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Upload, AlertCircle, CheckCircle, X, FileText } from "lucide-react"
import { useUploadQuotes } from "@/lib/hooks"
import { useRouter } from "next/navigation"

export default function UploadPDFPage() {
  const [selectedType, setSelectedType] = useState("Commercial Lines Insurance")
  const [dragActive, setDragActive] = useState(false)
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])
  const [uploadResult, setUploadResult] = useState<any>(null)
  
  const { uploadFiles, uploading, error } = useUploadQuotes()
  const router = useRouter()

  // Debug: Log the current environment and API URL
  useEffect(() => {
    console.log('Environment:', {
      hostname: typeof window !== 'undefined' ? window.location.hostname : 'server',
      protocol: typeof window !== 'undefined' ? window.location.protocol : 'server',
      NODE_ENV: process.env.NODE_ENV
    })
  }, [])

  const insuranceTypes = [
    {
      id: "personal",
      title: "Personal Lines Insurance",
      description: "Individual and family insurance covering personal assets",
      selected: selectedType === "Personal Lines Insurance",
    },
    {
      id: "commercial",
      title: "Commercial Lines Insurance",
      description: "Business insurance covering commercial operations and assets",
      selected: selectedType === "Commercial Lines Insurance",
    },
    {
      id: "life",
      title: "Life Insurance",
      description: "Life, disability, and health insurance coverage",
      selected: selectedType === "Life Insurance",
    },
    {
      id: "investment",
      title: "Investment Products",
      description: "Investment and savings products",
      selected: selectedType === "Investment Products",
    },
  ]

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    const files = Array.from(e.dataTransfer.files).filter(file => 
      file.type === 'application/pdf' && file.size <= 20 * 1024 * 1024  // Updated to 20MB
    )
    
    if (files.length > 0) {
      setSelectedFiles(prev => [...prev, ...files])
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log('File select triggered', e.target.files)
    const files = Array.from(e.target.files || []).filter(file => 
      file.type === 'application/pdf' && file.size <= 20 * 1024 * 1024  // Updated to 20MB
    )
    
    console.log('Filtered files:', files)
    
    if (files.length > 0) {
      setSelectedFiles(prev => [...prev, ...files])
      console.log('Files added to state')
    } else {
      console.log('No valid files selected')
    }
  }

  const handleButtonClick = () => {
    console.log('Button clicked - triggering file input')
    const fileInput = document.getElementById('file-upload') as HTMLInputElement
    if (fileInput) {
      fileInput.click()
      console.log('File input clicked programmatically')
    } else {
      console.error('File input not found')
    }
  }

  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index))
  }

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return

    const result = await uploadFiles(selectedFiles)
    if (result) {
      setUploadResult(result)
      setSelectedFiles([])
    }
  }

  const viewResults = () => {
    if (uploadResult?.comparison_id) {
      router.push(`/compare-policies?id=${uploadResult.comparison_id}`)
    }
  }

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
                <Button variant="ghost" className="text-gray-600 hover:text-gray-900 text-sm bg-gray-100">
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
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Upload Insurance Quotes</h1>
          <p className="text-blue-600">Upload your insurance quote PDFs to start comparing coverage and pricing.</p>
        </div>

        {/* Upload Success Message */}
        {uploadResult && (
          <Card className="bg-green-50 border border-green-200 mb-8">
            <CardContent className="p-6">
              <div className="flex items-start space-x-3">
                <CheckCircle className="w-6 h-6 text-green-600 mt-1" />
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-green-900 mb-2">Upload Successful!</h3>
                  <p className="text-green-800 mb-4">
                    {uploadResult.message} - {uploadResult.quote_count} quotes processed
                  </p>
                  <div className="flex space-x-3">
                    <Button 
                      onClick={viewResults}
                      className="bg-green-600 text-white hover:bg-green-700"
                    >
                      View Comparison Results
                    </Button>
                    <Button 
                      variant="outline" 
                      onClick={() => setUploadResult(null)}
                      className="border-green-300 text-green-700 hover:bg-green-50"
                    >
                      Upload More Files
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Error Message */}
        {error && (
          <Card className="bg-red-50 border border-red-200 mb-8">
            <CardContent className="p-6">
              <div className="flex items-start space-x-3">
                <AlertCircle className="w-6 h-6 text-red-600 mt-1" />
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-red-900 mb-2">Upload Failed</h3>
                  <p className="text-red-800 mb-4">{error}</p>
                  <p className="text-red-700 text-sm">
                    Make sure the backend is running on port 5000. Run: <code className="bg-red-100 px-1 rounded">cd backend && source venv/bin/activate && python run.py</code>
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Insurance Type Selection */}
        <Card className="bg-white border border-gray-200 mb-8">
          <CardContent className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-2">Select Insurance Type</h2>
            <p className="text-gray-600 text-sm mb-6">
              Choose the type of insurance quotes you'll be uploading for optimal data extraction.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
              {insuranceTypes.map((type) => (
                <Card
                  key={type.id}
                  className={`cursor-pointer transition-all ${
                    type.selected ? "border-blue-500 bg-blue-50" : "border-gray-200 hover:border-gray-300"
                  }`}
                  onClick={() => setSelectedType(type.title)}
                >
                  <CardContent className="p-4">
                    <h3 className="font-medium text-gray-900 mb-2">{type.title}</h3>
                    <p className="text-xs text-gray-600 mb-3">{type.description}</p>
                    {type.selected && (
                      <Button size="sm" className="bg-blue-600 text-white text-xs">
                        Selected
                      </Button>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <p className="text-sm text-blue-800">
                <span className="font-medium">Selected:</span> {selectedType} - The system will extract data according
                to this template for optimal comparison results.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Current Plan */}
        <Card className="bg-white border border-gray-200 mb-8">
          <CardContent className="p-6">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">Current Plan: Free</h3>
                <p className="text-gray-600 text-sm">0 of 2 reports used this month</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600">Max 10 quotes per comparison</p>
                <p className="text-sm text-gray-600">Currently: {selectedFiles.length} quotes selected</p>
              </div>
            </div>
            <div className="mt-4 flex items-center text-orange-600">
              <AlertCircle className="w-4 h-4 mr-2" />
              <span className="text-sm">Upgrade to Basic or Pro for more reports and quotes per comparison</span>
            </div>
          </CardContent>
        </Card>

        {/* Selected Files */}
        {selectedFiles.length > 0 && (
          <Card className="bg-white border border-gray-200 mb-8">
            <CardContent className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Selected Files ({selectedFiles.length})</h3>
              <div className="space-y-3">
                {selectedFiles.map((file, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <FileText className="w-5 h-5 text-blue-600" />
                      <div>
                        <p className="font-medium text-gray-900">{file.name}</p>
                        <p className="text-sm text-gray-600">
                          {(file.size / (1024 * 1024)).toFixed(2)} MB
                        </p>
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeFile(index)}
                      className="text-red-600 hover:text-red-700 hover:bg-red-50"
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                ))}
              </div>
              <div className="mt-4 flex space-x-3">
                <Button 
                  onClick={handleUpload}
                  disabled={uploading}
                  className="bg-green-600 text-white hover:bg-green-700"
                >
                  {uploading ? "Processing..." : `Upload ${selectedFiles.length} Files`}
                </Button>
                <Button 
                  variant="outline" 
                  onClick={() => setSelectedFiles([])}
                  disabled={uploading}
                >
                  Clear All
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Upload Section */}
        <Card className="bg-white border border-gray-200">
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload PDF Files</h3>
            <p className="text-gray-600 text-sm mb-6">
              Drag and drop your insurance quote PDFs here, or click to select files. Maximum file size: 20MB per file.
            </p>

            <div
              className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
                dragActive ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-gray-400"
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h4 className="text-lg font-medium text-gray-900 mb-2">Drop your PDF files here</h4>
              <p className="text-gray-600 mb-4">or click to browse and select files</p>
              <Button onClick={handleButtonClick} className="bg-black text-white hover:bg-gray-800">
                Select PDF Files
              </Button>
              <input
                id="file-upload"
                type="file"
                multiple
                accept=".pdf"
                onChange={handleFileSelect}
                className="hidden"
              />
              
              {/* Debug info */}
              <div className="mt-4 text-xs text-gray-500">
                <p>Selected files: {selectedFiles.length}</p>
                <p>Upload status: {uploading ? 'Uploading...' : 'Ready'}</p>
                {error && <p className="text-red-500">Error: {error}</p>}
              </div>
            </div>

            <div className="mt-6 flex items-start space-x-2 bg-blue-50 border border-blue-200 rounded-lg p-4">
              <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm text-blue-800">
                  <span className="font-medium">Requirements:</span> Only PDF files are accepted. Maximum file size is
                  20MB. Files should contain insurance quote information for best results.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
