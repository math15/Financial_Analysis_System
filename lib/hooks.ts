"use client";

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

export function useUploadQuotes() {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const uploadFiles = async (files: File[]) => {
    setUploading(true);
    setError(null);
    
    try {
      const response = await insuranceAPI.uploadQuotes(files);
      if (response.error) {
        setError(response.error);
        return null;
      }
      return response.data;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
      return null;
    } finally {
      setUploading(false);
    }
  };

  return { uploadFiles, uploading, error };
} 