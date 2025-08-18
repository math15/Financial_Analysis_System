/** @type {import('next').NextConfig} */
import bundleAnalyzer from '@next/bundle-analyzer';

const withBundleAnalyzer = bundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
});

const nextConfig = {
  // Experimental features
  experimental: {
    optimizePackageImports: ['lucide-react', '@radix-ui/react-icons'],
  },

  // Development configuration - Fix for cross-origin warnings
  allowedDevOrigins: [
    'mailbroker.ddns.net',
    'apimailbroker.ddns.net',
    'localhost',
    '127.0.0.1',
  ],

  // Image optimization
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'mailbroker.ddns.net',
      },
      {
        protocol: 'http',
        hostname: 'localhost',
      },
    ],
    formats: ['image/webp', 'image/avif'],
  },

  // PWA-like features
  headers: async () => [
    {
      source: '/(.*)',
      headers: [
        {
          key: 'X-Content-Type-Options',
          value: 'nosniff',
        },
        {
          key: 'X-Frame-Options',
          value: 'DENY',
        },
        {
          key: 'X-XSS-Protection',
          value: '1; mode=block',
        },
        {
          key: 'Referrer-Policy',
          value: 'origin-when-cross-origin',
        },
      ],
    },
  ],

  // API routes configuration
  async rewrites() {
    return [
      {
        source: '/api/backend/:path*',
        destination: process.env.NODE_ENV === 'production' 
          ? 'https://apimailbroker.ddns.net/:path*'
          : 'http://localhost:5000/:path*',
      },
    ];
  },

  // Environment variables
  env: {
    BACKEND_URL: process.env.NODE_ENV === 'production' 
      ? 'https://apimailbroker.ddns.net'
      : 'http://localhost:5000',
    FRONTEND_URL: process.env.NODE_ENV === 'production' 
      ? 'https://mailbroker.ddns.net'
      : 'http://localhost:3000',
  },

  // Build optimization
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // Output configuration
  output: 'standalone',  // Restored for production deployment
  
  // Webpack configuration
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Performance optimizations
    config.optimization.splitChunks = {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
        common: {
          name: 'common',
          minChunks: 2,
          chunks: 'all',
          enforce: true,
        },
      },
    };

    // Handle PDF files
    config.resolve.alias.canvas = false;
    config.resolve.alias.encoding = false;

    return config;
  },

  // TypeScript configuration
  typescript: {
    ignoreBuildErrors: false,
  },

  // ESLint configuration
  eslint: {
    ignoreDuringBuilds: false,
  },

  // Static optimization
  trailingSlash: false,
  poweredByHeader: false,

  // Compression
  compress: true,

  // Development configuration
  devIndicators: {
    buildActivity: true,
    buildActivityPosition: 'bottom-right',
  },
};

export default withBundleAnalyzer(nextConfig);
