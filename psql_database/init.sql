-- Database Initialization Script for Multi-Agent System
-- This script creates the necessary tables, constraints, and indexes to support your project.


----LISTEN/NOTIFY messaging between Nodes----
-- 6. Table for inter-agent communication (LISTEN/NOTIFY mechanism)
-- with each messageloaded in table: new instance=row with this parameters=columns will be created
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,         -- Unique identifier for each notification
    channel_name VARCHAR(50) NOT NULL,          -- Channel name for the notification (could be the agent name)
    sender_agent VARCHAR(50) NOT NULL,          -- Agent sending the notification
    receiver_agent VARCHAR(50) NOT NULL,        -- Agent receiving the notification
    message_payload JSONB,                      -- Payload of the notification (data)
    sent_at TIMESTAMP DEFAULT NOW(),            -- Timestamp of when the notification was sent
    acknowledged BOOLEAN DEFAULT FALSE          -- Acknowledgment flag to track whether the notification has been processed
);





-- 7. Table for logging activities and system performance
--for logger routines that will convert this data into text
CREATE TABLE system_logs (
    log_id SERIAL PRIMARY KEY,                  -- Unique identifier for each log entry
    component VARCHAR(50) NOT NULL,            -- System component generating the log
    log_level VARCHAR(10) NOT NULL,            -- Log level (e.g., INFO, ERROR, DEBUG)
    message TEXT NOT NULL,                     -- Log message
    timestamp TIMESTAMP DEFAULT NOW()          -- When the log entry was recorded
);

-- Indexes for performance optimization
--use with LISTEN/NOTIFY tables for faster and lighter messaging