## Auntie Ivy
An AI peer-based conversational pedagogical agent that is designed for older adults to learn about deepfakes. 🧓

### Topics
The conversational flows of Auntie Ivy span 3 topics.

1. How are deepfakes created?
2. How to spot deepfakes?
3. What are the benefits and harms of deepfakes?


### Characteristics
Auntie Ivy takes on the persona of a peer older adult who is learning alongside the learner. It has the following characteristics:

| Aspect          | Description                                                                                                                                               |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Knowledge       | Has limited knowledge, which may include inaccuracies or gaps.                                                                                            |
| Engagement      | A blend of reactive and proactive, responding to the learner while also taking initiative to guide the conversation.                                      |
| Problem-Solving | Able to offer direct answers for simple factual questions that it knows the answers to, but engages in discussions for more subjective or complex topics. |


### Tech Stack
Auntie Ivy is a Telegram bot developed using Python and PostgresSQL. It uses OpenAI API for text and audio generation functionalities.

At the moment, it supports text input/ouput, as well as audio input/output.


### How to Set Up
1. Clone the project to a local directory of your preference.

```
git clone https://github.com/eugenetangkj/auntie-ivy.git
```

2. Change directory to the root directory of the Auntie Ivy project.
```
cd auntie-ivy
```

3. Download the Python packages required for the project as stated in [`requirements.txt`](requirements.txt)

```
pip install -r requirements.txt
```

4. Create a local PostgreSQL database.

- Download [PostgreSQL](https://www.postgresql.org/download/) which is a relational database system.
- I recommend also downloading [pgAdmin](https://www.pgadmin.org/download/), a GUI tool that allows you to manage your PostgreSQL databases. 
- Create a PostgreSQL database via pgAdmin after following the above 2 pointers.

> [!NOTE]
> If you are using Windows, ensure that the bin folder of PostgreSQL is added to your PATH variable.

> [!TIP]
> You can refer to the [Windows tutorial](https://www.youtube.com/watch?v=v1d2Fa9FPOQ) and [macOS tutorial](https://www.youtube.com/watch?v=fy-42clnbmc) if required.


5. Create four tables in the PostgreSQL database that you had created in Step 4 above. To do so, in your selected database, run the [`create_tables.sql`](/sql_files/create_tables.sql) file using the query tool in pgAdmin.


6. In the root directory, create a new `.env` file.
- To obtain the Telegram API token, create a bot using BotFather. A simple tutorial can be found [here](https://medium.com/@Elhazin/creating-a-telegram-bot-55e6ca4e337d).
- Obtain the OpenAI API key from the [API key page](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key).
- The database environment variables should correspond to the information that you used in Steps 4 and 5 above. 

```
TELEGRAM_TOKEN=<Your Telegram API token>
OPENAI_API_KEY=<Your OpenAI API key>
DB_HOST='localhost'
DB_NAME=<Your database name> # The database name chose in Step 4 above
DB_USER=<Your database username> #Default is postgres
DB_PASSWORD=<Your database password>
```

7. Download [FFmpeg](https://www.ffmpeg.org/download.html), a cross-platform multimedia tool that allows you to work with multimedia files of various formats.

> [!NOTE]
> If you are using Windows, ensure that the bin folder of FFmpeg is added to your PATH variable.

8. To run the bot, execute the following command in the root directory.
```
python bot.py
```

9. After running the command in Step 8, head to Telegram and start interacting with your bot.

### Interactions
Currently, there are 2 supported ways for you to interact with Auntie Ivy.
1. Text message
2. Voice message

> [!NOTE]
> Please ensure that you send **1 message** at a time. After sending 1 message, wait for the bot's reply before sending another message. This is because simultaneous handling of multiple messages is not supported at the moment.

> [!WARNING]
> Sending a voice message incurs OpenAI credits. Do use with discretion.


### Commands
There are several built-in commands for the bot.

#### `/start` Command
This initialises the conversation and creates an entry for the user in the `users` table if the user does not yet exist.

#### `/delete` Command
This deletes the current user in the `users` table and all of the user's conversation history in the `conversation_history` table. Use this command to effectively reset your conversation with the bot.

```
# To reset your conversation with the bot, run these 2 commands in the bot
/delete
/start
```

> [!CAUTION]
> The `/delete` command clears all of your conversation history with the bot. Only use it if you are sure that you want to reset your interactions with the bot.

#### `/audio` Command
This toggles the audio mode of the bot.
- If the audio mode is enabled, the bot will reply using voice messages.
- If the audio mode is disabled, the bot will reply using text messages.

> [!NOTE]
> Some messages in the conversational flow will always be produced through text messages, regardless of whether the audio mode is enabled or not. This is deliberate by design, as some content is better rendered as text.

> [!WARNING]
> The audio mode uses OpenAI credits. Do use with discretion.

#### `/topic` Command
This allows you to navigate between the three topics supported by Auntie Ivy. The syntax is `/topic <topic_num>`.
```
# To change to Topic 1, run this in the bot
/topic 1

# To change to Topic 2, run this in the bot
/topic 2

# To change to Topic 3, run this in the bot
/topic 3
```