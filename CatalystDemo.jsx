import React, { useState, useEffect } from 'react';
import './CatalystDemo.css';
import CatalystStatusWidget from './CatalystStatusWidget';

// Import your logos
import SparkLogo from './assets/The_Spark.png';
import ClipboardLogo from './assets/Coach_s_Clipboard.png';
import WCNLogo from './assets/What_Comes_Next.png';

const CatalystDemo = () => {
  const [isVideoPlaying, setIsVideoPlaying] = useState(false);

  return (
    <div className="catalyst-demo-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="logo-lockup">
            <img src={WCNLogo} alt="What Comes Next" className="wcn-logo" />
            <h1 className="hero-title">The Catalyst</h1>
            <p className="hero-subtitle">Privacy-First Behavioral Intelligence</p>
          </div>
          
          <p className="hero-description">
            Watch how we extract structured insights from voice notes using 
            local LLM infrastructure. No cloud APIs. No data harvesting. 
            Just your hardware, your data, your intelligence.
          </p>
        </div>
      </section>

      {/* Video Demo Section */}
      <section className="video-section">
        <div className="section-header">
          <h2>See It In Action</h2>
          <p>Watch The Catalyst process a real Spark from transcription to intelligence</p>
        </div>

        <div className="video-container">
          {/* Placeholder for your 9:16 video */}
          <div className="video-wrapper portrait">
            <div className="video-placeholder">
              <div className="placeholder-content">
                <svg 
                  width="80" 
                  height="80" 
                  viewBox="0 0 80 80" 
                  fill="none" 
                  className="play-icon"
                  onClick={() => setIsVideoPlaying(true)}
                >
                  <circle cx="40" cy="40" r="40" fill="#216869" opacity="0.1"/>
                  <circle cx="40" cy="40" r="35" fill="#216869"/>
                  <path 
                    d="M32 28L56 40L32 52V28Z" 
                    fill="white"
                  />
                </svg>
                <p className="placeholder-text">
                  Video Demo<br />
                  <span className="placeholder-specs">1080 × 1920 (9:16)</span>
                </p>
              </div>
            </div>
            {/* Replace placeholder with your actual video element:
            <video 
              className="demo-video"
              controls
              poster="./path-to-poster.jpg"
            >
              <source src="./path-to-your-video.mp4" type="video/mp4" />
            </video>
            */}
          </div>

          <div className="video-caption">
            <p>
              <strong>What you're seeing:</strong> catalyst_demo.py processing 
              a Spark through faster-whisper transcription, Mistral analysis, 
              and structured markdown output. This is running on a GTX 1060 
              in an apartment in Michigan.
            </p>
          </div>
        </div>
      </section>

      {/* The Proof Section - Status Widget */}
      <section className="proof-section">
        <div className="section-header">
          <h2>This Isn't a Mock Demo</h2>
          <p>The status below is live. This infrastructure is running right now.</p>
        </div>

        <CatalystStatusWidget />

        <div className="proof-explanation">
          <p>
            Every time someone tests the demo, you'll see the "Last Processed" 
            timestamp update. The hardware specs are real. The location is real. 
            This is the infrastructure that powers The Catalyst backend for 
            Coach's Clipboard.
          </p>
        </div>
      </section>

      {/* The Architecture Section */}
      <section className="architecture-section">
        <div className="section-header">
          <h2>How It Works</h2>
          <p>Full transparency. Here's the actual architecture.</p>
        </div>

        <div className="architecture-diagram">
          <div className="flow-step">
            <div className="step-icon">📱</div>
            <div className="step-content">
              <h3>Your Spark</h3>
              <p>Upload a voice note or video</p>
            </div>
          </div>

          <div className="flow-arrow">→</div>

          <div className="flow-step">
            <div className="step-icon">🔊</div>
            <div className="step-content">
              <h3>faster-whisper</h3>
              <p>Speech-to-text transcription</p>
            </div>
          </div>

          <div className="flow-arrow">→</div>

          <div className="flow-step">
            <div className="step-icon">🧠</div>
            <div className="step-content">
              <h3>Mistral 7B</h3>
              <p>Behavioral intelligence analysis</p>
            </div>
          </div>

          <div className="flow-arrow">→</div>

          <div className="flow-step">
            <div className="step-icon">📊</div>
            <div className="step-content">
              <h3>Structured Output</h3>
              <p>Categories, insights, energy levels</p>
            </div>
          </div>
        </div>

        <div className="tech-specs">
          <div className="spec-card">
            <h4>Hardware</h4>
            <ul>
              <li>GTX 1060 6GB (inference)</li>
              <li>ZFS SAN (storage)</li>
              <li>Gigabit LAN</li>
            </ul>
          </div>

          <div className="spec-card">
            <h4>Software</h4>
            <ul>
              <li>Ollama + Mistral 7B</li>
              <li>faster-whisper</li>
              <li>FastAPI wrapper</li>
            </ul>
          </div>

          <div className="spec-card">
            <h4>Privacy</h4>
            <ul>
              <li>Local processing only</li>
              <li>No cloud APIs</li>
              <li>Inference stored, media stays local</li>
            </ul>
          </div>
        </div>

        <div className="cta-whitepaper">
          <p>
            Want to build your own? Read the full technical whitepaper.
          </p>
          <a href="/whitepaper" className="btn-primary">
            Download Whitepaper
          </a>
        </div>
      </section>

      {/* The Ecosystem Section */}
      <section className="ecosystem-section">
        <div className="section-header">
          <h2>The Catalyst Powers Our Product Ecosystem</h2>
          <p>Local intelligence extraction for privacy-first coaching infrastructure</p>
        </div>

        <div className="product-grid">
          <div className="product-card">
            <img src={SparkLogo} alt="The Spark" className="product-logo" />
            <h3>The Spark</h3>
            <p className="product-tag">Client App • Free</p>
            <p>
              Mobile habit tracking through photos and voice notes. 
              Progress visualization and Coach's Notes delivery.
            </p>
          </div>

          <div className="product-card">
            <img src={ClipboardLogo} alt="Coach's Clipboard" className="product-logo" />
            <h3>Coach's Clipboard</h3>
            <p className="product-tag">B2B SaaS • $149/mo</p>
            <p>
              CRM for independent coaches. Client management, Evolution tracking, 
              and Catalyst-powered insights. Unlimited clients.
            </p>
          </div>

          <div className="product-card catalyst-card">
            <div className="catalyst-logo">
              <div className="ellipsis-dots">
                <span className="dot">•</span>
                <span className="dot">•</span>
                <span className="dot">•</span>
              </div>
            </div>
            <h3>The Catalyst</h3>
            <p className="product-tag">Backend Infrastructure</p>
            <p>
              Behavioral intelligence engine. Pattern recognition, Coach's Notes 
              generation, DITL creation. Runs locally for privacy.
            </p>
          </div>
        </div>

        <div className="ecosystem-note">
          <p>
            <strong>The Catalyst</strong> is the intelligence layer that makes 
            The Spark useful and Coach's Clipboard powerful. It extracts behavioral 
            patterns from longitudinal data without ever touching the cloud.
          </p>
        </div>
      </section>

      {/* Footer Section */}
      <footer className="demo-footer">
        <div className="footer-content">
          <div className="footer-branding">
            <img src={WCNLogo} alt="What Comes Next" className="footer-logo" />
            <p className="footer-tagline">
              Innovation • Iteration • Evolution
            </p>
          </div>

          <div className="footer-links">
            <a href="https://whatcomesnextllc.ai">whatcomesnextllc.ai</a>
            <span className="separator">•</span>
            <a href="/whitepaper">Technical Whitepaper</a>
            <span className="separator">•</span>
            <a href="mailto:jason@whatcomesnextllc.ai">Contact</a>
          </div>

          <div className="footer-note">
            <p>
              Running on hardware in Michigan, not AWS.<br />
              Privacy by architecture, not policy.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default CatalystDemo;
