from memory.base_memory import BaseMemory
import sqlite3


class ProceduralMemory(BaseMemory):
    def __init__(self, db_path="relational.db"):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS procedures(name TEXT PRIMARY KEY, instructions TEXT)"
        )
        self.conn.commit()

        # Example procedure to be stored
        self.store(
            "add_two",
            "To add two to a number, simply increment the number by 2."
        )

    def store(self, name, instructions):
        """
        Stores a procedure in the procedural memory.

        :param name: str - Name of the procedure
        :param instructions: str - Instructions of the procedure as a string
        """
        self.cur.execute(
            """
            INSERT INTO procedures (name, instructions) VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET
            instructions = excluded.instructions
            """,
            (name, instructions),
        )
        self.conn.commit()

    def retrieve(self, name):
        """
        Retrieves a procedure from the procedural memory.

        :param name: str - Name of the procedure to retrieve
        :return: str - Instructions for the procedure
        """
        tool = self.cur.execute(
            "SELECT instructions FROM procedures WHERE name = ?", (name,)).fetchone()
        if tool:
            return tool[0]
        return None


# Example usage:
if __name__ == "__main__":
    mem = ProceduralMemory()
    instructions = mem.retrieve("add_two")
    assert instructions == "To add two to a number, simply increment the number by 2."
    print(f"Procedure 'add_two': {instructions}")
