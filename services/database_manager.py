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

    # Special case: If lower and upper bounds are the same, select only that exact topic-stage pair
    if (current_topic_lower_bound == current_topic_upper_bound) and (current_stage_lower_bound == current_stage_upper_bound):
        cursor.execute("""
        SELECT role, message 
        FROM conversation_history
        WHERE user_id = %s
          AND current_topic = %s
          AND current_stage = %s
        ORDER BY current_topic ASC, current_stage ASC
        """, (user_id, current_topic_lower_bound, current_stage_lower_bound))

    else:
        # General case: Select messages within the topic-stage range
        cursor.execute("""
        SELECT role, message 
        FROM conversation_history
        WHERE user_id = %s
          AND (
              (current_topic = %s AND current_stage >= %s)
              OR (current_topic > %s AND current_topic < %s)
              OR (current_topic = %s AND current_stage <= %s)
          )
        ORDER BY current_topic ASC, current_stage ASC
        """, (user_id, 
          current_topic_lower_bound, current_stage_lower_bound,
          current_topic_lower_bound, current_topic_upper_bound,
          current_topic_upper_bound, current_stage_upper_bound)
        )
    
    # Fetch all matching rows
    result = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    # Return output
    return result


'''
Retrieves the latest message in the conversation history of the given user that falls within
the specified topics and stages (inclusive).

Parameters:
    - user_id: ID of the user whose conversation history is to be fetched
    - current_topic_lower_bound: Lower bound for topic to fetch from
    - current_stage_lower_bound: Lower bound for stage to fetch from
    - current_topic_upper_bound: Upper bound for topic to fetch from
    - current_stage_upper_bound: Upper bound for stage to fetch from

Returns:
    - The latest message

'''
def fetchLatestMessage(user_id, current_topic_lower_bound, current_stage_lower_bound, current_topic_upper_bound, current_stage_upper_bound):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL query to fetch the latest message based on the conditions
    cursor.execute("""
    SELECT message
    FROM conversation_history
    WHERE user_id = %s
      AND (
          (current_topic = %s AND current_stage >= %s) 
          OR (current_topic > %s AND current_stage < %s)
          OR (current_topic = %s AND current_stage <= %s)
      )
    ORDER BY datetime DESC
    LIMIT 1
    """, (user_id, 
          current_topic_lower_bound, current_stage_lower_bound,
          current_topic_lower_bound, current_stage_upper_bound,
          current_topic_upper_bound, current_stage_upper_bound)
    )
    
    # Fetch the latest message (only one row)
    result = cursor.fetchone()
    
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
    - topic: Topic associated with the knowledge
'''
def add_knowledge(user_id, knowledge_rows, topic):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the knowledge rows into the knowledge table
    for knowledge_row in knowledge_rows:
        cursor.execute(
            """
            INSERT INTO knowledge (user_id, fact, topic, date_updated)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, knowledge_row, topic, datetime.now())
        )
    
    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()


'''
Retrieves the current knowledge facts of the agent for a given topic

Parameters:
    - user_id: ID of the user
    - topic: Topic to be retrieved

Returns:
    - A list of knowledge facts that the agent currently has for the given topic

'''
def fetchKnowledge(user_id, topic):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute query to fetch all rows that match the given user_id
    cursor.execute("SELECT fact FROM knowledge WHERE user_id = %s AND topic = %s", (user_id, topic,))
    
    # Fetch all matching rows
    rows = cursor.fetchall()
    
    # Extract just the 'fact' column from each row and return it as a list
    facts = [row[0] for row in rows]
    
    # Close the connection
    conn.close()
    
    # Return the facts list
    return facts


'''
Retrieves the current knowledge facts of the agent, along with the IDs of the knowledge facts.

Parameters:
    - user_id: ID of the user
    - topic: Topic associated with the knowledge

Returns:
    - A list of tuples. Each tuple is (id, knowledge_fact)

