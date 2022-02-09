CREATE TABLE IF NOT EXISTS question_data (
    class_name TEXT NOT NULL,
    due_date TEXT,
    question TEXT NOT NULL,
    question_type TEXT NOT NULL,
    primary_hash TEXT NOT NULL PRIMARY KEY,
    secondary_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS message_ids (
    primary_hash TEXT NOT NULL PRIMARY KEY,
    message_id TEXT NOT NULL,
    FOREIGN KEY (primary_hash) REFERENCES question_data(primary_hash)
);
