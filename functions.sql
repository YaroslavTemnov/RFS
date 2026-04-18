CREATE OR REPLACE FUNCTION search(info VARCHAR)
RETURNS TABLE(
    id INTEGER,
    name VARCHAR,
    number VARCHAR
)
LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN QUERY
    SELECT * FROM contacts c
    WHERE c.name LIKE '%' || info || '%' 
    OR c.number LIKE '%' || info || '%' ; 
END;
$$;

CREATE OR REPLACE FUNCTION upsert(info VARCHAR, num VARCHAR)
RETURNS VOID
LANGUAGE plpgsql
AS
$$
BEGIN
    IF 
    EXISTS(SELECT 1 FROM contacts WHERE NAME = info) THEN
    UPDATE contacts SET number = num
    WHERE name = info;
    ELSE
    INSERT INTO contacts (name, number) VALUES (info, num);
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION get_contacts (f INTEGER, q INTEGER)
RETURNS TABLE(
    id INTEGER,
    name VARCHAR,
    number VARCHAR
)
LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.number 
    FROM contacts c
    LIMIT q OFFSET f;

END;
$$;

CREATE OR REPLACE FUNCTION validate_phone(phone VARCHAR)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
BEGIN
    IF phone ~ '^[0-9+\-\(\)\s]+$' 
       AND length(phone) >= 5 
       AND length(phone) <= 20 THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$;