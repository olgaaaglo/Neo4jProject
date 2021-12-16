from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class Queries:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

#CREATE CONSTRAINT ON (p:Project) ASSERT p.name IS UNIQUE
    def create_project(self, project_name, nr_students):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_project, project_name, nr_students)
        return result

    @staticmethod
    def _create_and_return_project(tx, project_name, nr_students):
        query = (
            """MERGE (p:Project {name: $project_name})
                ON CREATE SET p.nr_students = $nr_students"""
        )
        result = tx.run(query, project_name=project_name, nr_students=nr_students)
        try:
            return [{"p": row["p"]["name"], "n": row["p"]["nr_students"]}
                    for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def add_student_to_project(self, project_name, student_fname, student_lname):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._add_student_to_project_and_return, project_name, student_fname, student_lname)
        return result

    @staticmethod
    def _add_student_to_project_and_return(tx, project_name, student_fname, student_lname):
        query = (
            """MATCH (p:Project {name: $project_name}) 
            WITH p OPTIONAL MATCH (s:Student)-[:WORKS_ON]->(p)
            WITH COUNT(s) as nr, p
            WHERE nr < toInteger(p.nr_students)
            MATCH (s2:Student {fname: $student_fname, lname: $student_lname})
            MERGE (s2)-[:WORKS_ON]->(p) return s2, p"""
        )
        result = tx.run(query, project_name=project_name, student_fname=student_fname, student_lname=student_lname)
        try:
            return [{"p": row["p"]["name"], "sf": row["s2"]["fname"], "sl": row["s2"]["lname"]}
                    for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    
    def find_project_team(self, project_name):
        with self.driver.session() as session:
            return session.read_transaction(self._find_and_return_project_team, project_name)

    @staticmethod
    def _find_and_return_project_team(tx, project_name):
        query = (
            """MATCH (p:Project {name: $project_name})
            MATCH (s:Student)
            WHERE (s)-[:WORKS_ON]->(p)
            RETURN p, s"""
        )
        result = tx.run(query, project_name=project_name)
        return [{"p": row["p"]["name"], "pn" : row["p"]["nr_students"],
                "s": row["s"]["fname"] + " " + row["s"]["lname"]} for row in result]

    def delete_project(self, project_name):
        with self.driver.session() as session:
            return session.read_transaction(self._delete_project, project_name)

    @staticmethod
    def _delete_project(tx, project_name):
        query = (
            """MATCH (p:Project {name: $project_name})
                DETACH DELETE p"""
        )
        result = tx.run(query, project_name=project_name)
        return result

    def delete_student_from_project(self, project_name, student_fname, student_lname):
        with self.driver.session() as session:
            return session.read_transaction(self._delete_student_from_project, project_name, student_fname, student_lname)

    @staticmethod
    def _delete_student_from_project(tx, project_name, student_fname, student_lname):
        query = (
            """OPTIONAL MATCH (s:Student {fname:$student_fname, lname:$student_lname})-[w:WORKS_ON]->(p:Project {name:$project_name}) 
                DETACH DELETE w"""
        )
        result = tx.run(query, project_name=project_name, student_fname=student_fname, student_lname=student_lname)
        return result

    def update_project(self, project_name, nr_students):
        with self.driver.session() as session:
            return session.read_transaction(self._update_and_return_project, project_name, nr_students)

    @staticmethod
    def _update_and_return_project(tx, project_name, nr_students):
        query = (
            """MATCH (p:Project {name : $project_name}) SET p.nr_students=$nr_students return p"""
        )
        result = tx.run(query, project_name=project_name, nr_students=nr_students)
        return [{"p": row["p"]["name"], "n": row["p"]["nr_students"]}
                    for row in result]

    #pokaz wszystkie projekty
    def find_all_projects(self):
        with self.driver.session() as session:
            return session.read_transaction(self._find_and_return_all_projects)

    @staticmethod
    def _find_and_return_all_projects(tx):
        query = (
            """MATCH (p:Project)
            RETURN p"""
        )
        result = tx.run(query)
        return [{"p": row["p"]["name"], "pn" : row["p"]["nr_students"]} for row in result]

        
    #pokaz projekty danego studenta
