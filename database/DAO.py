from rich._ratio import Edge

from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """
            SELECT DISTINCT year(s.`datetime`)
            FROM sighting s 
            Order by year(s.`datetime`) DESC 
            """
            cursor.execute(query)

            for row in cursor:
                result.append(row[0])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllShape():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """
            SELECT DISTINCT s.shape 
            FROM sighting s 
            WHERE s.shape <> ""
            """
            cursor.execute(query)

            for row in cursor:
                result.append(row[0])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAvvistamenti(anno, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
            SELECT s.*
            FROM sighting s 
            WHERE year(s.`datetime`) = %s
            AND s.shape = %s
            """
            cursor.execute(query, (anno, shape))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(anno, shape, idMapShapes):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """
            SELECT a1.id as a1, a2.id as a2
            FROM (
                SELECT DISTINCT s.id, s.`datetime`, s.state 
                FROM sighting s 
                WHERE year(s.`datetime`) = %s
                AND s.shape = %s
            ) as a1,
            (
                SELECT DISTINCT s.id, s.`datetime`, s.state 
                FROM sighting s 
                WHERE year(s.`datetime`) = %s
                AND s.shape = %s
            ) as a2, neighbor n 
            WHERE a1.state = a2.state 
            AND a1.`datetime` < a2.`datetime`
            GROUP BY a1.id, a2.id
            """

            queryV2 = """
            SELECT a1.id as a1, a2.id as a2
            FROM sighting a1, sighting a2
            WHERE a1.state = a2.state 
            AND a1.`datetime` < a2.`datetime`
            AND year(a1.`datetime`) = %s
            AND a1.shape = %s
            AND year(a2.`datetime`) = %s
            AND a2.shape = %s
            """
            cursor.execute(queryV2, (anno, shape, anno, shape))

            for row in cursor:

                result.append((idMapShapes[row[0]], idMapShapes[row[1]]))

            cursor.close()
            cnx.close()
        return result




