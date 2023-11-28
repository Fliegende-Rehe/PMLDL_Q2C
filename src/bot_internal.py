import sqlite3

from ai import get_scenario_record, get_embedding, find_scenario_record, ChatState

DATABASE_FILENAME = 'database.db'
DATABASE_TABLENAME = 'Chats'


def db_connect(db_filename):
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {DATABASE_TABLENAME} (
    id BIGINT PRIMARY KEY,
    state INTEGER NOT NULL,
    branched_id INTEGER
    )
    ''')
    return connection, cursor


def get_record(id):
    connection, cursor = db_connect(DATABASE_FILENAME)
    cursor.execute(f"SELECT * FROM {DATABASE_TABLENAME} WHERE id=?", (id,))
    result = cursor.fetchone()
    connection.close()
    return result


def update_record(id, state, branched_id):
    conn, cursor = db_connect(DATABASE_FILENAME)
    current_state = get_record(id)
    if current_state is None:
        cursor.execute(f"INSERT INTO {DATABASE_TABLENAME} (id, state, branched_id) VALUES (?, ?, ?)",
                       (id, state.value, branched_id))
    else:
        cursor.execute(f"UPDATE {DATABASE_TABLENAME} SET id = ?, state = ?, branched_id = ?",
                       (id, state.value, branched_id))
    conn.commit()
    conn.close()


def process_prompt(bot, scenario, scenario_prompts, message):
    msg_emb = get_embedding(message.text)
    chat_id = message.chat.id
    db_record = get_record(chat_id)

    chat_id, state, branched_id = db_record[0], ChatState(
        db_record[1]), db_record[2]

    if state == ChatState.INITIAL:
        best_match = get_scenario_record(scenario_prompts, 'initial', msg_emb)
        id, phrase, type, emb, ind = best_match
        scenario_record = find_scenario_record(scenario, id)
        bot.reply_to(message, f'<Your prompt>: {phrase}')

        if 'action' in scenario_record:
            bot.reply_to(
                message, f'<Making an action>: {scenario_record["action"]}')
            update_record(chat_id, ChatState.INITIAL, None)
        elif 'nextPrompt' in scenario_record:
            nextPromptId = scenario_record['nextPrompt']
            branched_id = nextPromptId  # save this
            branched_record = find_scenario_record(scenario, branched_id)
            bot.reply_to(message, f'Please tell: {branched_record["label"]}')
            update_record(chat_id, ChatState.CHOOSE, branched_id)
    elif state == ChatState.CHOOSE:
        record = find_scenario_record(scenario, branched_id)
        best_match = get_scenario_record(
            scenario_prompts, 'choose', msg_emb, certain_id=record['id'])
        prompt_index = best_match[4]
        action = record['action'][prompt_index]
        bot.reply_to(message, f'<Your prompt>: {record["prompts"][prompt_index]}')
        bot.reply_to(message, f'<Making an action>: {action}')
        update_record(chat_id, ChatState.INITIAL, None)
    else:
        bot.reply_to(message, f'Sorry, something wrong happened.')
