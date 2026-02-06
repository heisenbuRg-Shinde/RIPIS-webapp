import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

// Subtopics mapping for each domain
const SUBTOPICS = {
    DSA: [
        { value: 'array', label: '📊 Array' },
        { value: 'string', label: '🔤 String' },
        { value: 'linked_list', label: '🔗 Linked List' },
        { value: 'tree', label: '🌳 Tree' },
        { value: 'graph', label: '🕸️ Graph' },
        { value: 'dynamic_programming', label: '📈 Dynamic Programming' },
        { value: 'sorting', label: '📶 Sorting' },
        { value: 'searching', label: '🔍 Searching' }
    ],
    OS: [
        { value: 'deadlock', label: '🔒 Deadlock' },
        { value: 'process_scheduling', label: '⏱️ Process Scheduling' },
        { value: 'memory_management', label: '💾 Memory Management' },
        { value: 'synchronization', label: '🔄 Synchronization' }
    ],
    DBMS: [
        { value: 'normalization', label: '📐 Normalization' },
        { value: 'transactions', label: '💳 Transactions' },
        { value: 'indexing', label: '📑 Indexing' },
        { value: 'joins', label: '🔀 Joins' },
        { value: 'query_optimization', label: '⚡ Query Optimization' }
    ]
};

export default function Reasoning() {
    const { user, logout, token } = useAuth();

    // --- State Declarations ---
    const [interviewType, setInterviewType] = useState('coding');
    const [domain, setDomain] = useState('');
    const [subtopic, setSubtopic] = useState('');
    const [voiceAssisted, setVoiceAssisted] = useState(false);
    const [isListening, setIsListening] = useState(false);
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [captionText, setCaptionText] = useState('');

    // --- Helper Functions ---

    const handleDomainChange = (e) => {
        setDomain(e.target.value);
        setSubtopic('');
    };

    const speakResponse = (text) => {
        if (!voiceAssisted || !text) return;
        window.speechSynthesis.cancel();

        // Update caption
        setCaptionText(text);

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1;
        utterance.pitch = 1;

        utterance.onend = () => {
            // Clear caption after speech ends (plus small buffer)
            setTimeout(() => setCaptionText(''), 3000);
        };

        window.speechSynthesis.speak(utterance);
    };

    const handleSubmit = async (e) => {
        if (e && e.preventDefault) e.preventDefault();
        setError('');
        setLoading(true);
        setResults(null);
        window.speechSynthesis.cancel(); // Stop any pending speech

        try {
            const response = await fetch('/api/reasoning', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    interview_type: interviewType,
                    domain,
                    subtopic: subtopic || null,
                    voice_assisted: voiceAssisted
                })
            });

            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Session expired. Please login again.');
                }
                throw new Error('Failed to generate reasoning');
            }

            const data = await response.json();
            setResults(data);

            // Speak response if voice assisted mode is ON
            if (voiceAssisted && data.voice_script) {
                speakResponse(data.voice_script);
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleVoiceCommand = (command) => {
        if (!command) return;

        // Domain selection
        if (command.includes('dsa') || command.includes('data structure')) {
            setDomain('DSA');
            setSubtopic('');
            speakResponse("Selected DSA.");
        } else if (command.includes('os') || command.includes('operating system')) {
            setDomain('OS');
            setSubtopic('');
            speakResponse("Selected Operating Systems.");
        } else if (command.includes('dbms') || command.includes('database')) {
            setDomain('DBMS');
            setSubtopic('');
            speakResponse("Selected DBMS.");
        }

        // Topic selection (simple matching)
        if (domain) {
            const topics = SUBTOPICS[domain];
            const foundTopic = topics?.find(t => command.includes(t.label.split(' ')[1].toLowerCase()));
            if (foundTopic) {
                setSubtopic(foundTopic.value);
                speakResponse(`Selected subtopic ${foundTopic.label.split(' ')[1]}.`);
            }
        }

        // Generate action
        if (command.includes('generate') || command.includes('reason')) {
            speakResponse("Generating reasoning.");
            // We pass a mock event or nothing, handleSubmit handles it.
            handleSubmit({ preventDefault: () => { } });
        }
    };

    // --- Effects ---

    // Auto-start listening when voice mode is enabled
    useEffect(() => {
        let recognition = null;

        if (voiceAssisted) {
            if (!('webkitSpeechRecognition' in window)) {
                setError('Voice recognition not supported in this browser.');
                setVoiceAssisted(false);
                return;
            }

            recognition = new window.webkitSpeechRecognition();
            recognition.continuous = true; // Continuous listening
            recognition.lang = 'en-US';
            recognition.interimResults = false;

            recognition.onstart = () => {
                setIsListening(true);
                setError('');
            };

            recognition.onresult = (event) => {
                const lastResultIndex = event.results.length - 1;
                const transcript = event.results[lastResultIndex][0].transcript.toLowerCase();
                console.log('Voice Command:', transcript);
                handleVoiceCommand(transcript);
            };

            recognition.onerror = (event) => {
                console.error('Voice recognition error:', event.error);
                if (event.error === 'not-allowed') {
                    setError('Microphone access denied. Please allow permission.');
                    setVoiceAssisted(false);
                }
            };

            recognition.onend = () => {
                // Auto-restart if still enabled (for "always on" feel)
                if (voiceAssisted && recognition) {
                    try {
                        recognition.start();
                    } catch (e) {
                        // Already started or busy
                    }
                } else {
                    setIsListening(false);
                }
            };

            try {
                recognition.start();
            } catch (e) {
                console.error('Failed to start recognition:', e);
            }
        } else {
            setIsListening(false);
            if (window.speechSynthesis) window.speechSynthesis.cancel();
        }

        return () => {
            if (recognition) {
                recognition.onend = null; // Prevent restart on cleanup
                recognition.stop();
            }
        };
    }, [voiceAssisted, domain]); // Re-run when toggle changes

    return (
        <div className="app-container">
            {/* Header */}
            <header className="header">
                <div className="logo">
                    <span className="logo-icon">&lt;/&gt;</span>
                    <h1>RIPIS</h1>
                </div>
                <p className="tagline">Interview Practice Intelligence System</p>
            </header>

            {/* Floating Caption Bar - Showing feedback when listening OR speaking */}
            {(captionText || isListening) && (
                <div className="caption-bar">
                    {captionText || "Listening..."}
                    {isListening && !captionText && <span className="listening-indicator">🔴</span>}
                </div>
            )}

            {/* Main Grid */}
            <main className="main-grid">
                {/* Sidebar */}
                <aside className="sidebar">
                    {/* User Info */}
                    <div className="glass-card user-info">
                        <span className="user-name">👤 {user?.username}</span>
                        <button className="logout-btn" onClick={logout}>Logout</button>
                    </div>

                    {/* Configuration Panel */}
                    <div className="glass-card panel">
                        <h2 className="panel-title">
                            <span className="panel-icon">⚙️</span> Configuration
                        </h2>

                        <form className="auth-form" onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label htmlFor="interview-type">Interview Type</label>
                                <select
                                    id="interview-type"
                                    value={interviewType}
                                    onChange={(e) => setInterviewType(e.target.value)}
                                >
                                    <option value="coding">💻 Coding</option>
                                    <option value="theory">📚 Theory</option>
                                </select>
                            </div>

                            <div className="form-group">
                                <label htmlFor="domain">Domain</label>
                                <select
                                    id="domain"
                                    value={domain}
                                    onChange={handleDomainChange}
                                    required
                                >
                                    <option value="">Select Domain...</option>
                                    <option value="DSA">🔢 DSA</option>
                                    <option value="OS">🖥️ Operating Systems</option>
                                    <option value="DBMS">🗄️ DBMS</option>
                                </select>
                            </div>

                            <div className="form-group">
                                <label htmlFor="subtopic">Subtopic</label>
                                <select
                                    id="subtopic"
                                    value={subtopic}
                                    onChange={(e) => setSubtopic(e.target.value)}
                                    disabled={!domain}
                                >
                                    <option value="">Select subtopic...</option>
                                    {domain && SUBTOPICS[domain]?.map((st) => (
                                        <option key={st.value} value={st.value}>
                                            {st.label}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div className="form-group toggle-group">
                                <div className="toggle-label">
                                    <span>Voice Based Assisted Mode</span>
                                    {isListening && <span className="listening-indicator" title="Listening... (Pulse)">🔴</span>}
                                </div>
                                <label className="toggle-switch">
                                    <input
                                        type="checkbox"
                                        checked={voiceAssisted}
                                        onChange={(e) => {
                                            setVoiceAssisted(e.target.checked);
                                            window.speechSynthesis.cancel();
                                        }}
                                    />
                                    <span className="slider"></span>
                                </label>
                            </div>

                            {/* Listening text helper if no caption bar shown */}
                            {isListening && !captionText && (
                                <div style={{ color: 'var(--orange-primary)', fontSize: '0.8rem', textAlign: 'center', marginBottom: '10px' }}>
                                    Listening...
                                </div>
                            )}

                            <button
                                type="submit"
                                className="btn btn-primary btn-full"
                                disabled={loading || !domain}
                            >
                                {loading ? 'Generating...' : 'Generate Reasoning →'}
                            </button>
                        </form>
                    </div>

                    {/* Stats Panel */}
                    <div className="glass-card panel">
                        <h3 className="panel-title">
                            <span className="panel-icon">📊</span> Coverage
                        </h3>
                        <div className="stats-grid">
                            <div className="stat">
                                <span className="stat-value">20+</span>
                                <span className="stat-label">Topics</span>
                            </div>
                            <div className="stat">
                                <span className="stat-value">3</span>
                                <span className="stat-label">Domains</span>
                            </div>
                        </div>
                    </div>
                </aside>

                {/* Content */}
                <section className="content glass-card results-container">
                    {error && <div className="message error">{error}</div>}

                    {/* Welcome State */}
                    {!loading && !results && !error && (
                        <div className="welcome-state">
                            <div className="welcome-icon">🧠</div>
                            <h2>Ready to Practice</h2>
                            <p>
                                Select a domain and subtopic to generate structured reasoning
                                hints for your interview preparation.
                            </p>
                        </div>
                    )}

                    {/* Loading State */}
                    {loading && (
                        <div className="loading-state">
                            <div className="loader"></div>
                            <p>Generating reasoning...</p>
                        </div>
                    )}

                    {/* Results */}
                    {results && (
                        <div className="results-grid">
                            <div className="glass-card result-card concept">
                                <div className="card-header">
                                    <span className="card-icon">📚</span>
                                    <h3>Theory & Concept</h3>
                                </div>
                                <div className="card-content">{results.concept}</div>
                            </div>

                            {results.syntax_structure && (
                                <div className="glass-card result-card syntax">
                                    <div className="card-header">
                                        <span className="card-icon">🧱</span>
                                        <h3>Syntax & Structure</h3>
                                    </div>
                                    <pre className="card-content code-content">{results.syntax_structure}</pre>
                                </div>
                            )}

                            <div className="glass-card result-card approach">
                                <div className="card-header">
                                    <span className="card-icon">🎯</span>
                                    <h3>Approach</h3>
                                </div>
                                <div className="card-content">{results.approach}</div>
                            </div>

                            <div className="glass-card result-card pseudocode">
                                <div className="card-header">
                                    <span className="card-icon">📝</span>
                                    <h3>Pseudocode</h3>
                                </div>
                                <pre className="card-content code-content">{results.pseudocode}</pre>
                            </div>

                            {results.example_code && (
                                <div className="glass-card result-card example-code">
                                    <div className="card-header">
                                        <span className="card-icon">💻</span>
                                        <h3>Example Code</h3>
                                    </div>
                                    <pre className="card-content code-content">{results.example_code}</pre>
                                </div>
                            )}

                            <div className="glass-card result-card mistakes">
                                <div className="card-header">
                                    <span className="card-icon">⚠️</span>
                                    <h3>Common Mistakes</h3>
                                </div>
                                <div className="card-content">{results.common_mistakes}</div>
                            </div>
                        </div>
                    )}
                </section>
            </main>

            {/* Footer */}
            {/* Footer */}
            <footer className="footer">
                <span className="footer-left">All in one interview prep site like only</span>
                <span className="footer-right">RIPIS 2026</span>
            </footer>
        </div>
    );
}
