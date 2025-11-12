import { useState } from 'react';
import Logo from './Logo';

function StudentView({ sessionCode }) {
  const [mode, setMode] = useState('reflection'); // 'reflection' or 'live'
  const [name, setName] = useState('');
  const [sessionNum, setSessionNum] = useState(1);
  const [signals, setSignals] = useState({
    stuck: 0,
    gotIt: 0,
    pause: 0,
    example: 0
  });
  const [confidence, setConfidence] = useState(3);
  const [submitted, setSubmitted] = useState(false);
  const [feedback, setFeedback] = useState('');

  const handleSignalClick = (type) => {
    setSignals(prev => ({
      ...prev,
      [type]: prev[type] + 1
    }));
  };

  const handleLiveSignal = (signal, emoji) => {
    console.log(`Live signal sent: ${signal}, Confidence: ${confidence}`);
    setFeedback(`${emoji} ${signal} sent!`);
    setTimeout(() => setFeedback(''), 2000);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitted:', { name, sessionNum, signals, confidence });
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 3000);
  };

  const totalSignals = signals.stuck + signals.gotIt + signals.pause + signals.example;

  // LIVE MODE VIEW
  if (mode === 'live') {
    return (
      <div className="student-container">
        <div className="student-card">
          <div className="student-header">
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', marginBottom: '5px' }}>
              <Logo size={35} />
              <h1 className="student-title" style={{ margin: 0 }}>LearnTwin</h1>
            </div>
            <p style={{ fontSize: '18px', fontWeight: '600', color: '#34D399', marginBottom: '5px' }}>
              🔴 LIVE Session
            </p>
            <p style={{ fontSize: '14px', marginTop: '5px' }}>
              Session: <span className="session-code">{sessionCode}</span>
            </p>
            <button
              onClick={() => setMode('reflection')}
              style={{
                marginTop: '15px',
                padding: '8px 16px',
                background: '#4F46E5',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '14px'
              }}
            >
              Switch to Reflection Mode
            </button>
          </div>

          {feedback && (
            <div className="feedback-message">
              {feedback}
            </div>
          )}

          <div style={{ marginBottom: '20px' }}>
            <p style={{ textAlign: 'center', fontSize: '14px', color: '#666', marginBottom: '15px' }}>
              Tap buttons in real-time during class
            </p>
            <div className="button-grid">
              <button
                onClick={() => handleLiveSignal('Stuck', '✋')}
                className="signal-btn stuck"
              >
                <span className="btn-emoji">✋</span>
                <span className="btn-text">Stuck</span>
              </button>

              <button
                onClick={() => handleLiveSignal('Got it', '✅')}
                className="signal-btn gotit"
              >
                <span className="btn-emoji">✅</span>
                <span className="btn-text">Got it</span>
              </button>

              <button
                onClick={() => handleLiveSignal('Pause', '⏸️')}
                className="signal-btn pause"
              >
                <span className="btn-emoji">⏸️</span>
                <span className="btn-text">Pause</span>
              </button>

              <button
                onClick={() => handleLiveSignal('Example?', '💡')}
                className="signal-btn example"
              >
                <span className="btn-emoji">💡</span>
                <span className="btn-text">Example?</span>
              </button>
            </div>
          </div>

          <div className="confidence-section">
            <label className="confidence-label">
              Confidence: <span className="confidence-value">{confidence}</span>
            </label>
            <input
              type="range"
              min="1"
              max="5"
              value={confidence}
              onChange={(e) => setConfidence(Number(e.target.value))}
              className="confidence-slider"
            />
            <div className="slider-labels">
              <span>1 (Low)</span>
              <span>2</span>
              <span>3</span>
              <span>4</span>
              <span>5 (High)</span>
            </div>
          </div>

          <p className="student-footer">
            🔴 Live mode • Real-time feedback • Anonymous
          </p>
        </div>
      </div>
    );
  }

  // REFLECTION MODE VIEW (original)
  return (
    <div className="student-container">
      <div className="student-card">
        <div className="student-header">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', marginBottom: '5px' }}>
            <Logo size={35} />
            <h1 className="student-title" style={{ margin: 0 }}>LearnTwin</h1>
          </div>
          <p>Post-Class Reflection</p>
          <p style={{ fontSize: '14px', marginTop: '5px' }}>
            Session: <span className="session-code">{sessionCode}</span>
          </p>
          <button
            onClick={() => setMode('live')}
            style={{
              marginTop: '15px',
              padding: '8px 16px',
              background: '#34D399',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            Switch to Live Mode
          </button>
        </div>

        {submitted && (
          <div className="feedback-message">
            ✅ Thank you! Your reflection has been submitted.
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Your Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your name"
              required
              style={{
                width: '100%',
                padding: '12px',
                border: '2px solid #ddd',
                borderRadius: '8px',
                fontSize: '16px'
              }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Session Number
            </label>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button
                type="button"
                onClick={() => setSessionNum(1)}
                style={{
                  flex: 1,
                  padding: '12px',
                  border: sessionNum === 1 ? '3px solid #4F46E5' : '2px solid #ddd',
                  borderRadius: '8px',
                  background: sessionNum === 1 ? '#EEF2FF' : 'white',
                  fontWeight: sessionNum === 1 ? '700' : '500',
                  cursor: 'pointer'
                }}
              >
                Session 1
              </button>
              <button
                type="button"
                onClick={() => setSessionNum(2)}
                style={{
                  flex: 1,
                  padding: '12px',
                  border: sessionNum === 2 ? '3px solid #4F46E5' : '2px solid #ddd',
                  borderRadius: '8px',
                  background: sessionNum === 2 ? '#EEF2FF' : 'white',
                  fontWeight: sessionNum === 2 ? '700' : '500',
                  cursor: 'pointer'
                }}
              >
                Session 2
              </button>
            </div>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '12px', fontWeight: '600' }}>
              How did you feel during today's class? (Tap multiple times)
            </label>
            <div className="button-grid">
              <button
                type="button"
                onClick={() => handleSignalClick('stuck')}
                className="signal-btn stuck"
              >
                <span className="btn-emoji">✋</span>
                <span className="btn-text">Stuck</span>
                <span style={{ fontSize: '14px', marginTop: '5px', display: 'block' }}>
                  {signals.stuck}x
                </span>
              </button>

              <button
                type="button"
                onClick={() => handleSignalClick('gotIt')}
                className="signal-btn gotit"
              >
                <span className="btn-emoji">✅</span>
                <span className="btn-text">Got it</span>
                <span style={{ fontSize: '14px', marginTop: '5px', display: 'block' }}>
                  {signals.gotIt}x
                </span>
              </button>

              <button
                type="button"
                onClick={() => handleSignalClick('pause')}
                className="signal-btn pause"
              >
                <span className="btn-emoji">⏸️</span>
                <span className="btn-text">Pause</span>
                <span style={{ fontSize: '14px', marginTop: '5px', display: 'block' }}>
                  {signals.pause}x
                </span>
              </button>

              <button
                type="button"
                onClick={() => handleSignalClick('example')}
                className="signal-btn example"
              >
                <span className="btn-emoji">💡</span>
                <span className="btn-text">Example?</span>
                <span style={{ fontSize: '14px', marginTop: '5px', display: 'block' }}>
                  {signals.example}x
                </span>
              </button>
            </div>
          </div>

          <div className="confidence-section">
            <label className="confidence-label">
              Overall Confidence: <span className="confidence-value">{confidence}</span>
            </label>
            <input
              type="range"
              min="1"
              max="5"
              value={confidence}
              onChange={(e) => setConfidence(Number(e.target.value))}
              className="confidence-slider"
            />
            <div className="slider-labels">
              <span>1 (Low)</span>
              <span>2</span>
              <span>3</span>
              <span>4</span>
              <span>5 (High)</span>
            </div>
          </div>

          <button
            type="submit"
            disabled={!name || totalSignals === 0}
            style={{
              width: '100%',
              padding: '16px',
              marginTop: '20px',
              background: (!name || totalSignals === 0) ? '#ccc' : '#4F46E5',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: '700',
              cursor: (!name || totalSignals === 0) ? 'not-allowed' : 'pointer'
            }}
          >
            Submit Reflection
          </button>
        </form>

        <p className="student-footer">
          Anonymous • Privacy-first • Used only to improve your learning
        </p>
      </div>
    </div>
  );
}

export default StudentView;
