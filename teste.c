#include <stdio.h>
#define MAX_ITERACOES 5

// Teste de tipos de dados, declarações e inicialização
int global_var = 10;
const float PI = 3.14159;

struct Ponto {
    int x;
    int y;
};

enum Cor {
    VERMELHO = 1,
    AZUL,
    VERDE
};

// Protótipo de função
int calcular_soma(int a, int b);

void main() {
    // Declaração de variáveis locais
    int a = 0x10; // Literal hexadecimal
    int b = 20U;  // Literal com sufixo
    int resultado = 0;
    char caractere = 'A'; // Literal de caractere
    
    struct Ponto p;
    p.x = 5;
    p.y = 10;
    
    // Teste de operadores de atribuição composta
    resultado += a;
    resultado -= b;
    
    // Teste de operadores unários e pós-fixados
    a++;
    --b;
    
    // Teste de do-while
    do {
        resultado = calcular_soma(a, b);
        a--;
    } while (a > 0);
    
    // Teste de if-else
    if (resultado > 50) {
        printf("Resultado alto\n");
    } else if (resultado > 20) {
        printf("Resultado medio\n");
    } else {
        printf("Resultado baixo\n");
    }
    
    // Teste de switch-case
    switch (resultado) {
        case 1:
            printf("Caso 1\n");
            break;
        case MAX_ITERACOES:
            printf("Caso MAX_ITERACOES\n");
            break;
        default:
            printf("Caso default\n");
    }
    
    // Teste de for
    for (int i = 0; i < 3; i++) {
        printf("Iteracao %d\n", i);
    }
    
    // Teste de while
    while (global_var > 0) {
        global_var--;
    }
    
    // Teste de operador ternário
    int max = (a > b) ? a : b;
    
    return;
}

int calcular_soma(int a, int b) {
    return a + b;
}