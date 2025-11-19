# 🧵 Compilador em Python para Subconjunto da Linguagem C

Este projeto é um **compilador completo**, escrito em Python, capaz de analisar um **subconjunto da linguagem C**.  
O compilador possui:

- **Lexer** (analisador léxico)
- **Parser** (analisador sintático)
- **Árvore Sintática Abstrata** (AST)
- **Interpretador** simples

O objetivo é demonstrar o funcionamento interno de um compilador, como estudado na disciplina de **Compiladores**.

---

## 📚 Funcionalidades

O compilador atualmente suporta:

### ✔️ Tipos e declarações
- `int`
- Variáveis locais
- Declaração com inicialização
- Atribuição

### ✔️ Expressões aritméticas
- `+`, `-`, `*`, `/`
- Parênteses
- Precedência correta

### ✔️ Funções
- Declaração de funções
- Parâmetros
- Escopo
- `return`

### ✔️ Comandos de controle
- `if (...) { }`
- `else`
- `while (...) { }`

### ✔️ Chamadas de função
- `sum(x, 20);`

### ✔️ Blocos `{}`



