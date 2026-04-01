CREATE TABLE IF NOT EXISTS submissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  learner_id TEXT,
  unit TEXT NOT NULL,
  qno INTEGER NOT NULL,
  mode TEXT NOT NULL,
  prompt_japanese TEXT NOT NULL,
  correct_answer TEXT NOT NULL,
  user_answer TEXT NOT NULL,
  ipa_us TEXT,
  source_audio TEXT,
  source_image TEXT,
  user_agent TEXT,
  client_timestamp TEXT
);

CREATE INDEX IF NOT EXISTS idx_submissions_unit_qno
ON submissions (unit, qno);

CREATE INDEX IF NOT EXISTS idx_submissions_created_at
ON submissions (created_at);
