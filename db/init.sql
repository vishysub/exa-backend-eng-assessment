
CREATE TABLE bundle (
    id SERIAL PRIMARY KEY,
    resource jsonb
);

GRANT ALL PRIVILEGES ON DATABASE fhir TO postgres;