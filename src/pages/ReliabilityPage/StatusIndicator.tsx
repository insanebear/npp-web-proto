import React from 'react';

interface StatusIndicatorProps {
  jobId: string;
  jobStatus: string;
}

const StatusIndicator: React.FC<StatusIndicatorProps> = ({ jobId, jobStatus }) => {
  return (
    <div 
      style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        padding: '32px',
        backgroundColor: 'rgba(31, 41, 55, 0.8)',
        backdropFilter: 'blur(12px)',
        borderRadius: '8px',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        color: '#ffffff',
        textAlign: 'center',
        width: '400px'
      }}
    >
      <h2 style={{ 
        fontSize: '24px', 
        fontWeight: 'bold', 
        marginBottom: '16px' 
      }}>
        Simulation Running
      </h2>
      <p style={{ fontSize: '18px' }}>
        Job Status: 
        <span style={{ 
          fontWeight: '600', 
          color: '#38bdf8', 
          marginLeft: '8px' 
        }}>
          {jobStatus}...
        </span>
      </p>
      <p style={{ 
        fontSize: '12px', 
        color: '#9ca3af', 
        marginTop: '16px', 
        wordBreak: 'break-all' 
      }}>
        Job ID: {jobId}
      </p>
    </div>
  );
};

export default StatusIndicator;