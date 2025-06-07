from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

import os

API_KEY = "C:\\Users\\WAA-HP\\Documents\\posweb\\bibliotecario.chain\\genai.key"
# MODELO = "gemini-2.0-flash-001"
MODELO = "gemini-2.5-flash-preview-04-17"

def iniciar_IA(prompt):
    iniciada, IA = False, None
    
    try:
        with open(API_KEY, "r") as chave_openai:
            chave = chave_openai.read()
            os.environ["GOOGLE_API_KEY"] = chave

            chave_openai.close()

        llm = ChatGoogleGenerativeAI(model=MODELO, temperature=0, max_tokens=None, timeout=None, max_retries=4)
        IA = ChatPromptTemplate.from_messages(prompt) | llm

        iniciada = True
    except Exception as e:
        print(f"ocorreu um erro iniciando acesso a Google Gemini: {str(e)}")
    
    return iniciada, IA


def obter_resposta(IA, parametros):
    sucesso, resposta = False, None
    
    try:
        resposta = IA.invoke(parametros)

        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro testando o prompt: {str(e)}")

    return sucesso, resposta

if __name__ == "__main__":
    prompt = [
        ("system", "Você é um assistente capaz de traduzir do português para o inglês."),
        ("system", "Traduza a sentença do usuário. A resposta tem que ser direta, sem qualquer enunciado ou comentário."),
        ("human", "{sentencas}"),
    ]
    iniciada, IA = iniciar_IA(prompt)
    if iniciada:
        print("acesso à IA iniciado, iniciando o chat...")

        sucesso, resposta = obter_resposta(IA, {"sentencas": "Estou com fome, quero almoçar."})
        if sucesso:
            print(f"Resposta: {resposta.content}") 
