// API client for insurance quote comparison backend
// Place this file in your Next.js project (e.g., lib/api.ts)

// Auto-detect API base URL based on current location
const getApiBaseUrl = () => {
  // Client-side detection
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;
    
    if (hostname === 'mailbroker.ddns.net') {
      // Production environment - backend on apimailbroker.ddns.net
      return `${protocol}//apimailbroker.ddns.net`;
    }
  }
  
  // Default to localhost for development
  return 'http://localhost:5000';
};

const API_BASE_URL = getApiBaseUrl();
const AUTH_TOKEN = 'demo-token'; // Replace with proper authentication

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

interface QuoteUploadResponse {
  comparison_id: string;
  status: string;
  message: string;
  quote_count: number;
  results: QuoteResult[];
}

interface QuoteResult {
  quote_number: number;
  vendor: string;
  total_premium: string;
  payment_terms: string;
  contact_phone: string;
  contact_email: string;
  risk_address: string;
  client_details: string;
  quote_reference: string;
  quote_date: string;
  policy_sections: Record<string, PolicySection>;
}

interface PolicySection {
  included: string;
  premium: string;
  sum_insured: string;
  sub_sections: string[];
  excess: string;
}

interface UserStats {
  total_quotes: number;
  completed: number;
  processing: number;
  average_premium: string;
}

interface QuoteSummary {
  comparison_id: string;
  created_at: string;
  status: string;
  quote_count: number;
  file_names: string[];
  total_premiums: string[];
}

class InsuranceAPI {
  private baseURL: string;
  private authToken: string;

  constructor(baseURL: string = API_BASE_URL, authToken: string = AUTH_TOKEN) {
    this.baseURL = baseURL;
    this.authToken = authToken;
    
    // Log the API URL for debugging
    console.log(`🔗 Insurance API initialized with base URL: ${this.baseURL}`);
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseURL}${endpoint}`;
      console.log(`📡 API Request: ${options.method || 'GET'} ${url}`);
      
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.authToken}`,
          // Force HTTP/1.1 to avoid HTTP/2 ping failures
          'Connection': 'keep-alive',
          'Upgrade-Insecure-Requests': '1',
          ...options.headers,
        },
        // Force HTTP/1.1 mode
        keepalive: true,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      console.error('API request failed:', error);
      
      // Handle specific network errors
      if (error instanceof TypeError && error.message.includes('fetch')) {
        return { error: 'Network error: Unable to connect to server. Please check your connection.' };
      }
      
      if (error instanceof Error && error.message.includes('HTTP2_PING_FAILED')) {
        return { error: 'Network protocol error: HTTP/2 connection failed. Please try again.' };
      }
      
      return { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  // Health check
  async healthCheck(): Promise<ApiResponse<{ status: string; timestamp: string }>> {
    return this.request('/api/health');
  }

  // Upload quote files
  async uploadQuotes(files: File[]): Promise<ApiResponse<QuoteUploadResponse>> {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      console.log(`📤 Uploading ${files.length} files to ${this.baseURL}/api/quotes/upload`);
      
      const response = await fetch(`${this.baseURL}/api/quotes/upload`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.authToken}`,
          // Force HTTP/1.1 to avoid HTTP/2 ping failures
          'Connection': 'keep-alive',
          'Upgrade-Insecure-Requests': '1',
          // Add explicit content type for multipart
          'Accept': 'application/json',
        },
        body: formData,
        // Force HTTP/1.1 mode
        keepalive: true,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Upload failed: ${response.status}`);
      }

      const data = await response.json();
      console.log(`✅ Upload successful: ${data.message}`);
      return { data };
    } catch (error) {
      console.error('Upload failed:', error);
      
      // Handle specific network errors
      if (error instanceof TypeError && error.message.includes('fetch')) {
        return { error: 'Network error: Unable to connect to server. Please check your connection.' };
      }
      
      if (error instanceof Error && error.message.includes('HTTP2_PING_FAILED')) {
        return { error: 'Network protocol error: HTTP/2 connection failed. Please try again.' };
      }
      
      return { error: error instanceof Error ? error.message : 'Upload failed' };
    }
  }

  // Get comparison results
  async getComparison(comparisonId: string): Promise<ApiResponse<QuoteResult[]>> {
    return this.request(`/api/quotes/compare/${comparisonId}`);
  }

  // Get user quotes
  async getUserQuotes(): Promise<ApiResponse<{ total_comparisons: number; comparisons: QuoteSummary[] }>> {
    return this.request('/api/quotes/my-quotes');
  }

  // Get user stats for dashboard
  async getUserStats(): Promise<ApiResponse<UserStats>> {
    return this.request('/api/quotes/stats');
  }

  // Generate report
  async generateReport(comparisonId: string): Promise<ApiResponse<{ 
    report_id: string; 
    filename: string; 
    download_url: string; 
    generated_at: string 
  }>> {
    return this.request(`/api/quotes/generate-report/${comparisonId}`, {
      method: 'POST',
    });
  }

  // Download report
  getReportDownloadUrl(filename: string): string {
    return `${this.baseURL}/api/reports/download/${filename}`;
  }
}

// Create and export API instance
export const insuranceAPI = new InsuranceAPI();

// Export types for use in components
export type {
  QuoteUploadResponse,
  QuoteResult,
  PolicySection,
  UserStats,
  QuoteSummary,
  ApiResponse,
}; 