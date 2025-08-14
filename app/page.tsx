import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Users, FileText, Clock, Target, Upload, BarChart3, Shield, FileBarChart } from "lucide-react"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-14 sm:h-16">
            <div className="flex items-center">
              <Link href="/">
                <h1 className="text-lg sm:text-xl font-bold text-gray-900 cursor-pointer hover:text-gray-700">
                  FinancialConsult
                </h1>
              </Link>
            </div>
            <div className="hidden sm:flex items-center space-x-3 lg:space-x-4">
              <Link href="/signin">
                <Button variant="ghost" className="text-gray-600 hover:text-gray-900 text-sm lg:text-base">
                  Sign In
                </Button>
              </Link>
              <Link href="/signup">
                <Button className="bg-black text-white hover:bg-gray-800 text-sm lg:text-base px-4 lg:px-6">
                  Get Started
                </Button>
              </Link>
            </div>
            {/* Mobile menu */}
            <div className="sm:hidden flex items-center space-x-2">
              <Link href="/signin">
                <Button variant="ghost" size="sm" className="text-gray-600 hover:text-gray-900">
                  Sign In
                </Button>
              </Link>
              <Link href="/signup">
                <Button size="sm" className="bg-black text-white hover:bg-gray-800">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Demo Mode Banner */}
      <div className="bg-blue-50 border-l-4 border-blue-400 p-3 sm:p-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-start sm:items-center">
            <div className="flex-shrink-0 mt-0.5 sm:mt-0">
              <div className="w-4 h-4 sm:w-5 sm:h-5 bg-blue-400 rounded-full flex items-center justify-center">
                <span className="text-white text-xs">i</span>
              </div>
            </div>
            <div className="ml-3">
              <p className="text-xs sm:text-sm text-blue-700 leading-relaxed">
                <span className="font-medium">Demo Mode:</span> Explore all features with real extracted insurance data
                <span className="hidden sm:inline"> - Using demo mode - you can still explore all features</span>
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <section className="py-12 sm:py-16 lg:py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-bold text-gray-900 mb-4 sm:mb-6 leading-tight">
            Compare Insurance Quotes
            <br />
            <span className="text-gray-600">Effortlessly</span>
          </h1>
          <p className="text-base sm:text-lg lg:text-xl text-gray-600 mb-6 sm:mb-8 max-w-2xl lg:max-w-3xl mx-auto leading-relaxed px-4 sm:px-0">
            Upload your insurance quote PDFs and let our AI-powered platform analyze and compare them for you. Make
            informed decisions with clear, highlighted comparisons.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center space-y-3 sm:space-y-0 sm:space-x-4 px-4 sm:px-0">
            <Link href="/signup">
              <Button className="bg-black text-white hover:bg-gray-800 px-6 sm:px-8 py-3 text-sm sm:text-base w-full sm:w-auto">
                Start Comparing Now →
              </Button>
            </Link>
            <Link href="/signin">
              <Button
                variant="outline"
                className="px-6 sm:px-8 py-3 bg-transparent text-sm sm:text-base w-full sm:w-auto"
              >
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 sm:py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8 text-center">
            <div className="flex flex-col items-center">
              <Users className="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 text-gray-600 mb-3 sm:mb-4" />
              <div className="text-2xl sm:text-3xl font-bold text-gray-900">1,000+</div>
              <div className="text-gray-600 text-xs sm:text-sm lg:text-base">Happy Customers</div>
            </div>
            <div className="flex flex-col items-center">
              <FileText className="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 text-gray-600 mb-3 sm:mb-4" />
              <div className="text-2xl sm:text-3xl font-bold text-gray-900">5,000+</div>
              <div className="text-gray-600 text-xs sm:text-sm lg:text-base">Quotes Processed</div>
            </div>
            <div className="flex flex-col items-center">
              <Clock className="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 text-gray-600 mb-3 sm:mb-4" />
              <div className="text-2xl sm:text-3xl font-bold text-gray-900">{"< 2 min"}</div>
              <div className="text-gray-600 text-xs sm:text-sm lg:text-base">Average Processing Time</div>
            </div>
            <div className="flex flex-col items-center">
              <Target className="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 text-gray-600 mb-3 sm:mb-4" />
              <div className="text-2xl sm:text-3xl font-bold text-gray-900">99.9%</div>
              <div className="text-gray-600 text-xs sm:text-sm lg:text-base">Accuracy Rate</div>
            </div>
          </div>
        </div>
      </section>

      {/* Why Choose Section */}
      <section className="py-12 sm:py-16 lg:py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-3 sm:mb-4">
              Why Choose FinancialConsult?
            </h2>
            <p className="text-base sm:text-lg lg:text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed px-4 sm:px-0">
              Our platform simplifies insurance comparison with cutting-edge technology and user-friendly design.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6 sm:gap-8">
            <Card className="p-6 sm:p-8 text-center border border-gray-200 shadow-sm bg-white hover:shadow-md transition-shadow">
              <CardContent className="pt-4 sm:pt-6">
                <Upload className="w-10 h-10 sm:w-12 sm:h-12 text-gray-700 mx-auto mb-4 sm:mb-6" strokeWidth={1.5} />
                <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">Easy PDF Upload</h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  Simply upload your insurance quotes in PDF format and let our AI extract the information
                  automatically.
                </p>
              </CardContent>
            </Card>

            <Card className="p-6 sm:p-8 text-center border border-gray-200 shadow-sm bg-white hover:shadow-md transition-shadow">
              <CardContent className="pt-4 sm:pt-6">
                <BarChart3 className="w-10 h-10 sm:w-12 sm:h-12 text-gray-700 mx-auto mb-4 sm:mb-6" strokeWidth={1.5} />
                <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">Smart Comparison</h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  Our intelligent algorithm compares quotes and highlights the best features, premiums, and coverage
                  options.
                </p>
              </CardContent>
            </Card>

            <Card className="p-6 sm:p-8 text-center border border-gray-200 shadow-sm bg-white hover:shadow-md transition-shadow">
              <CardContent className="pt-4 sm:pt-6">
                <Shield className="w-10 h-10 sm:w-12 sm:h-12 text-gray-700 mx-auto mb-4 sm:mb-6" strokeWidth={1.5} />
                <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">Secure & Private</h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  Your data is encrypted and secure. We never share your personal information with third parties.
                </p>
              </CardContent>
            </Card>

            <Card className="p-6 sm:p-8 text-center border border-gray-200 shadow-sm bg-white hover:shadow-md transition-shadow">
              <CardContent className="pt-4 sm:pt-6">
                <FileBarChart
                  className="w-10 h-10 sm:w-12 sm:h-12 text-gray-700 mx-auto mb-4 sm:mb-6"
                  strokeWidth={1.5}
                />
                <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">Detailed Reports</h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  Generate comprehensive comparison reports that you can download or email to yourself.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-12 sm:py-16 lg:py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-3 sm:mb-4">How It Works</h2>
            <p className="text-base sm:text-lg lg:text-xl text-gray-600">Get started in three simple steps</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
            <Card className="p-6 sm:p-8 text-center border-0 shadow-lg hover:shadow-xl transition-shadow">
              <CardContent className="pt-4 sm:pt-6">
                <div className="w-12 h-12 sm:w-16 sm:h-16 bg-black text-white rounded-full flex items-center justify-center text-lg sm:text-xl font-bold mx-auto mb-4 sm:mb-6">
                  01
                </div>
                <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4">Upload Your Quotes</h3>
                <p className="text-gray-600 text-sm sm:text-base">
                  Upload multiple insurance quote PDFs from different providers.
                </p>
              </CardContent>
            </Card>

            <Card className="p-6 sm:p-8 text-center border-0 shadow-lg hover:shadow-xl transition-shadow">
              <CardContent className="pt-4 sm:pt-6">
                <div className="w-12 h-12 sm:w-16 sm:h-16 bg-black text-white rounded-full flex items-center justify-center text-lg sm:text-xl font-bold mx-auto mb-4 sm:mb-6">
                  02
                </div>
                <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4">AI Processing</h3>
                <p className="text-gray-600 text-sm sm:text-base">
                  Our AI extracts and categorizes all the important information.
                </p>
              </CardContent>
            </Card>

            <Card className="p-6 sm:p-8 text-center border-0 shadow-lg hover:shadow-xl transition-shadow">
              <CardContent className="pt-4 sm:pt-6">
                <div className="w-12 h-12 sm:w-16 sm:h-16 bg-black text-white rounded-full flex items-center justify-center text-lg sm:text-xl font-bold mx-auto mb-4 sm:mb-6">
                  03
                </div>
                <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-3 sm:mb-4">Compare & Decide</h3>
                <p className="text-gray-600 text-sm sm:text-base">
                  View side-by-side comparisons and make informed decisions.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 sm:py-16 lg:py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-3 sm:mb-4">
            Ready to Compare Your Insurance Quotes?
          </h2>
          <p className="text-base sm:text-lg lg:text-xl text-gray-600 mb-6 sm:mb-8 max-w-3xl mx-auto leading-relaxed px-4 sm:px-0">
            Join thousands of customers who have saved time and money by using our platform.
          </p>
          <Link href="/signup">
            <Button className="bg-black text-white hover:bg-gray-800 px-6 sm:px-8 py-3 text-sm sm:text-base lg:text-lg w-full sm:w-auto">
              Start Your Free Account →
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black text-white py-8 sm:py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
            <div className="sm:col-span-2 lg:col-span-1">
              <h3 className="text-lg font-semibold mb-3 sm:mb-4">FinancialConsult</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Making insurance comparison simple and transparent.
              </p>
            </div>

            <div>
              <h4 className="text-base sm:text-lg font-semibold mb-3 sm:mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Features
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Pricing
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Security
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="text-base sm:text-lg font-semibold mb-3 sm:mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    About
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Contact
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Support
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="text-base sm:text-lg font-semibold mb-3 sm:mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Terms of Service
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Cookie Policy
                  </Link>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-6 sm:mt-8 pt-6 sm:pt-8 text-center text-gray-400">
            <p className="text-xs sm:text-sm">© 2025 FinancialConsult. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
