int sum(int a, int b) {
    int r = a + b;
    return r;
}

int main() {
    int x = 10;
    int y = sum(x, 20);
    if (y > 20) {
        y = y - 1;
    }
    return 0;
}
