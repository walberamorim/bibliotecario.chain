from inicializar_modelo import *
from processar_artigos import *

import json
import os

NOME_ROBO = "Akhenaton"

CONVERSAS = [
    "C:\\Users\\WAA-HP\\Documents\\posweb\\bibliotecario.chain\\conversas\\saudacoes.json",
    "C:\\Users\\WAA-HP\\Documents\\posweb\\bibliotecario.chain\\conversas\\informacoes_basicas.json"
]

def carregar_conversas():
    conversas = []

    for arquivo_conversas in CONVERSAS:
        with open(arquivo_conversas, "r", encoding="utf-8") as arquivo:
            lista_conversas = json.load(arquivo)
            conversas.append(lista_conversas["conversas"])

            arquivo.close()

    return conversas

def get_pares_mensagem_resposta(conversas):
    pares = []

    for conversa in conversas:
        for mensagens_resposta in conversa:
            mensagens = mensagens_resposta["mensagens"]
            resposta = mensagens_resposta["resposta"]

            for mensagem in mensagens:
                pares.append((mensagem, resposta))

    return pares

def get_pares_artigo_tokens():
    pares = []

    for contador in range(1, MAXIMO_ARTIGOS):
        caminho_artigo = f"{CAMINHO_ARTIGOS}\\{contador}.tex"

        if os.path.exists(caminho_artigo):
            sucesso, conteudo = ler_conteudo(caminho_artigo)

            if sucesso:
                titulo = extrair_titulo(conteudo)
                resumo = extrair_resumo(conteudo)

                tokens = word_tokenize(resumo.lower())
                tokens = eliminar_marcacoes_latex(tokens)

                pares.append((titulo, tokens))
        else:
            break

    return pares

def get_prompt(pares_mensagem_resposta, pares_artigo_tokens):
    prompt = []

    prompt.append(("system", f"Você é um bibliotecário chamado '{NOME_ROBO}'"))
    prompt.append(("system", "vousé deve fonecer suporte a usuários de uma biblioteca de uma instituição de ensino"))

    for mensagem, resposta in pares_mensagem_resposta:
        prompt.append(("system", f"Caso os usuários falem ou perguntem '{mensagem}' ou algo parecido com isso, sua resposta deve ser '{resposta}'"))
    
    for artigo, tokens in pares_artigo_tokens:
        prompt.append(("system", f"Considere que existe um artigo cujo título é '{artigo}' e que possui esta lista de tokens significativos: '{tokens}'"))
    
    prompt.append(("system", "Você deve extrair da lista de tokens dos artigos as palavras-chave mais significativas, que são aquelas relacionadas com tecnologia da informação."))
    prompt.append(("system", "Você deve realizar uma filtragem de artigos por palavras-chave sempre que o usuario informar que deseja pesquisar por artigos. A sua resposta, neste caso, deve ser 'Informe as palavras-chave desejadas' ou alguma variação"))
    prompt.append(("system", "Caso o usuário envie alguma mensagem ou pergunta além destas configuradas, você deve informar que não tem como responder e que ele deve procurar informações no site oficial da biblioteca"))
    prompt.append(("system", "Ao apresentar o resultado da pesquisa, você deve apresentar apenas a lista de artigos encontrados e um contador de quantos artigos foram encontrados"))
    prompt.append(("system", "O usuario poderá informar as palavras-chave separadas por vírgula ou espaço."))
    prompt.append(("human", "{pergunta}"))
    return prompt

if __name__ == "__main__":

    pares_mensagem_resposta = get_pares_mensagem_resposta(carregar_conversas())
    pares_artigo_tokens = get_pares_artigo_tokens()

    iniciada, IA = iniciar_IA(get_prompt(pares_mensagem_resposta, pares_artigo_tokens))
    if iniciada:
        print("acesso à IA iniciado, atendendo usuários...")
        while True:
            pergunta = input("👤: ")

            sucesso, resposta = obter_resposta(IA, {"pergunta": pergunta})
            if sucesso:
                print(f"🤖: {resposta.content}")
            else:
                print(f"🤖: Estou tendo problemas para realizar o processamento de sua mensagem neste momento. Tente novamente mais tarde")