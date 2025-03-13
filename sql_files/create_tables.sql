CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
	current_topic integer DEFAULT 1,
    current_stage integer DEFAULT 1,
    stance TEXT,
    is_audio_enabled BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE conversation_history (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    role VARCHAR(10) CHECK (role IN ('user', 'system')),
    message TEXT NOT NULL,
	current_topic INT NOT NULL,
    current_stage INT NOT NULL,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	-- Cascading deletion where if a user is deleted, all its conversation history will be cleared as well
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE knowledge (
    id SERIAL PRIMARY KEY,
	user_id BIGINT NOT NULL,
    fact TEXT NOT NULL,
    topic INT NOT NULL,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Cascading deletion where if a user is deleted, all the knowledge with the user will be cleared as well
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE contradicting_facts (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    fact_id INT NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key reference to the users table
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Foreign key reference to the knowledge table
    FOREIGN KEY (fact_id) REFERENCES knowledge(id) ON DELETE CASCADE
);