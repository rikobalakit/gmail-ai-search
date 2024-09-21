CREATE TABLE IF NOT EXISTS emails (
    id VARCHAR PRIMARY KEY,
    subject TEXT,
    sender TEXT,
    snippet TEXT,
    bodyraw TEXT,
    bodyclean TEXT,
    timestamp BIGINT
);