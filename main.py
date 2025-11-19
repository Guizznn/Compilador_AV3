# main.py
from lexer import lexer
# O parser foi importado mas vamos focar na saída Léxica exigida pelo Barema
# from parser import Parser, pretty 

def main():
    nome_arquivo = "teste.c"
    
    # 1. PRÉ REQUISITO: LEITURA DO ARQUIVO FONTE
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            code = f.read()
            print(f"--- LENDO ARQUIVO: {nome_arquivo} ---\n")
            print(code)
            print("\n" + "="*40 + "\n")
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Arquivo '{nome_arquivo}' não encontrado.")
        return

    # Executa o analisador léxico
    tokens = lexer(code)

    # Estruturas para o Barema
    tabela_simbolos = {} 
    lista_tokens_formatada = []
    
    # Lógica para separar Tokens de Símbolos
    # Símbolos são apenas os Identificadores (ID) das variáveis/funções
    ordem_simbolo = 1

    print(">>> 1. LISTA DOS TOKENS <<<")
    print(f"{'TIPO':<20} | {'VALOR'}")
    print("-" * 40)

    for token in tokens:
        tipo, valor = token
        
        # Imprime na Lista de Tokens
        print(f"{tipo:<20} | {valor}")
        
        # Lógica da Tabela de Símbolos
        # Se for um Identificador (ID), vai para a tabela de símbolos
        if tipo == "ID":
            if valor not in tabela_simbolos:
                tabela_simbolos[valor] = {
                    'ordem': ordem_simbolo,
                    'tipo': 'IDENTIFICADOR' # Em compiladores simples, começa como genérico
                }
                ordem_simbolo += 1

    print("\n" + "="*40 + "\n")

    print(">>> 2. TABELA DE SÍMBOLOS <<<")
    print(f"Quantidade de Símbolos Encontrados: {len(tabela_simbolos)}")
    print("-" * 50)
    print(f"{'ORDEM':<10} | {'SÍMBOLO (ID)':<20} | {'CATEGORIA'}")
    print("-" * 50)

    for simbolo, dados in tabela_simbolos.items():
        print(f"{dados['ordem']:<10} | {simbolo:<20} | {dados['tipo']}")

    print("\n" + "="*40 + "\n")
    print("Análise Léxica concluída com sucesso.")

if __name__ == "__main__":
    main()