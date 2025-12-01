from lexer import lexer
from parser import Parser, pretty_compact 

def main():
    nome_arquivo = "teste.c"
    
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            code = f.read()
            print(f"--- LENDO ARQUIVO: {nome_arquivo} ---\n")
            print(code)
            
           
            lines = code.split('\n')
            processed_lines = [line for line in lines if not line.strip().startswith('#')]
            code = '\n'.join(processed_lines)
            
            print("\n--- CÓDIGO APÓS PRÉ-PROCESSAMENTO SIMPLES ---\n")
            print(code)
            print("\n" + "="*40 + "\n")
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Arquivo '{nome_arquivo}' não encontrado.")
        return

  
    tokens = lexer(code)

    
    tabela_simbolos = {} 
    
    
    ordem_simbolo = 1

    print(">>> 1. LISTA DOS TOKENS <<<")
    print(f"{'TIPO':<20} | {'VALOR'}")
    print("-" * 40)

    for token in tokens:
        tipo, valor = token
        
       
        print(f"{tipo:<20} | {valor}")
        
        
        if tipo == "ID":
            if valor not in tabela_simbolos:
                tabela_simbolos[valor] = {
                    'ordem': ordem_simbolo,
                    'tipo': 'IDENTIFICADOR'
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
    
   
    print(">>> 3. ANÁLISE SINTÁTICA (PARSER) <<<")
    
    try:
        parser_instance = Parser(tokens)
        
        
        ast_root = parser_instance.parse()
        
        print("\n--- ÁRVORE DE SINTAXE ABSTRATA (AST) ---\n")
        
        print(pretty_compact(ast_root))

    except Exception as e:
        print(f"\nERRO DE PARSING: {e}")
        
    print("\n" + "="*40 + "\n")
    print("Análise Léxica e Sintática concluídas com sucesso.")


if __name__ == "__main__":
    main()