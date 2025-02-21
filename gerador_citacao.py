#!/usr/bin/env python3

# Função para formatar o nome dos autores no padrão ABNT
def formatar_nome_autor(nome):
    partes = nome.split()
    if len(partes) > 1:
        ultimo_sobrenome = partes[-1].upper()  # Último sobrenome em caixa alta
        restante_nome = " ".join(partes[:-1])  # Restante do nome normal
        return f"{ultimo_sobrenome}, {restante_nome}"
    return nome.upper()


# Função para formatar a citação conforme o tipo de documento
def formatar_citacao(tipo, dados):
    if tipo == "artigo":
        # Formatação para artigos científicos
        autores = "; ".join([formatar_nome_autor(autor) for autor in dados['autores']])
        doi = f" DOI: {dados['doi']}." if dados.get("doi") else ""
        paginacao = f" p. {dados['paginacao']}." if dados.get("paginacao") else ""
        volume = f" v. {dados['volume']}," if dados.get("volume") else ""
        numero = f" n. {dados['numero']}," if dados.get("numero") else ""
        return (
            f"{autores}. {dados['titulo']}. {dados['revista']},{volume}{numero} {dados['ano']}.{paginacao}{doi}"
        )

    elif tipo == "livro":
        # Formatação para livros
        autores = "; ".join([formatar_nome_autor(autor) for autor in dados['autores']])
        organizador = " (Org.)" if dados.get("organizador") == "s" else ""
        edicao = f" {dados['edicao']} ed." if dados.get("edicao") else ""
        volume = f" v. {dados['volume']}" if dados.get("volume") else ""
        doi = f" DOI: {dados['doi']}." if dados.get("doi") else ""
        url = f" Disponível em: {dados['url']}." if dados.get("url") else ""
        return (
            f"{autores}{organizador}. {dados['titulo']}.{edicao}{volume} {dados['local']}: {dados['editora']}, {dados['ano']}.{doi}{url}"
        )

    elif tipo == "capitulo":
        # Formatação para capítulos de livros
        autores_capitulo = "; ".join([formatar_nome_autor(autor) for autor in dados['autores']])
        autores_livro = "; ".join([formatar_nome_autor(autor) for autor in dados['autores_livro']])
        organizador = f" In: {autores_livro} (Org.)." if dados.get("livro_tem_organizador") else f" In: {autores_livro}."
        edicao = f" {dados['edicao']} ed." if dados.get("edicao") else ""
        volume = f" v. {dados['volume']}" if dados.get("volume") else ""
        doi = f" DOI: {dados['doi']}." if dados.get("doi") else ""
        url = f" Disponível em: {dados['url']}." if dados.get("url") else ""
        return (
            f"{autores_capitulo}. {dados['titulo']}.{organizador} {dados['livro']}.{edicao}{volume} {dados['local']}: {dados['editora']}, {dados['ano']}. p. {dados['paginas']}.{doi}{url}"
        )

    elif tipo == "documento_oficial":
        # Formatação para documentos oficiais
        return (
            f"{dados['orgao']}. {dados['titulo']}. {dados['tipo']}, nº {dados['numero']}, de {dados['data']}. Disponível em: {dados['url']}. Acesso em: {dados['acesso']}."
        )

    elif tipo == "site":
        # Formatação para sites
        autores = "; ".join([formatar_nome_autor(autor) for autor in dados['autores']])
        return f"{autores}. {dados['titulo']}. Disponível em: {dados['url']}. Acesso em: {dados['acesso']}."

    else:
        return "Tipo de documento não suportado."


# Função para solicitar os nomes dos autores
def solicitar_autores(mensagem="Digite os nomes dos autores. Deixe em branco para finalizar."):
    autores = []
    print(mensagem)
    while True:
        try:
            autor = input(f"Autor {len(autores) + 1}: ").strip()
            if not autor and len(autores) > 0:
                break
            elif not autor and len(autores) == 0:
                print("Pelo menos um autor deve ser informado.")
                continue
            autores.append(autor)
        except KeyboardInterrupt:
            print("\n\nVocê pressionou Ctrl+C. Retornando ao menu principal...\n")
            raise
    return autores


