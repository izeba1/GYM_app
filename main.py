from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from datetime import datetime
import sys
import sqlite3
from utilities import razlika_datuma, kilaza_razlika, program_id_provjera, provjera_korisnickog_unosa, \
    provjera_isteka_clanarine, provjera_korisnickog_unosa_napredak
from enumeratori import Kategorija

con = sqlite3.connect("gymDB.db")
cur = con.cursor()

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GYM')
        self.setGeometry(200, 200, 600, 505)
        self.setWindowIcon(QtGui.QIcon('images/gym_logo.png'))
        self.initUI()
        self.prikazi_clanove()
        self.napredak_prikazi()

    def initUI(self):
        self.font = QtGui.QFont('Arial', 8)

# Unos člana teretane
        # Frame za unos člana
        self.frame_unos_korisnika = QtWidgets.QFrame(self)
        self.frame_unos_korisnika.setGeometry(QtCore.QRect(10, 10, 581, 211))
        self.frame_unos_korisnika.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_unos_korisnika.setFrameShadow(QtWidgets.QFrame.Plain)

        # Frame za label 'Unos člana'
        self.frame_unos_clana = QtWidgets.QFrame(self.frame_unos_korisnika)
        self.frame_unos_clana.setGeometry(QtCore.QRect(0, 0, 81, 31))
        self.frame_unos_clana.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_unos_clana.setFrameShadow(QtWidgets.QFrame.Plain)

        # Label 'Unos člana'
        self.label_unos_clana = QtWidgets.QLabel(self.frame_unos_clana)
        self.label_unos_clana.setGeometry(QtCore.QRect(10, 0, 71, 31))

        # Grid layout za unos člana
        self.gridLayoutWidget = QtWidgets.QWidget(self.frame_unos_korisnika)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 201, 171))
        self.gridLayout_clan = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_clan.setContentsMargins(0, 0, 0, 0)

        # Label ime
        self.label_ime = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout_clan.addWidget(self.label_ime, 0, 0, 1, 1)

        # Text ime
        self.text_ime = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout_clan.addWidget(self.text_ime, 0, 1, 1, 1)

        # Label prezime
        self.label_prezime = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout_clan.addWidget(self.label_prezime, 1, 0, 1, 1)

        # Text prezime
        self.text_prezime = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.text_prezime.setText("")
        self.gridLayout_clan.addWidget(self.text_prezime, 1, 1, 1, 1)

        # Label kilaža
        self.label_kilaza = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout_clan.addWidget(self.label_kilaza, 2, 0, 1, 1)

        # Text kilaža
        self.text_kilaza = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout_clan.addWidget(self.text_kilaza, 2, 1, 1, 1)

        # Label datum učlanjenja
        self.label_datum_uclanjenja = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout_clan.addWidget(self.label_datum_uclanjenja, 3, 0, 1, 1)

        # DateEdit za datum učlanjenja, prikazuje današnji datum (radi probe funkcije provjere članarine)
        self.dateEdit_datum_uclanjenja = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.gridLayout_clan.addWidget(self.dateEdit_datum_uclanjenja, 3, 1, 1, 1)
        danasnji_datum = QDate.currentDate()
        self.dateEdit_datum_uclanjenja.setDate(danasnji_datum)

        # Vertical layout za popis članova
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame_unos_korisnika)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(220, 10, 351, 191))
        self.verticalLayout_popis_clanova = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_popis_clanova.setContentsMargins(0, 0, 0, 0)

        # List za ispis clanova
        self.list_clan = QtWidgets.QListWidget(self)
        self.list_clan.setStyleSheet("background-color: rgb(255, 255, 255);")

        # ScrollArea popis članova
        self.scrollArea_popis_korisnika = QtWidgets.QScrollArea(self)
        self.scrollArea_popis_korisnika.setMinimumSize(QtCore.QSize(347, 91))
        self.scrollArea_popis_korisnika.setWidgetResizable(True)
        self.scrollArea_popis_korisnika.setLayout(QtWidgets.QVBoxLayout())
        self.scrollArea_popis_korisnika.setWidget(self.list_clan)
        self.verticalLayout_popis_clanova.addWidget(self.scrollArea_popis_korisnika)

        # Gumb za unos člana
        self.pushButton_unos_clana = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.verticalLayout_popis_clanova.addWidget(self.pushButton_unos_clana)
        self.pushButton_unos_clana.clicked.connect(self.unos_korisnika)

        # Gumb za brisanje člana
        self.pushButton_obrisi_clana = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.verticalLayout_popis_clanova.addWidget(self.pushButton_obrisi_clana)
        self.pushButton_obrisi_clana.clicked.connect(self.brisanje_korisnika)

        # Gumb za obnavljanje članarine
        self.pushButton_obnova = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.verticalLayout_popis_clanova.addWidget(self.pushButton_obnova)
        self.pushButton_obnova.clicked.connect(self.obnova_clanarine)

        # Label error unos korisnika
        self.label_error_unos_korisnik = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_error_unos_korisnik.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_error_unos_korisnik.setStyleSheet('color: red;')
        self.label_error_unos_korisnik.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_popis_clanova.addWidget(self.label_error_unos_korisnik)

