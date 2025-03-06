import os
from dotenv import load_dotenv
import psycopg2
from definitions.role import Role
from datetime import datetime

"""
Environment variables for connecting to the Postgres database
"""
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


"""
Sets up the connection to the Postgres database
"""
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


'''
Determines the current topic and stage that the user is in by reading from the database

Parameters:
    - user_id: The user id of the user, obtained from Telegram API

Returns:
    - current_topic: Current topic selected by the user
    - current_stage: Current stage in the topic that the user is in
'''
def determineUserTopicAndStage(user_id):
    # Connect to the database
    conn = get_db_connection()

    # Search the users table using user_id and retrieve current topic and current stage
    cursor = conn.cursor()
    cursor.execute("SELECT current_topic, current_stage FROM users WHERE user_id = %s", (user_id,))

    # Fetch the result which is a tuple with 2 values corresponding to current stage and substage
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Check if current topic and current stage exists
    if result:
        current_topic, current_stage = result
        return current_topic, current_stage
    else:
        return None


'''
Determines the current topic that the user is in.

Parameters:
    - user_id: The user id of the user, obtained from Telegram API

Returns:
    - current_topic: Current topic that the user is in
'''
def determineUserTopic(user_id):
    # Connect to the database
    conn = get_db_connection()

    # Search the users table using user_id and retrieve current topic
    cursor = conn.cursor()
    cursor.execute("SELECT current_topic FROM users WHERE user_id = %s", (user_id,))

    # Fetch the result which is a tuple with 1 values corresponding to current topic
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Check if current topic exists
    if result:
        current_topic = result
        return current_topic
    else:
        return None


'''
Checks whether the user exists in the users table of the database

Parameters:
    user_id: The user id of the user, obtained from Telegram API

Returns:
    True if the user is found in the users table
    False if the user is not found in the users table
'''
def check_if_user_exist(user_id):
    # Connect to the database
    conn = get_db_connection()

    # Search the users table using user id
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()

    # Return output
    return result is not None


'''
Adds the current user into the users table of the database

Parameters:
    user_id: The user id of the user, obtained from Telegram API

Returns:
    No return value
'''
def add_user(user_id):
    # Connect to the database
    conn = get_db_connection()

    # Check if the user already exists in the users table before trying to add
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    # Only add the user if the user does not exist in the users table
    if not result:
        cursor.execute(
            "INSERT INTO users (user_id) VALUES (%s)",
            (user_id,)
        )
        conn.commit()

    # Close the connection
    conn.close()


'''
Deletes the current user from the users table of the database

Parameters:
    user_id: The user id of the user, obtained from Telegram API

Returns:
    No return value
'''
def delete_user(user_id):
    # Connect to the database
    conn = get_db_connection()

    # Check if the user  exists in the users table before trying to delete
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    # Only delete the user if the user exists in the users table
    if result:
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()

    # Close the connection
    conn.close()


'''
Updates the topic and stage of the given user.

Parameters:
    - user_id: ID of the user whose topic and stage are to be updated
    - new_topic: New topic of the user
    - new_stage: New stage of the user

Returns:
    - No return value

'''
def updateUserTopicAndStage(user_id, new_topic, new_stage):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update the user's stage and substage
    cursor.execute(
        "UPDATE users SET current_topic = %s, current_stage = %s WHERE user_id = %s",
        (new_topic, new_stage, user_id)
    )

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()


'''
Saves a message to the conversation history of the given user

Parameters:
    - user_id : ID of the user to which the message belongs to
    - role: Role of the user, either 'user' or 'system'
    - message: The message to be saved
    - current_topic: Topic in which the message is sent
    - current_stage: Stage in which the message is sent

Returns:
    - No return value
'''
def saveMessageToConversationHistory(user_id, role: Role, message, current_topic, current_stage):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the current datetime
    timestamp = datetime.now()

    # Insert the message into the conversation_history table
    cursor.execute(
        """
        INSERT INTO conversation_history (user_id, role, message, current_topic, current_stage, datetime)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user_id, role.value, message, current_topic, current_stage, timestamp)
    )
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()


'''
Retrieves the conversation history of the given user that falls within
the specified topics and stages (inclusive) sorted in oldest to newest.

Parameters:
    - user_id: ID of the user whose conversation history is to be fetched
    - current_topic_lower_bound: Lower bound for topic to fetch from
    - current_stage_lower_bound: Lower bound for stage to fetch from
    - current_topic_upper_bound: Upper bound for topic to fetch from
    - current_stage_upper_bound: Upper bound for stage to fetch from

Returns:
    - A list of messages in the form of (role, message)

'''
def fetchConversationHistory(user_id, current_topic_lower_bound, current_stage_lower_bound, current_topic_upper_bound, current_stage_upper_bound):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL query to fetch conversation history based on the conditions
    cursor.execute("""
    SELECT role, message 
    FROM conversation_history
    WHERE user_id = %s
      AND (
          (current_topic = %s AND current_stage >= %s) 
          OR (current_topic > %s AND current_stage < %s)
          OR (current_topic = %s AND current_stage <= %s)
      )
    ORDER BY datetime ASC
    """, (user_id, 
      current_topic_lower_bound, current_stage_lower_bound,
      current_topic_lower_bound, current_stage_upper_bound,
      current_topic_upper_bound, current_stage_upper_bound)
    )
    
    # Fetch all matching rows
    result = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    # Return output
    return result


'''
Determines if the user has enabled audio mode or not. If the user turns on the audio mode,
it means that the user wants the bot to reply via a voice message instead of a text message.

Parameters:
    - user_id: ID of the user

Return:
    - did_user_enable_audio: A boolean indicating whether the user has enabled audio mode
'''
def determine_is_audio_enabled(user_id):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve the value from the database
    cursor.execute("""
        SELECT is_audio_enabled
        FROM users
        WHERE user_id = %s
    """, (user_id,))

    # Fetch one row since user_id should be unique
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Return the boolean value or None if no result is found
    return result[0] if result else None


'''
Sets the value of is_audio_enabled for the given user in the users table.

Parameters:
    - user_id: ID of the user
    - is_audio_enabled_value_to_use: Value to set for the is_audio_enabled field

'''
def set_is_audio_enabled(user_id, is_audio_enabled_value_to_use):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update the database
    cursor.execute("""
        UPDATE users
        SET is_audio_enabled = %s
        WHERE user_id = %s
    """, (is_audio_enabled_value_to_use, user_id))

   
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()


'''
Add a list of knowledge rows into the knowledge table

Parameters:
    - user_id: ID of the user
    - knowledge_rows: List of knowledge to be added
'''
def add_knowledge(user_id, knowledge_rows):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the knowledge rows into the knowledge table
    for knowledge_row in knowledge_rows:
        cursor.execute(
            """
            INSERT INTO knowledge (user_id, fact, date_updated)
            VALUES (%s, %s, %s)
            """,
            (user_id, knowledge_row, datetime.now())
        )
    
    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()


'''
Retrieves the current knowledge facts of the agent.

Parameters:
    - user_id: ID of the user

Returns:
    - A list of knowledge facts that the agent currently has

'''
def fetchKnowledge(user_id):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute query to fetch all rows that match the given user_id
    cursor.execute("SELECT fact FROM knowledge WHERE user_id = %s", (user_id,))
    
    # Fetch all matching rows
    rows = cursor.fetchall()
    
    # Extract just the 'fact' column from each row and return it as a list
    facts = [row[0] for row in rows]
    
    # Close the connection
    conn.close()
    
    # Return the facts list
    return facts