"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Mail } from "lucide-react"

export default function ForgotPasswordPage() {
  const [emailSent, setEmailSent] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setEmailSent(true)
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="text-center">
          <Link href="/">
            <h1 className="text-2xl font-bold text-gray-900 mb-2 cursor-pointer hover:text-gray-700">
              FinancialConsult
            </h1>
          </Link>
          <p className="text-gray-600">Compare insurance quotes effortlessly</p>
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <Card className="shadow-lg border-0">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-bold text-gray-900">
              {emailSent ? "Check your email" : "Forgot your password?"}
            </CardTitle>
            <p className="text-gray-600">
              {emailSent
                ? "We've sent a password reset link to your email address"
                : "Enter your email address and we'll send you a link to reset your password"}
            </p>
          </CardHeader>
          <CardContent className="space-y-6">
            {emailSent ? (
              <div className="text-center space-y-4">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                  <Mail className="w-8 h-8 text-green-600" />
                </div>
                <p className="text-sm text-gray-600">
                  If an account with that email exists, we've sent you a password reset link. Please check your email
                  and follow the instructions.
                </p>
                <p className="text-xs text-gray-500">Didn't receive the email? Check your spam folder or try again.</p>
                <Button onClick={() => setEmailSent(false)} variant="outline" className="w-full">
                  Try again
                </Button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="email" className="text-sm font-medium text-gray-700">
                    Email
                  </Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    placeholder="Enter your email address"
                    className="mt-1"
                    required
                  />
                </div>

                <Button type="submit" className="w-full bg-black text-white hover:bg-gray-800">
                  Send reset link
                </Button>
              </form>
            )}

            <div className="text-center">
              <Link href="/signin" className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to sign in
              </Link>
            </div>
          </CardContent>
        </Card>

        <div className="mt-8 text-center">
          <p className="text-xs text-gray-500">© 2025 FinancialConsult. All rights reserved.</p>
        </div>
      </div>
    </div>
  )
}
