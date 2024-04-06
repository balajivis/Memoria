from memory.base_memory import BaseMemory
import sqlite3
import json
import dill


class ProceduralMemory(BaseMemory):
    def __init__(self):
        self.conn = sqlite3.connect("/tmp/mem.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS tools(name, function BLOB, description, parameters)"
        )
        self.functions = []

        # add example methods
        self.store(
            (
                "add_two",
                lambda x: x + 2,
                "adds the current weather by 2",
                [("x", "integer", "variable to add to")],
            )
        )

    def store(self, kv):
        """
        name: str
        function: python def
        description: str
        parameters: (listof (name: str, type: str, description: str))
        """
        name, function, description, parameters = kv
        # self.functions((name, function, description, parameters))

        self.cur.execute(
            """
            INSERT INTO tools VALUES (?, ?, ?, ?)
        """,
            (name, dill.dumps(function), description, json.dumps(parameters)),
        )

    def retrieve(self, obj):
        tools = self.cur.execute("SELECT * FROM tools")
        formatted_tools = []
        for tool in tools:
            name, function, description, parameters = tool
            parameters = json.loads(parameters)
            function = dill.loads(function)

            formatted_tools.append(
                {
                    "name": name,
                    "description": description,
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            param[0]: {"type": param[1],
                                       "description": param[2]}
                            for param in parameters
                        },
                        "required": [param[0] for param in parameters]
                    },
                }
            )

        return formatted_tools


mem = ProceduralMemory()

assert mem.retrieve("")[0]["name"] == "add_two"
