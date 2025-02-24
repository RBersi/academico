#!/usr/bin/env python3

import os
import requests
import time  # Para adicionar pausa entre os downloads

# Pasta onde as imagens serão salvas
output_folder = "imagens_baixadas"

# Cria a pasta se ela não existir
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Lê os links do arquivo
with open("links.txt", "r") as file:
    links = file.readlines()

# Remove espaços em branco e quebras de linha
links = [link.strip() for link in links if link.strip()]

# Função para baixar uma imagem
def download_image(url, folder):
    try:
        # Faz a requisição para baixar a imagem
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Extrai o nome do arquivo da URL
            filename = os.path.join(folder, url.split("/")[-1])
            # Salva a imagem no disco
            with open(filename, 'wb') as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            print(f"Imagem salva: {filename}")
        else:
            print(f"Falha ao baixar: {url} (Status Code: {response.status_code})")
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

# Intervalo de tempo entre os downloads (em segundos)
intervalo_entre_downloads = 1  # Altere conforme necessário (ex.: 0.5 para 0.5 segundos)

# Itera sobre os links e baixa cada imagem
for i, link in enumerate(links, start=1):
    print(f"Baixando imagem {i}/{len(links)}: {link}")
    download_image(link, output_folder)

    # Pausa entre os downloads
    time.sleep(intervalo_entre_downloads)

print("Download concluído!")
