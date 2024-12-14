from langgraph.agent import LangGraphAgent
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from newsapi import NewsApiClient
from utils.email_util import send_email
from config.settings import NEWS_API_KEY

# Configurar NewsAPI
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Configurar el prompt para limpiar noticias
news_prompt = PromptTemplate(
    input_variables=["raw_news"],
    template="Reescribe y organiza la siguiente información como una noticia clara y concisa: {raw_news}"
)
llm_chain = LLMChain(prompt=news_prompt)

class NewsAgent(LangGraphAgent):
    def search_news(self, topic):
        """Busca noticias relacionadas con el tema usando NewsAPI."""
        articles = newsapi.get_everything(q=topic, language="en", sort_by="relevancy", page_size=5)
        results = []
        for article in articles["articles"]:
            results.append({
                "title": article["title"],
                "description": article["description"],
                "source": article["source"]["name"],
                "url": article["url"]
            })
        return results

    def clean_and_summarize_news(self, news):
        """Limpia y redacta las noticias con LangChain."""
        raw_news = "\n".join(
            [f"Título: {item['title']}\nDescripción: {item['description']}\nFuente: {item['source']}\nURL: {item['url']}" for item in news]
        )
        summarized_news = llm_chain.run(raw_news)
        return summarized_news

    def send_email(self, email, topic, summarized_news):
        """Envía el correo electrónico con las noticias."""
        send_email(email, f"Noticias recientes sobre {topic}", summarized_news)
