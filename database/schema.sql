CREATE TABLE supplier (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    manager VARCHAR(100),
    phone VARCHAR(30),
    status VARCHAR(50)
);

CREATE TABLE truck (
    id SERIAL PRIMARY KEY,
    registration VARCHAR(50) NOT NULL UNIQUE,
    driver VARCHAR(100),
    capacity FLOAT,
    status VARCHAR(50)
);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    sku VARCHAR(100),
    quantity INTEGER DEFAULT 0,
    supplier_id INTEGER REFERENCES supplier(id)
);

CREATE TABLE route (
    id SERIAL PRIMARY KEY,
    origin VARCHAR(100),
    destination VARCHAR(100),
    distance_km FLOAT,
    selected BOOLEAN DEFAULT FALSE,
    truck_id INTEGER REFERENCES truck(id)
);

CREATE TABLE ticket (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(50),
    status VARCHAR(50),
    assignee VARCHAR(100),
    jira_key VARCHAR(100)
);