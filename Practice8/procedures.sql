-- Процедура Upsert (вставить или обновить, если имя уже есть)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO contacts (name, phone)
    VALUES (p_name, p_phone)
    ON CONFLICT (name) DO UPDATE 
    SET phone = EXCLUDED.phone;
END;
$$;

-- Процедура удаления
CREATE OR REPLACE PROCEDURE delete_contact(p_search VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE name = p_search OR phone = p_search;
END;
$$;

-- Массовая вставка с проверкой длины номера
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names VARCHAR[], 
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..cardinality(p_names) LOOP
        IF LENGTH(p_phones[i]) >= 10 THEN
            INSERT INTO contacts (name, phone)
            VALUES (p_names[i], p_phones[i])
            ON CONFLICT (name) DO UPDATE SET phone = EXCLUDED.phone;
        ELSE
            RAISE NOTICE 'Invalid phone for user %: %', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;