CREATE TABLE groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

ALTER TABLE contacts
    ADD COLUMN email    VARCHAR(100),
    ADD COLUMN birthday DATE,
    ADD COLUMN group_id INTEGER REFERENCES groups(id);

CREATE TABLE phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20)  NOT NULL,
    type       VARCHAR(10)  CHECK (type IN ('home', 'work', 'mobile'))
);