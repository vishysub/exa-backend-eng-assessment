
CREATE TABLE bundle (
    id SERIAL PRIMARY KEY,
    resource jsonb
);

INSERT INTO bundle VALUES (1,  '{"name": {"fire":"test","age": 23}, "tags": ["Improvements", "Office"], "finished": true}');
GRANT ALL PRIVILEGES ON DATABASE fhir TO postgres;