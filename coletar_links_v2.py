#!/usr/bin/env python3
import signal
import sys
from bs4 import BeautifulSoup
import requests

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

def coletar_links(url, filtrar_externos=False, filtrar_imagens=False):
    """
    Coleta todos os links de um documento HTML.
    
    Parâmetros:
        url (str): URL do documento HTML.
        filtrar_externos (bool): Se True, filtra apenas links externos.
        filtrar_imagens (bool): Se True, filtra apenas links de imagens.
        
    Retorna:
        list: Lista de links coletados.
    """
    try:
        # Faz a requisição HTTP para obter o conteúdo da página
        response = requests.get(url)
        response.raise_for_status()  # Lança exceção para erros HTTP
        
        # Analisa o conteúdo HTML usando BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extrai todos os links <a href="..."> e links de imagens <img src="...">
        links = []
        for tag in soup.find_all(['a', 'img']):
            if not executando:
                break  # Sai do loop se o programa foi interrompido
            
            if tag.name == 'a' and 'href' in tag.attrs:
                link = tag['href']
                if not filtrar_imagens and not filtrar_externos:
                    links.append(link)
                elif filtrar_externos and ('http' in link or 'https' in link):
                    links.append(link)
            elif tag.name == 'img' and 'src' in tag.attrs:
                if filtrar_imagens:
                    links.append(tag['src'])
        
        return links
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return []

# Exemplo de uso
if __name__ == "__main__":
    # Configura o manipulador de sinal para capturar Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    url = input("Digite a URL do documento: ")
    opcao = input("Deseja filtrar links externos? (s/n): ").lower()
    filtrar_externos = opcao == 's'
    
    opcao = input("Deseja filtrar links de imagens? (s/n): ").lower()
    filtrar_imagens = opcao == 's'
    
    links = coletar_links(url, filtrar_externos, filtrar_imagens)
    
    if links:
        print("\nLinks encontrados:")
        for link in links:
            if not executando:
                break  # Sai do loop se o programa foi interrompido
            print(link)
    else:
        print("Nenhum link encontrado.")
