from chainlit import user_session
from agents.news_agent import NewsAgent
from copilotkit import CopilotKit

# Inicializar el agente
agent = NewsAgent()

# Configuración de Chainlit
@chainlit.app
async def app():
    user_topic = user_session.get("topic")
    user_email = user_session.get("email")

    if not user_topic or not user_email:
        await chainlit.send_message("Por favor, proporciona un tema y un correo electrónico.")
        return

    # Buscar noticias
    news = agent.search_news(user_topic)

    if not news:
        await chainlit.send_message(f"No se encontraron noticias sobre el tema: {user_topic}")
        return

    # Limpiar y redactar las noticias
    summarized_news = agent.clean_and_summarize_news(news)

    # Enviar correo electrónico con noticias
    agent.send_email(user_email, user_topic, summarized_news)

    # Confirmación al usuario
    await chainlit.send_message(f"Las noticias sobre '{user_topic}' fueron redactadas y enviadas a {user_email}.")

# Uso de CopilotKit para extender funcionalidades
copilot = CopilotKit(agent=agent)
copilot.run()

# Iniciar Chainlit
if __name__ == "__main__":
    chainlit.run()
