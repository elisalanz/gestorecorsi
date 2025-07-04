from database.DB_connect import DBConnect
from model.corso import Corso
from model.studente import Studente


class DAO():
    @staticmethod
    def getCodins():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT c.codins 
                    FROM corso c"""

        cursor.execute(query)

        for row in cursor:
            res.append(row["codins"])
        #processa res

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllCorsi():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT * FROM corso c"""

        cursor.execute(query)

        for row in cursor:
            # res.append(Corso(codins=row["codins"],
            #                  crediti = row["crediti"],
            #                  nome = row["nome"],
            #                  pd = row["pd"]))
            res.append(Corso(**row)) # modo più compatto
        # processa res

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getCorsiPD(pd):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT *
                    FROM corso c
                    WHERE c.pd = %s"""

        cursor.execute(query, (pd,))

        for row in cursor:
            res.append(Corso(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getCorsiPDwithIscritti(pd):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT c.codins, c.crediti, c.nome, c.pd, count(*) as n
                    FROM corso c, iscrizione i
                    WHERE c.pd = %s AND c.codins = i.codins
                    GROUP BY c.codins, c.crediti, c.nome, c.pd"""

        cursor.execute(query, (pd,))

        for row in cursor:
            res.append((Corso(row["codins"], row["crediti"], row["nome"], row["pd"]), row["n"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getStudentiCorso(codins):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT s.*
                    FROM studente s, iscrizione i
                    WHERE s.matricola = i.matricola AND i.codins =%s"""

        cursor.execute(query, (codins,))

        for row in cursor:
            res.append(Studente(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getCDSofCorso(codins):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res

        cursor = cnx.cursor(dictionary=True)

        query =   """SELECT s.CDS, count(*) as n
                        FROM studente s, iscrizione i
                        WHERE s.matricola = i.matricola AND i.codins = %s AND s.CDS !=""
                        GROUP BY s.CDS"""

        cursor.execute(query, (codins,))

        for row in cursor:
            res.append((row["CDS"], row["n"]))

        cursor.close()
        cnx.close()
        return res