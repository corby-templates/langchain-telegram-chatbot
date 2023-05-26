from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import asyncio, os

# Load environment variables
load_dotenv()

def main():
    llm = OpenAI(temperature=0)
    tools = load_tools([])
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent = initialize_agent(tools, llm, agent="conversational-react-description", memory=memory, verbose=False)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        response = agent.run(update.message.text)
        await update.message.reply_text(response)

    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    #application.add_handler(CommandHandler("start", start))
    #application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("[+] Telegram bot listening...")

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()