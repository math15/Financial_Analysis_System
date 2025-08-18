// React hooks for Insurance API integration
// Place this file in your Next.js project (e.g., lib/hooks.ts)

import { useState, useEffect } from 'react';
import { insuranceAPI, UserStats, QuoteSummary } from './api';

export function useUserStats() {
  const [stats, setStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = async () => {
    setLoading(true);
    const response = await insuranceAPI.getUserStats();
    if (response.data) {
      setStats(response.data);
      setError(null);
    } else {
      setError(response.error || 'Failed to fetch stats');
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return { stats, loading, error, refetch: fetchStats };
}

export function useUserQuotes() {
  const [quotes, setQuotes] = useState<QuoteSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchQuotes = async () => {
    setLoading(true);
    const response = await insuranceAPI.getUserQuotes();
    if (response.data) {
      setQuotes(response.data.comparisons);
      setError(null);
    } else {
      setError(response.error || 'Failed to fetch quotes');
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchQuotes();
  }, []);

  return { quotes, loading, error, refetch: fetchQuotes };
} 