from unidecode import unidecode

# Caminho do arquivo de entrada e saída
arquivo_entrada = '/home/rodrigo/nomes.txt'
arquivo_saida = '/home/rodrigo/nomes_sem_acentos.txt'

# Função para processar o arquivo
def remover_acentos(arquivo_entrada, arquivo_saida):
    try:
        # Abre o arquivo de entrada para leitura
        with open(arquivo_entrada, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()

        # Processa cada linha removendo acentos e convertendo para maiúsculas
        linhas_sem_acentos = [unidecode(linha.strip()).upper() + '\n' for linha in linhas]

        # Salva o resultado no arquivo de saída
        with open(arquivo_saida, 'w', encoding='utf-8') as arquivo:
            arquivo.writelines(linhas_sem_acentos)

        print(f"Arquivo processado com sucesso! Resultado salvo em: {arquivo_saida}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Executa a função
remover_acentos(arquivo_entrada, arquivo_saida)