# Napredak člana teretane
        # Frame napredak člana
        self.frame_napredak = QtWidgets.QFrame(self)
        self.frame_napredak.setGeometry(QtCore.QRect(10, 230, 581, 231))
        self.frame_napredak.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_napredak.setFrameShadow(QtWidgets.QFrame.Plain)

        # Frame za label 'Napredak'
        self.frame_napredak_clan = QtWidgets.QFrame(self.frame_napredak)
        self.frame_napredak_clan.setGeometry(QtCore.QRect(0, 0, 81, 31))
        self.frame_napredak_clan.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_napredak_clan.setFrameShadow(QtWidgets.QFrame.Plain)

        # Label 'Napredak'
        self.label_napredak = QtWidgets.QLabel(self.frame_napredak_clan)
        self.label_napredak.setGeometry(QtCore.QRect(10, 0, 51, 31))

        #grid layout napredak člana
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.frame_napredak)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 201, 191))
        self.gridLayout_napredak = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_napredak.setContentsMargins(0, 0, 0, 0)

        # Label kilaža
        self.label_napredak_kilaza = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.gridLayout_napredak.addWidget(self.label_napredak_kilaza, 3, 0, 1, 1)

        # Text kilaža
        self.text_napredak_kilaza = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.gridLayout_napredak.addWidget(self.text_napredak_kilaza, 3, 1, 1, 1)

        # Label datum
        self.label_datum = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.gridLayout_napredak.addWidget(self.label_datum, 1, 0, 1, 1)

        # DateEdit za napredak člana, prikazuje današnji datum
        self.dateEdit_napredak_datum = QtWidgets.QDateEdit(self.gridLayoutWidget_2)
        self.gridLayout_napredak.addWidget(self.dateEdit_napredak_datum, 1, 1, 1, 1)
        self.dateEdit_napredak_datum.setDate(danasnji_datum)

        # Label program treninga
        self.label_kategorija = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.gridLayout_napredak.addWidget(self.label_kategorija, 2, 0, 1, 1)

        # Combo box za program treninga, odabir programa treniranja
        self.comboBox_napredak_program = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.gridLayout_napredak.addWidget(self.comboBox_napredak_program, 2, 1, 1, 1)
        for kategorija in Kategorija:
            self.comboBox_napredak_program.addItem(str(kategorija.value))

        # Label za unos id-a člana
        self.label_clan = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.gridLayout_napredak.addWidget(self.label_clan, 0, 0, 1, 1)

        # Text unos id-a člana
        self.text_napredak_clan = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.gridLayout_napredak.addWidget(self.text_napredak_clan, 0, 1, 1, 1)

        # Vertical layout za ispis napretka
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.frame_napredak)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(220, 10, 351, 211))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Scrol area za napredak članova
        self.scrollArea_napredak = QtWidgets.QScrollArea(self.verticalLayoutWidget_2)
        self.scrollArea_napredak.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 347, 178))

        # Table za napredak članova
        self.tableWidget_napredak = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget_napredak.setGeometry(QtCore.QRect(0, 0, 351, 161))
        self.tableWidget_napredak.setColumnCount(4)
        self.tableWidget_napredak.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_napredak.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_napredak.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_napredak.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_napredak.setHorizontalHeaderItem(3, item)
        self.scrollArea_napredak.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea_napredak)

        # Push buton za unos napretka člana
        self.pushButton_napredak_unesi = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.verticalLayout.addWidget(self.pushButton_napredak_unesi)
        self.pushButton_napredak_unesi.clicked.connect(self.napredak_unesi)

        # Label error napredak
        self.label_error_napredak = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_error_napredak.setAlignment(QtCore.Qt.AlignCenter)
        self.label_error_napredak.setStyleSheet('color: red;')
        self.verticalLayout.addWidget(self.label_error_napredak)

        # Postavljanje teksta za labele
        self.retranslateUi(Window)