# Função principal do programa
def main():
    while True:
        try:
            print("\n=== Gerador de Citações ABNT ===")
            print("Escolha o tipo de documento:")
            print("1. Artigo em periódico")
            print("2. Livro")
            print("3. Capítulo de livro")
            print("4. Documento oficial")
            print("5. Site")
            print("6. Sair")
            opcao = input("Digite o número correspondente: ")

            if opcao == "6":
                print("Encerrando o programa. Até logo!")
                break

            if opcao == "1":
                tipo = "artigo"
                dados = {
                    "autores": solicitar_autores(),
                    "titulo": input("Título do artigo: "),
                    "revista": input("Nome da revista: "),
                    "ano": input("Ano de publicação: "),
                    "paginacao": input("Paginação (ex.: 10-20, deixe em branco se não houver): ").strip() or None,
                    "doi": input("DOI (deixe em branco se não houver): ").strip() or None,
                    "volume": input("Volume (deixe em branco se não houver): ").strip() or None,  # Adicionado campo volume
                    "numero": input("Número (deixe em branco se não houver): ").strip() or None,  # Adicionado campo número
                }

            elif opcao == "2":
                tipo = "livro"
                dados = {
                    "autores": solicitar_autores(),
                    "titulo": input("Título do livro: "),
                    "local": input("Local de publicação: "),
                    "editora": input("Editora: "),
                    "ano": input("Ano de publicação: "),
                    "organizador": input("O autor é também organizador da obra? (s/n): ").lower(),
                    "edicao": input("Edição (deixe em branco se não houver): ").strip() or None,
                    "volume": input("Volume (deixe em branco se não houver): ").strip() or None,
                    "doi": input("DOI (deixe em branco se não houver): ").strip() or None,  # Adicionado campo DOI
                    "url": input("URL (deixe em branco se não houver): ").strip() or None,  # Adicionado campo URL
                }

            elif opcao == "3":
                tipo = "capitulo"
                dados = {
                    "autores": solicitar_autores("Digite os nomes dos autores do capítulo. Deixe em branco para finalizar."),
                    "titulo": input("Título do capítulo: "),
                    "livro": input("Título do livro: "),
                }
                dados["autores_livro"] = solicitar_autores(
                    "Digite os nomes dos autores/organizadores do livro. Deixe em branco para finalizar."
                )
                dados["livro_tem_organizador"] = input("Os autores do livro são organizadores? (s/n): ").lower() == "s"
                dados.update({
                    "local": input("Local de publicação: "),
                    "editora": input("Editora: "),
                    "ano": input("Ano de publicação: "),
                    "paginas": input("Páginas do capítulo (ex.: 10-20): "),
                    "edicao": input("Edição (deixe em branco se não houver): ").strip() or None,
                    "volume": input("Volume (deixe em branco se não houver): ").strip() or None,
                    "doi": input("DOI (deixe em branco se não houver): ").strip() or None,  # Adicionado campo DOI
                    "url": input("URL (deixe em branco se não houver): ").strip() or None,  # Adicionado campo URL
                })

            elif opcao == "4":
                tipo = "documento_oficial"
                dados = {
                    "orgao": input("Órgão responsável: "),
                    "titulo": input("Título do documento: "),
                    "tipo": input("Tipo de documento (ex.: Portaria, Lei, Decreto): "),
                    "numero": input("Número do documento: "),
                    "data": input("Data de publicação (DD/MM/AAAA): "),
                    "url": input("URL: "),
                    "acesso": input("Data de acesso (DD/MM/AAAA): "),
                }

            elif opcao == "5":
                tipo = "site"
                dados = {
                    "autores": solicitar_autores(),
                    "titulo": input("Título da página: "),
                    "url": input("URL: "),
                    "acesso": input("Data de acesso (DD/MM/AAAA): "),
                }

            else:
                print("Opção inválida!")
                continue

            citacao = formatar_citacao(tipo, dados)
            print("\nCitação formatada na ABNT:")
            print(citacao)

        except KeyboardInterrupt:
            print("\n\nVocê pressionou Ctrl+C. Encerrando o programa. Até logo!\n")
            break


if __name__ == "__main__":
    main()
