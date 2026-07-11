-- PostgeSQL db user script

    CREATE ROLE python_user WITH
        LOGIN
        NOSUPERUSER
        NOCREATEDB
        NOCREATEROLE
        INHERIT
        NOREPLICATION
        NOBYPASSRLS
        CONNECTION LIMIT -1
        PASSWORD 'xxxxxx';

    GRANT pg_write_all_data, pg_read_all_data TO python_user;
    COMMENT ON ROLE python_user IS 'Used by Python automations to write data and feed visualisations';

-- PostgreSQL Adzuna table*

    CREATE TABLE adzuna_jobs (
        id                  BIGINT PRIMARY KEY,
        title               TEXT NOT NULL,
        description         TEXT,
        company_name        TEXT,
        salary_min          NUMERIC(10,2),
        salary_max          NUMERIC(10,2),
        salary_is_predicted BOOLEAN,
        contract_type       TEXT,
        contract_time       TEXT,
        category_label      TEXT,
        latitude            NUMERIC(9,6),
        longitude           NUMERIC(9,6),
        location_display    TEXT,
        location_area       TEXT,
        redirect_url        TEXT,
        adref               TEXT,
        is_active           BOOLEAN DEFAULT TRUE,
        created             TIMESTAMPTZ,
        last_seen_at        TIMESTAMPTZ DEFAULT now(),
        inserted_at         TIMESTAMPTZ DEFAULT now()
    );

    -- Add indexes if needed later
    -- CREATE INDEX idx_adzuna_jobs_created ON adzuna_jobs (created);
    -- CREATE INDEX idx_adzuna_jobs_category_tag ON adzuna_jobs (category_tag);