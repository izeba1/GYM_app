import sqlite3
from iznimke import IznimkaPrazanTekst, IznimkaKilaza
from datetime import datetime

con = sqlite3.connect("gymDB.db")
cur = con.cursor()


def provjera_isteka_clanarine(datum_uclanjenja_str):
    danasnji_datum = datetime.now().date()
    datum_uclanjenja = datetime.strptime(datum_uclanjenja_str, '%d.%m.%Y.').date()
    razlika = danasnji_datum - datum_uclanjenja

    if razlika.days > 1:
        return "ISTEKLA"

    else:
        return None


def provjera_korisnickog_unosa_napredak(id, kilaza):
    try:
        if int(id) == 0 or int(kilaza) == 0:
            raise IznimkaPrazanTekst()

    except IznimkaPrazanTekst as e:
        return str(e)

    except ValueError:
        return str('Kilaža mora biti cijeli broj!')

    else:
        return None


def program_id_provjera(program_ime):
    try:
        query = """
                    SELECT id FROM kategorija WHERE naziv = ?
                """
        cur.execute(query, (program_ime,))
        result = cur.fetchone()

        if result:
            return result[0]
        else:
            return None

    except sqlite3.Error as e:
        print("SQLite greška:", e)
        return None


def provjera_korisnickog_unosa(ime, prezime, kilaza):
    try:
        if len(ime) == 0 or len(prezime) == 0:
            raise IznimkaPrazanTekst()

        broj = int(kilaza)

        if broj < 40 or broj > 200:
            raise IznimkaKilaza()

    except IznimkaPrazanTekst as e:
        return str(e)

    except IznimkaKilaza as e:
        return str(e)

    except ValueError:
        return str('Kilaža mora biti broj!')

    else:
        return None


def kilaza_razlika(stara_kilaza, trenutna_kilaza):
    try:
        stara_kilaza = float(stara_kilaza)
        trenutna_kilaza = float(trenutna_kilaza)
        razlika = trenutna_kilaza - stara_kilaza
        return int(razlika)
    except ValueError:
        return None


def razlika_datuma(datum1_str, datum2_str):
    try:
        # Pretvaranje stringova u datetime objekte
        datum1 = datetime.strptime(datum1_str, '%d.%m.%Y.')
        datum2 = datetime.strptime(datum2_str, '%d.%m.%Y.')

        # Izračun razlike u danima
        razlika = datum2 - datum1

        # Povrat razlike u danima kao integer
        return razlika.days
    except ValueError:
        # U slučaju greške (npr. neispravan format datuma), vratite None
        return None