'''
def fetchKnowledgeWithId(user_id, topic):
    try:
        # Connect to the database using a context manager
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Execute query to fetch both id and fact columns
                cursor.execute("SELECT id, fact FROM knowledge WHERE user_id = %s AND topic = %s", (user_id, topic))
                rows = cursor.fetchall()
                
                # Extract (id, fact) tuples into a list
                facts = [(row[0], row[1]) for row in rows]
        return facts
    except Exception as e:
        print(f"Error fetching knowledge: {e}")
        return []


'''
Retrieves a given knowledge fact.

Parameters:
    - user_id: ID of the user
    - fact_id: ID of the fact to fetch

Returns:
    - The given knowledge fact

'''
def fetchKnowledgeFactUsingId(user_id, fact_id):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute query to fetch the fact that matches the given user_id and fact_id
    cursor.execute("SELECT fact FROM knowledge WHERE user_id = %s AND id = %s", (user_id, fact_id))
    
    # Fetch the matching row
    row = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    # Return the fact if found, else None
    return row[0] if row else None


'''
Updates a given knowledge fact.

Parameters:
    - user_id: ID of the user
    - fact_id: ID of the knowledge fact in the knowledge table which is to be updated
    - new_fact: New fact that is to be used
'''
def updateKnowledgeFactUsingId(user_id, fact_id, new_fact):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update the fact field in the knowledge table with the new fact, and the date updated to the the current datetime
    cursor.execute("""
    UPDATE knowledge
    SET fact = %s, date_updated = CURRENT_TIMESTAMP
    WHERE user_id = %s AND id = %s
    """, (new_fact, user_id, fact_id))

    # Commit the transaction to save changes
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()


'''
Add a contradicting fact

Parameters:
    - user_id: ID of the user in the users table
    - fact_id: ID of the contradicting fact in the facts table

Returns:
    - No return value
'''
def add_contradicting_fact(user_id, fact_id):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Add the contradicting fact
    cursor.execute("""
    INSERT INTO contradicting_facts (user_id, fact_id)
    VALUES (%s, %s)
    """, (user_id, fact_id))

    # Commit the transaction to make sure the insert is saved in the database
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()


'''
Retrieve the ID of the contradicting fact for a given user

Parameters:
    - user_id: ID of the user in the users table

Returns:
    - The id of the contradicting fact
'''
def retrieve_id_of_contradicting_fact(user_id):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch ID of the contradicting fact from the contradicting facts table
    cursor.execute("""
    SELECT fact_id 
    FROM contradicting_facts 
    WHERE user_id = %s
    """, (user_id,))

    # Fetch the result
    result = cursor.fetchone()

    # Close the connection
    cursor.close()
    conn.close()

    # If no contradicting fact is found, return None
    if result:
        return result[0]
    else:
        return None


'''
Removes the contradicting fact for a given user

Parameters:
    - user_id: ID of the user in the users table

Returns:
    - No return value
'''
def remove_contradicting_facts_for_user(user_id):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Remove all contradicting facts associated with the user
    cursor.execute("""
    DELETE FROM contradicting_facts
    WHERE user_id = %s
    """, (user_id,))

    # Commit the transaction
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()


'''
Updates the stance of the user.

Parameters:
    - user_id: ID of the user whose stance is to be updated
    - new_stance: New stance of the user

Returns:
    - No return value

'''
def updateUserStance(user_id, new_stance):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update the user's stage and substage
    cursor.execute(
        "UPDATE users SET stance = %s WHERE user_id = %s",
        (new_stance, user_id)
    )

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()


'''
Fetches the stance of the user

Parameters:
    - user_id: ID of the user whose stance is to be retrieved

Returns:
    - stance: Stance of the user     
'''
def fetchUserStance(user_id):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the user's stance based on their user_id
    cursor.execute(
        "SELECT stance FROM users WHERE user_id = %s",
        (user_id,)
    )

    # Fetch the result and return the user's stance
    stance = cursor.fetchone()

    # Close the connection
    conn.close()

    # Return the stance if found, otherwise return empty stance
    if stance:
        return stance[0]
    else:
        return ''

