// =============================================================================
// API SERVICE - Backend Integration Layer
// =============================================================================
// This file handles all HTTP requests to the backend API

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api';

// -----------------------------------------------------------------------------
// Session Management
// -----------------------------------------------------------------------------

export async function createSession() {
  const response = await fetch(`${API_BASE_URL}/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  return response.json(); // { sessionCode: "1234" }
}

export async function getSession(sessionCode) {
  const response = await fetch(`${API_BASE_URL}/sessions/${sessionCode}`);
  return response.json();
}

// -----------------------------------------------------------------------------
// Reflection Mode (Post-Class Feedback)
// -----------------------------------------------------------------------------

export async function submitFeedback(sessionCode, data) {
  const response = await fetch(`${API_BASE_URL}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sessionCode,
      sessionNumber: data.sessionNum,
      stuck: data.signals.stuck,
      gotIt: data.signals.gotIt,
      pause: data.signals.pause,
      example: data.signals.example,
      confidence: data.confidence
    })
  });
  return response.json();
}

export async function getClassAnalytics(sessionCode, sessionNum) {
  const response = await fetch(
    `${API_BASE_URL}/analytics/${sessionCode}/${sessionNum}`
  );
  return response.json();
}

export async function getSessionComparison(sessionCode) {
  const response = await fetch(
    `${API_BASE_URL}/analytics/${sessionCode}/compare`
  );
  return response.json();
}

// -----------------------------------------------------------------------------
// Live Mode (Real-Time Signals)
// -----------------------------------------------------------------------------

export async function sendLiveSignal(sessionCode, signal, confidence) {
  const response = await fetch(`${API_BASE_URL}/live/signal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sessionCode,
      signalType: signal,
      confidence,
      timestamp: new Date().toISOString()
    })
  });
  return response.json();
}

export async function getLiveSignals(sessionCode) {
  const response = await fetch(`${API_BASE_URL}/live/signals/${sessionCode}`);
  return response.json();
}

// -----------------------------------------------------------------------------
// WebSocket for Real-Time Updates (Live Mode)
// -----------------------------------------------------------------------------

export function connectToLiveSession(sessionCode, onSignalReceived) {
  const ws = new WebSocket(`ws://localhost:3000/live/${sessionCode}`);

  ws.onmessage = (event) => {
    const signal = JSON.parse(event.data);
    onSignalReceived(signal);
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  return ws; // Return so caller can close connection
}

// -----------------------------------------------------------------------------
// CSV Export
// -----------------------------------------------------------------------------

export async function exportSessionCSV(sessionCode) {
  const response = await fetch(
    `${API_BASE_URL}/export/${sessionCode}/csv`
  );
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `session_${sessionCode}_${new Date().toISOString().split('T')[0]}.csv`;
  a.click();
}
