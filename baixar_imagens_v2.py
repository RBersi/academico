#!/usr/bin/env python3
import os
import requests
import time  # Para adicionar pausa entre os downloads
import signal  # Para capturar Ctrl+C
import sys  # Para encerrar o programa

# Variável global para controlar a execução
executando = True

def signal_handler(sig, frame):
    """
    Manipulador de sinal para capturar Ctrl+C.
    """
    global executando
    print("\nPrograma interrompido pelo usuário.")
    executando = False
    sys.exit(0)

# Configura o manipulador de sinal para capturar Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Pasta onde as imagens serão salvas
output_folder = "imagens_baixadas"

# Cria a pasta se ela não existir
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Solicita ao usuário o caminho completo do arquivo de links
arquivo_links = input("Digite o caminho completo do arquivo contendo os links: ").strip()

# Verifica se o arquivo existe
if not os.path.isfile(arquivo_links):
    print(f"Erro: O arquivo '{arquivo_links}' não foi encontrado.")
    exit(1)

# Lê os links do arquivo fornecido pelo usuário
try:
    with open(arquivo_links, "r") as file:
        links = file.readlines()
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
    exit(1)

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
                    if not executando:
                        break  # Sai do loop se o programa foi interrompido
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
    if not executando:
        break  # Encerra o loop se o programa foi interrompido
    print(f"Baixando imagem {i}/{len(links)}: {link}")
    download_image(link, output_folder)
    # Pausa entre os downloads
    time.sleep(intervalo_entre_downloads)

print("Download concluído!")
