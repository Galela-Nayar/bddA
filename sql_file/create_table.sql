CREATE TABLE region (
    reg VARCHAR(3) PRIMARY KEY,
    libelle VARCHAR(200) NOT NULL
);

CREATE TABLE departement (
    dep VARCHAR(3) PRIMARY KEY,
    reg VARCHAR(3) NOT NULL REFERENCES region(reg),
    libelle VARCHAR(200) NOT NULL
);

CREATE TABLE commune (
    com CHAR(5) PRIMARY KEY,
    dep VARCHAR(3) NOT NULL REFERENCES departement(dep),
    libelle VARCHAR(200) NOT NULL
);

CREATE TABLE chef_lieu_region (
    reg VARCHAR(3) PRIMARY KEY REFERENCES region(reg),
    chef_lieu CHAR(5) REFERENCES commune(com)
);

CREATE TABLE chef_lieu_departement (
    dep VARCHAR(3) PRIMARY KEY REFERENCES departement(dep),
    chef_lieu CHAR(5) REFERENCES commune(com)
);