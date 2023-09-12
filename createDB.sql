CREATE TABLE korisnik (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ime CHAR(50) NOT NULL,
    prezime CHAR(50) NOT NULL,
    datum_uclanjenja DATE NOT NULL,
    datum_clanarina DATE NOT NULL,
    kilaza INTEGER
);

CREATE TABLE kategorija (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    naziv VARCHAR(100)
);

CREATE TABLE napredak (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datum_pocetak DATE,
    datum_napredak DATE,
    id_korisnika INT,
    id_kategorije INT,
    kilaza_napredak INTEGER,
    FOREIGN KEY (id_korisnika) REFERENCES korisnik(id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (id_kategorije) REFERENCES kategorija(id) ON UPDATE CASCADE ON DELETE SET NULL
);

INSERT INTO kategorija (naziv) VALUES
    ('Summer challenge'),
    ('Sparta challenge'),
    ('Iron body');