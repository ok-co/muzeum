DROP TABLE IF EXISTS Artysci CASCADE;
DROP TABLE IF EXISTS Eksponaty CASCADE;
DROP TABLE IF EXISTS Galerie CASCADE;
DROP TABLE IF EXISTS Historia CASCADE;
DROP TABLE IF EXISTS Instytucje CASCADE;
DROP TABLE IF EXISTS Sale CASCADE;

CREATE TABLE Artysci (
    id              SERIAL      PRIMARY KEY,
    imie            varchar(64) NOT NULL,
    nazwisko        varchar(64) NOT NULL,
    rok_urodzenia   int         NOT NULL,
    rok_smierci     int,

    CONSTRAINT poprawny_urodzenia   CHECK (rok_urodzenia > 0),
    CONSTRAINT poprawny_smierci     CHECK (rok_smierci > 0),
    CONSTRAINT poprawny_wiek        CHECK (rok_smierci>rok_urodzenia)
);

CREATE TABLE Eksponaty (
    id              SERIAL      PRIMARY KEY,
    tytul           varchar(64) NOT NULL,
    typ             varchar(64) NOT NULL,
    wysokosc        int         NOT NULL,
    szerokosc       int         NOT NULL,
    waga            int         NOT NULL,
    cenny           boolean     NOT NULL,
    id_tworcy       int         REFERENCES Artysci(id) NOT NULL,

    CONSTRAINT poprawna_wysokosc    CHECK (wysokosc>0),
    CONSTRAINT poprawna_szerokosc   CHECK (szerokosc>0),
    CONSTRAINT poprawna_waga        CHECK (waga > 0)
);

CREATE TABLE Galerie (
    id              SERIAL      PRIMARY KEY,
    nazwa           varchar(64) NOT NULL
);


CREATE TABLE Instytucje (
    id              SERIAL      PRIMARY KEY,
    nazwa           varchar(64) NOT NULL,
    miasto          varchar(64) NOT NULL
);

CREATE TABLE Sale (
    id              int         PRIMARY KEY,
    id_galerii      int         REFERENCES Galerie(id) NOT NULL
);
CREATE TABLE Historia (
    id              SERIAL      PRIMARY KEY,
    status          char(16)    NOT NULL,
    id_eksponatu    int         REFERENCES Eksponaty(id) NOT NULL,
    id_instytucji   int         REFERENCES Instytucje(id),
    id_galerii      int         REFERENCES Galerie(id),
    id_sali         int         REFERENCES Sale(id),
    data_poczatku   date        NOT NULL,
    data_konca      date,

    CONSTRAINT poprawny_okres CHECK (data_konca > data_konca),
    CONSTRAINT poprawny_status CHECK (status in ('magazyn', 'wystawa', 'wypozyczenie')),
    CONSTRAINT warunki_stanu CHECK (
        (status = 'magazyn' AND id_instytucji IS NULL AND id_galerii IS NULL AND id_sali IS NULL) OR
        (status = 'wystawa' AND id_instytucji IS NULL AND id_galerii IS NOT NULL AND id_sali IS NOT NULL) OR
        (status = 'wypozyczenie' AND id_instytucji IS NOT NULL AND id_galerii IS NULL AND id_sali IS NULL)
    )
);

CREATE OR REPLACE FUNCTION dodaj_eksponat(
    _tytul varchar(64),
    _typ varchar(64),
    _wysokosc int,
    _szerokosc int,
    _waga int,
    _cenny boolean,
    _id_tworcy int
) RETURNS int AS $$
DECLARE
    _id int;
BEGIN
    INSERT INTO Eksponaty (tytul, typ, wysokosc, szerokosc, waga, cenny, id_tworcy)
    VALUES (_tytul, _typ, _wysokosc, _szerokosc, _waga, _cenny, _id_tworcy)
    RETURNING id INTO _id;
    RETURN _id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION dodaj_artyste(
    _imie varchar(64),
    _nazwisko varchar(64),
    _rok_urodzenia int,
    _rok_smierci int
) RETURNS int AS $$
DECLARE
    _id int;
BEGIN
    INSERT INTO Artysci (imie, nazwisko, rok_urodzenia, rok_smierci)
    VALUES (_imie, _nazwisko, _rok_urodzenia, _rok_smierci) RETURNING id into _id;
    RETURN _id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION dodaj_galerie(
    _nazwa varchar(64)
) RETURNS int AS $$
DECLARE
    _id int;
BEGIN
    INSERT INTO Galerie (nazwa)
    VALUES (_nazwa) RETURNING id INTO _id;
    RETURN _id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION dodaj_sale(
    _id int,
    _id_galerii int
) RETURNS int AS $$
BEGIN
    INSERT INTO Sale (id, id_galerii)
    VALUES (_id, _id_galerii);
    RETURN _id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION dodaj_instytucje(
    _nazwa varchar(64),
    _miasto varchar(64)
) RETURNS int AS $$
DECLARE
    _id int;
BEGIN
    INSERT INTO Instytucje (nazwa, miasto)
    VALUES (_nazwa, _miasto) RETURNING id INTO _id;
    RETURN _id;
END;
$$ LANGUAGE plpgsql;

