int soma(int a, int b) {
    return a + b;
}

int main() {
    int x = soma(1, 2);
    if (x > 0) {
        x = x - 1;
    } else {
        x = x + 1;
    }
    return 0;
}