# Tekst za labele
    def retranslateUi(self, Window):
        _translate = QtCore.QCoreApplication.translate
        self.label_unos_clana.setText(_translate("GYM", "Unos člana"))
        self.label_datum_uclanjenja.setText(_translate("GYM", "Datum"))
        self.label_ime.setText(_translate("GYM", "Ime"))
        self.label_prezime.setText(_translate("GYM", "Prezime"))
        self.label_kilaza.setText(_translate("GYM", "Kilaža"))
        self.pushButton_unos_clana.setText(_translate("GYM", "Unesi"))
        self.pushButton_obrisi_clana.setText(_translate("GYM", "Obriši"))
        self.pushButton_obnova.setText(_translate("GYM", "Obnovi članarinu"))
        self.label_napredak.setText(_translate("GYM", "Napredak"))
        self.label_napredak_kilaza.setText(_translate("GYM", "Kilaža"))
        self.label_datum.setText(_translate("GYM", "Datum"))
        self.label_kategorija.setText(_translate("GYM", "Program treninga"))
        self.label_clan.setText(_translate("GYM", "Član"))
        item = self.tableWidget_napredak.horizontalHeaderItem(0)
        item.setText(_translate("GYM", "Član"))
        item = self.tableWidget_napredak.horizontalHeaderItem(1)
        item.setText(_translate("GYM", "Dani"))
        item = self.tableWidget_napredak.horizontalHeaderItem(2)
        item.setText(_translate("GYM", "Program treninga"))
        item = self.tableWidget_napredak.horizontalHeaderItem(3)
        item.setText(_translate("GYM", "Razlika kilaže"))
        self.pushButton_napredak_unesi.setText(_translate("GYM", "Unesi"))
        self.label_error_napredak.setText(_translate("GYM", ""))
        self.label_error_unos_korisnik.setText(_translate("GYM", ""))


  # Ispis članova prilikom paljenja aplikacije
    def prikazi_clanove(self):
        self.list_clan.clear()
        self.text_ime.setText('')
        self.text_prezime.setText('')
        self.text_kilaza.setText('')
        danasnji_datum = QDate.currentDate()
        self.dateEdit_datum_uclanjenja.setDate(danasnji_datum)

        # Dohvaćanje članova iz baze podataka
        query = """
             SELECT * FROM korisnik;
         """
        clan = cur.execute(query).fetchall()

        for podatak_clan in clan:
            status_clanarine = provjera_isteka_clanarine(podatak_clan[4])
            # Ako je članarina istekla
            if status_clanarine == 'ISTEKLA':
                tekst = f'{podatak_clan[0]}. {podatak_clan[1]} {podatak_clan[2]} ' \
                    f'     Članarina: ISTEKLA!'
            # Ako članarina nije istekla
            else:
                tekst = f'{podatak_clan[0]}. {podatak_clan[1]} {podatak_clan[2]} ' \
                f'     Učlanjenje: {podatak_clan[4]}     Kilaža: {podatak_clan[5]}'

            self.list_clan.addItem(tekst)
            self.label_error_unos_korisnik.setText("")

    # Unos člana, dodavanje u bazu podataka i ponovni prikaz članova u listi
    def unos_korisnika(self):
        # Provjera unesenih podataka
        error_korisnik = provjera_korisnickog_unosa(self.text_ime.text(), self.text_prezime.text(),
                                                    self.text_kilaza.text())

        # Unos korisnika i spremanje u bazu podataka, samo ako su podatci ispravno uneseni
        if error_korisnik is None:
            # Prevođenje dateEdit u string željenog oblika
            qdate = self.dateEdit_datum_uclanjenja.date()
            datum = qdate.toPyDate()
            datum_uclanjenja = datum.strftime('%d.%m.%Y.')

            # Datum učlanjenja se sprema dva puta za istog korisnika te pomoću jednog datuma se provjerava članarina,
            # pomoću drugog se izračunavaju dani treniranja za tablicu napredak člana
            query = f"""
                        INSERT INTO korisnik (ime, prezime, datum_uclanjenja, datum_clanarina, kilaza)
                        VALUES ('{self.text_ime.text()}', '{self.text_prezime.text()}', 
                                '{datum_uclanjenja}', '{datum_uclanjenja}', '{self.text_kilaza.text()}')
                    """
            cur.execute(query)
            con.commit()
            self.prikazi_clanove()
        else:
            self.label_error_unos_korisnik.setText(error_korisnik)
            self.text_ime.setText('')
            self.text_prezime.setText('')
            self.text_kilaza.setText('')
            danasnji_datum = QDate.currentDate()
            self.dateEdit_datum_uclanjenja.setDate(danasnji_datum)

    # Brisanje člana iz liste i baze podataka
    def brisanje_korisnika(self):
        lista_clanova = self.list_clan.selectedItems()

        for c in lista_clanova:
            # Dobivanje teksta člana koji se briše
            obrisani_clan = c.text()
            # Razdvajanje stringa na dijelove, dohvaćanje prvog elementa liste (id)
            clan_id = obrisani_clan.split('.')[0]
            # Brisanje člana iz liste
            self.list_clan.takeItem(self.list_clan.row(c))
            # Brisanje člana iz baze podataka koristeći id
            query = """
                        DELETE FROM korisnik WHERE id = ?
                    """
            cur.execute(query, (clan_id,))
            con.commit()
            self.label_error_unos_korisnik.setText("Korisnik obrisan!")
            self.napredak_prikazi()

    # Obnova članarine
    def obnova_clanarine(self):
        odabrani_clan = self.list_clan.currentItem()

        if odabrani_clan:
            # Dohvaćanje id-a odabranog člana
            tekst_clana = odabrani_clan.text()
            clan_id = tekst_clana.split('.')[0]
            # Dohvaćanje trenutnog datuma
            danasnji_datum = datetime.now()
            # Obnova članarine za odabranog člana
            query = f"""
                        UPDATE korisnik
                        SET datum_clanarina = '{danasnji_datum.strftime('%d.%m.%Y.')}'
                        WHERE id = '{clan_id}'
                    """
            cur.execute(query)
            con.commit()
            # Osvežavanje prikaza članova, ispis Članarina obnovljena! u label error
            self.prikazi_clanove()
            self.napredak_prikazi()
            self.label_error_unos_korisnik.setText("Članarina obnovljena!")

    # Prikaz napretka članova
    def napredak_prikazi(self):
        # Dohvaćanje podataka o napretku članova iz baze podataka
        query = """
                    SELECT ime, prezime, datum_pocetak, datum_napredak, naziv, kilaza, kilaza_napredak, datum_clanarina FROM korisnik
                    INNER JOIN napredak ON korisnik.id = napredak.id_korisnika
                    LEFT JOIN kategorija ON napredak.id_kategorije = kategorija.id
                """
        data = cur.execute(query).fetchall()

        # Postavljanje broja redaka u QTableWidget na temelju broja rezultata iz baze
        self.tableWidget_napredak.setRowCount(len(data))
        #clanarina = provjera_isteka_clanarine(data)

        # Popunjavanje table widgeta podacima iz baze
        for row, row_data in enumerate(data):
            clanarina = provjera_isteka_clanarine(row_data[7])
            if clanarina == 'ISTEKLA':
                item = QtWidgets.QTableWidgetItem(f"{row_data[0]} {row_data[1]}")
                self.tableWidget_napredak.setItem(row, 0, item)
                item = QtWidgets.QTableWidgetItem("Članarina istekla!")
                self.tableWidget_napredak.setItem(row, 1, item)

            else:
                # Ime i prezime u prvom stupcu
                item = QtWidgets.QTableWidgetItem(f"{row_data[0]} {row_data[1]}")
                self.tableWidget_napredak.setItem(row, 0, item)

                # Razlika u danima između datum_pocetak i datum_napredak
                # Računa se broj dana treniranja
                razlika_dana = razlika_datuma(row_data[2], row_data[3])

                # Dani treniranja u drugom stupcu
                if razlika_dana is not None:
                    item = QtWidgets.QTableWidgetItem(str(razlika_dana))

                self.tableWidget_napredak.setItem(row, 1, item)

                # Naziv programa treniranja u trećem stupcu
                item = QtWidgets.QTableWidgetItem(row_data[4])
                self.tableWidget_napredak.setItem(row, 2, item)

                # Računanje razlike između početne kilaze i trenutne
                razlika_kilaze = kilaza_razlika(row_data[5], row_data[6])

                # Razlika kilaze u četvrtom stupcu
                if razlika_kilaze is not None:
                    item = QtWidgets.QTableWidgetItem(str(razlika_kilaze))

                self.tableWidget_napredak.setItem(row, 3, item)

        # Onemogućavanje uređivanja tablice tokom korištenja aplikacije
        self.tableWidget_napredak.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.label_error_napredak.setText('')
        self.text_napredak_clan.setText('')
        self.text_napredak_kilaza.setText('')
        danasnji_datum = QDate.currentDate()
        self.dateEdit_napredak_datum.setDate(danasnji_datum)

    # Unos napretka članova
    def napredak_unesi(self):
        # Odabir podataka korisnika iz baze pomoću unesenog id-a
        query_id_korisnika = """
                                SELECT id, ime, prezime, datum_uclanjenja, kilaza FROM korisnik WHERE id = ?
                            """
        cur.execute(query_id_korisnika, (self.text_napredak_clan.text(),))
        korisnik_podaci = cur.fetchone()

        if korisnik_podaci:
            id_korisnik = korisnik_podaci[0]
            datum_pocetak = korisnik_podaci[3]
            error_napredak = provjera_korisnickog_unosa_napredak(self.text_napredak_clan.text(), self.text_napredak_kilaza.text())
            if error_napredak is None:
                # Dohvaćanje id-a programa treniranja pomoću odabira imena programa u comboBoxu
                program_id = program_id_provjera(self.comboBox_napredak_program.currentText())
                if program_id is not None:
                    query = """
                        SELECT id, datum_pocetak, datum_napredak, kilaza_napredak FROM napredak WHERE id_korisnika = ? 
                    """
                    cur.execute(query, (id_korisnik,))
                    postojeci_clan = cur.fetchone()

                    # Prevođenje dateEdit u string željenog oblika
                    qdate = self.dateEdit_napredak_datum.date()
                    datum = qdate.toPyDate()
                    napredak_datum = datum.strftime('%d.%m.%Y.')

                    if postojeci_clan:
                        # Ažuriranje podataka ako već postoji unos za tog korisnika
                        query = f"""
                                    UPDATE napredak
                                    SET id_kategorije = ?,
                                        datum_napredak = ?,
                                        kilaza_napredak = ?
                                    WHERE id = ?
                                """
                        values = (program_id, napredak_datum, self.text_napredak_kilaza.text(), postojeci_clan[0])
                    else:
                        # Ako ne postoji, dodavanje novog unosa
                        query = """
                            INSERT INTO napredak (datum_pocetak, datum_napredak, id_korisnika, id_kategorije, kilaza_napredak)
                            VALUES (?, ?, ?, ?, ?)
                        """
                        values = (datum_pocetak, napredak_datum, id_korisnik, program_id, self.text_napredak_kilaza.text())

                    cur.execute(query, values)
                    con.commit()
                    self.napredak_prikazi()
                else:
                    self.label_error_napredak.setText("Odaberite program treninga!")
            else:
                self.label_error_napredak.setText(error_napredak)
        else:
            self.label_error_napredak.setText("Član s unesenim ID-om ne postoji.")


app = QtWidgets.QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())