CREATE OR REPLACE PROCEDURE multiple_inserting(
    names VARCHAR[],
    phones VARCHAR[],
    INOUT incorrect_data text[] default '{}'
    )

LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
    phone_valid BOOLEAN;
    error TEXT;
BEGIN
    incorrect_data := ARRAY[]::TEXT[];

    IF array_length(names, 1) IS DISTINCT FROM array_length(phones, 1) THEN
        RAISE EXCEPTION 'Names and phones arrays have different lengths';
    END IF;
    
    FOR i IN 1..array_length(names, 1)
    LOOP
        phone_valid := validate_phone(phones[i]);
        
        IF phone_valid THEN
            INSERT INTO contacts (name, number) 
            VALUES (names[i], phones[i]);
        ELSE
            error := format('Name: "%s", Phone: "%s" - Invalid phone format', 
                                   names[i], phones[i]);
            incorrect_data := array_append(incorrect_data, error);
        END IF;
    END LOOP;
    
    RAISE NOTICE 'Processed: % contacts', array_length(names, 1);
    RAISE NOTICE 'Successfully inserted: %', array_length(names, 1) - array_length(incorrect_data, 1);
    RAISE NOTICE 'Failed: %', array_length(incorrect_data, 1);
    
END;
$$;
CREATE OR REPLACE PROCEDURE delete_contact(
    search_value VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF
    EXISTS(SELECT 1 FROM contacts WHERE name = search_value OR number = search_value) 
    THEN
    DELETE FROM contacts WHERE name = search_value OR number = search_value;
    RAISE NOTICE 'The contact deleted';
    ELSE
    RAISE NOTICE 'The contact doesnt exist';
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR)

LANGUAGE plpgsql
AS $$
DECLARE
    id_of_contact INTEGER;
BEGIN
    id_of_contact := (SELECT id FROM contacts WHERE name = p_contact_name);
    INSERT INTO phones(contact_id, phone, type) VALUES (id_of_contact, p_phone, p_type);
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE
    id_of_group INTEGER;
BEGIN
    IF
    EXISTS(SELECT 1 FROM groups WHERE name = p_group_name) 
    THEN
    id_of_group := (SELECT id FROM groups WHERE name = p_group_name);
    UPDATE contacts SET group_id = id_of_group WHERE name = p_contact_name;
    ELSE
    INSERT INTO groups(name) VALUES (p_group_name);
    id_of_group := (SELECT id FROM groups WHERE name = p_group_name);
    UPDATE contacts SET group_id = id_of_group WHERE name = p_contact_name;
    END IF;
END;
$$;