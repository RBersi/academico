#!/usr/bin/env python3

import re

# Caminho para o arquivo de entrada (contendo os códigos da página web)
arquivo_entrada = "pagina_web.txt"

# Caminho para o arquivo de saída (onde os links filtrados serão salvos)
arquivo_saida = "links_filtrados.txt"

# Expressão regular para encontrar links que terminam com .jpg
padrao_jpg = r'https?://[^\s"\']+\.jpg'

# Lista para armazenar os links encontrados
links_jpg = []

# Lê o arquivo de entrada
try:
    with open(arquivo_entrada, "r", encoding="utf-8") as file:
        conteudo = file.read()

    # Encontra todos os links que correspondem ao padrão
    links_jpg = re.findall(padrao_jpg, conteudo)

    # Salva os links filtrados no arquivo de saída
    with open(arquivo_saida, "w", encoding="utf-8") as output_file:
        for link in links_jpg:
            output_file.write(link + "\n")

    print(f"{len(links_jpg)} links .jpg foram encontrados e salvos em '{arquivo_saida}'.")

except FileNotFoundError:
    print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
