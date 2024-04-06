import base64
from anthropic import Anthropic

client = Anthropic()
MODEL_NAME = "claude-3-opus-20240229"


def retrieve_values_for_tools(user_query):
    return f"""You are given a sentence that contains a property, and you should generate the values in the form of a list of 3 strings, where 

    - the first string is the property name, 
    - the second string is the type of the property (str, int) and 
    - the third string is a short 1-line description of what the property is.

    Here are a couple of examples that illustrate this:

    <example>
    Sentence: "I enjoy reading sci-fi genre books".
    The output: ['book_genre_interest','str','The genre of books the user enjoys.']
    </example>

    <example>
    Sentence: "My goal today is to ensure that I can get my bicep-workout done.
    The output: ['today_goal','str',"The user's goal for today"]
    </example>

    Now perform the same action here:

    Sentence: {user_query}
    Output:
    """


system_prompt = """
As an AI assistant, your task is to interact with the user and manage your memory effectively. To accomplish this, you have access to the MemoryManager class, which allows you to store and retrieve information in different types of memory: working memory, associative memory, long-term summary memory, and procedural memory.

Based on the user's input, you should determine which memory type to use, and whether to store or retrieve information. Here are the broad guidelines to follow:

1. If the user mentions their interests, hobbies, or preferences to you, store this information in associative memory using:
   memory_manager.store('associative', 'user_interests', 'summary_of_interests')

2. If the user's query requires knowledge about their interests, hobbies, or preferences, perform a retrieval into the associative memory using:
   memory_manager.retrieve('associative','user_query')
   
3. If the user provides a specific goal or task they want to accomplish, or information relevant to achieve the working goal, store it in working memory using:
   memory_manager.store('working', 'name_of_property', 'summary_of_information')

4. If the user's query requires context that references previous conversations, then query the long term memory to identify if there's relevant information available using:
    memory_manager.retrieve('longterm','summary_of_question')   

5. If the user shares a long-term plan or their objectives, store it in long-term summary memory using:
   memory_manager.store('longterm', 'name_of_property', 'summary_of_user_message')

6. If the user's query requires context that references previous conversations, then query the long term memory to identify if there's relevant information available using:
    memory_manager.retrieve('longterm','summary_of_question')

7. If the user provides step-by-step instructions or a procedure to follow, store it in procedural memory using:
   memory_manager.store('procedural', 'name_of_property', 'description_of_property')

8. If the user's goal requires you to take actions, then retrieve the tools you need to use through:
    memory_manager.retrieve('procedural','name_of_action')


Remember to use the information stored in memory to provide context-aware responses and assist the user effectively. If the user's input doesn't fit into any specific memory category, use your best judgment to determine if and where to store or retrieve the information.

Analyze their input and manage your memory accordingly to provide the best possible assistance.
"""


def claude_response(query):
    response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=2048,
    messages=[{'role':'user','content':retrieve_values_for_tools(query)}],
    )
    return response.content[0].text


tools = [
    {
        "name": 'memory_manager.store',
        'description': 'Store relevant context into memory',
        'input_schema': {
            "type": 'object',
            'properties': {
                'memory_type': {
                    'type': 'string',
                    'enum': ['procedural','longterm','working','associative'],
                    'description': 'The type of memory we want to store into'
                },
                claude_response[0]: {
                    'type': claude_response[1],
                    'description':claude_response[2],
                },
                user_query: {
                    'type':'str',
                    'description': 'Query of the user'
                }
                }
            },
            'required':['memory_type',claude_response[0],user_query],
        },

    {
        "name": 'memory_manager.store',
        'description': 'Store relevant context into memory',
        'input_schema': {
            "type": 'object',
            'properties': {
                'memory_type': {
                    'type': 'string',
                    'enum': ['procedural','longterm','working','associative'],
                    'description': 'The type of memory we want to store into'
                },
                claude_response[0]: {
                    'type': claude_response[1],
                    'description':claude_response[2],
                },
                }
            },
            'required':['memory_type',claude_response[0]],
        },
]