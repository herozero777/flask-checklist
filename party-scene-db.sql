-- Creating passwords table
CREATE TABLE access_passwd (
    id SERIAL PRIMARY KEY,
    password VARCHAR NOT NULL
);

-- Inserting password
INSERT INTO access_passwd (password) VALUES ('sceneon');

-- Creating treat_given_people table
CREATE TABLE treat_given_ppl (
    id SERIAL PRIMARY KEY,
    person VARCHAR NOT NULL
);

-- Creating treat_pending_people table
CREATE TABLE treat_pending_ppl (
    id SERIAL PRIMARY KEY,
    person VARCHAR NOT NULL
);

-- Inserting treat given people
INSERT INTO treat_given_ppl (person) VALUES ('Mohammad Ismail');

-- Inserting treat pending people
INSERT INTO treat_pending_ppl (person) VALUES ('Umar Farroq');