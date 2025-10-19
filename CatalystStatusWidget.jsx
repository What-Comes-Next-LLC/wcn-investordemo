import React, { useState, useEffect } from 'react';
import './CatalystStatusWidget.css';

const CatalystStatusWidget = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  // Poll the status endpoint
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        // This will hit your Cloudflare Tunnel endpoint
        const response = await fetch('https://api.evolutions.whatcomesnextllc.ai/status');
        
        if (!response.ok) {
          throw new Error('Status endpoint unavailable');
        }

        const data = await response.json();
        setStatus(data);
        setError(null);
        setLastUpdate(new Date());
        setLoading(false);
      } catch (err) {
        console.error('Status fetch failed:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    // Fetch immediately
    fetchStatus();

    // Poll every 30 seconds
    const interval = setInterval(fetchStatus, 30000);

    // Cleanup
    return () => clearInterval(interval);
  }, []);

  // Format time ago
  const timeAgo = (timestamp) => {
    if (!timestamp) return 'Unknown';
    
    const now = new Date();
    const then = new Date(timestamp);
    const diffMs = now - then;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
  };

  if (loading) {
    return (
      <div className="status-widget loading">
        <div className="status-header">
          <h3>Checking infrastructure status...</h3>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="status-widget offline">
        <div className="status-header">
          <div className="status-indicator offline">
            <span className="status-dot">🔴</span>
            <span className="status-label">Offline</span>
          </div>
        </div>
        <div className="status-body">
          <p className="error-message">
            Demo infrastructure temporarily offline. Watch the video walkthrough above 
            to see how it works.
          </p>
        </div>
      </div>
    );
  }

  const isOnline = status?.status === 'online';

  return (
    <div className={`status-widget ${isOnline ? 'online' : 'offline'}`}>
      <div className="status-header">
        <div className={`status-indicator ${isOnline ? 'online' : 'offline'}`}>
          <span className="status-dot">{isOnline ? '🟢' : '🔴'}</span>
          <span className="status-label">
            {isOnline ? 'Infrastructure Online' : 'Offline'}
          </span>
        </div>
        
        {lastUpdate && (
          <div className="last-check">
            Last checked: {lastUpdate.toLocaleTimeString()}
          </div>
        )}
      </div>

      <div className="status-body">
        <div className="status-grid">
          <div className="status-metric">
            <div className="metric-label">Last Processed</div>
            <div className="metric-value">
              {timeAgo(status?.last_processed)}
            </div>
          </div>

          <div className="status-metric">
            <div className="metric-label">Hardware</div>
            <div className="metric-value">
              {status?.hardware || 'GTX 1060 6GB'}
            </div>
          </div>

          <div className="status-metric">
            <div className="metric-label">Location</div>
            <div className="metric-value">
              {status?.location || 'Michigan'}
            </div>
          </div>

          <div className="status-metric">
            <div className="metric-label">Avg Processing Time</div>
            <div className="metric-value">
              {status?.avg_processing_time || '~60 seconds'}
            </div>
          </div>

          {status?.queue_depth !== undefined && (
            <div className="status-metric">
              <div className="metric-label">Current Queue</div>
              <div className="metric-value">
                {status.queue_depth} {status.queue_depth === 1 ? 'job' : 'jobs'}
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="status-footer">
        <p className="status-note">
          <strong>Live Infrastructure:</strong> This status is polled from actual 
          hardware every 30 seconds. When you see "Online," the Catalyst pipeline 
          is ready to process Sparks.
        </p>
      </div>
    </div>
  );
};

export default CatalystStatusWidget;
