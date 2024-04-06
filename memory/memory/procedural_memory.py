from memory.base_memory import BaseMemory
import sqlite3
import json
import dill


class ProceduralMemory(BaseMemory):
    def __init__(self, db_path="/tmp/mem.db"):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS tools(name TEXT PRIMARY KEY, function BLOB, description TEXT, parameters TEXT)"
        )
        self.conn.commit()

        # Example method to be stored
        self.store(
            "add_two",
            lambda x: x + 2,
            "Adds 2 to the given number",
            [("x", "integer", "Number to add to")]
        )

    def store(self, name, function, description, parameters):
        """
        Stores a tool in the procedural memory.

        :param name: str - Name of the function
        :param function: callable - Python function object
        :param description: str - Description of what the function does
        :param parameters: list of tuples - Parameters the function takes
        """
        self.cur.execute(
            """
            INSERT INTO tools (name, function, description, parameters) VALUES (?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
            function = excluded.function,
            description = excluded.description,
            parameters = excluded.parameters
            """,
            (name, dill.dumps(function), description, json.dumps(parameters)),
        )
        self.conn.commit()

    def retrieve(self, name):
        """
        Retrieves a tool from the procedural memory.

        :param name: str - Name of the function to retrieve
        :return: dict - Tool data including name, description, and input schema
        """
        tool = self.cur.execute(
            "SELECT * FROM tools WHERE name = ?", (name,)).fetchone()
        if tool:
            name, function, description, parameters = tool
            parameters = json.loads(parameters)
            function = dill.loads(function)

            return {
                "name": name,
                "description": description,
                "function": function,
                "input_schema": {
                    "type": "object",
                    "properties": {
                        param[0]: {"type": param[1], "description": param[2]}
                        for param in parameters
                    },
                    "required": [param[0] for param in parameters]
                },
            }
        return None


# Example usage:
if __name__ == "__main__":
    mem = ProceduralMemory()
    tool = mem.retrieve("add_two")
    assert tool["name"] == "add_two"
    # Should output 12 after adding 2 to 10
    print(f"Function 'add_two': {tool}")
