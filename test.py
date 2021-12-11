from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_project(self, project_name, nr_students):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_project, project_name, nr_students)
        return result

    @staticmethod
    def _create_and_return_project(tx, project_name, nr_students):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            """MERGE (p:Project { name: $project_name, nr_students: $nr_students })
            RETURN p"""
        )
        result = tx.run(query, project_name=project_name, nr_students=nr_students)
        try:
            return [{"p": row["p"]["name"], "n": row["p"]["nr_students"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def add_student_to_project(self, project_name, student_fname, student_lname):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._add_student_to_project_and_return, project_name, student_fname, student_lname)
        return result

    @staticmethod
    def _add_student_to_project_and_return(tx, project_name, student_fname, student_lname):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            """MERGE (s:Student {fname: $student_fname, lname: $student_lname})
            with s MATCH (p:Project {name: $project_name})
            MERGE (s)-[:WORKS_ON]->(p) return s, p"""
        )
        result = tx.run(query, project_name=project_name, student_fname=student_fname, student_lname=student_lname)
        try:
            return [{"p": row["p"]["name"], "sf": row["s"]["fname"], "sl": row["s"]["lname"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
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
        return [{"p": row["p"]["name"], "s": row["s"]["fname"] + " " + row["s"]["lname"]} for row in result]

if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+s://ffceff21.databases.neo4j.io"
    user = "neo4j"
    password = "s3M3B0rzrxJCZtEr181zpzyzK8jkWNajVkXgcAuCebw"
    app = App(uri, user, password)
    app.create_friendship("Alice", "David")
    app.find_person("Alice")
    app.close()