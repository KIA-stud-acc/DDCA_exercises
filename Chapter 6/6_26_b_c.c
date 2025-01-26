int int_div(int a, int b){  //функция, выполняющая целочисленное деление
  int quotient = 0;         //инициализация частного нулём
  int t3 = b;               //временная переменная хранящая делитель*n, где n -- проверяемое в цикле частное
  while (a>=t3){            //пока делимое больше, чем делитель умноженный на частное
    quotient++;             //инкрементировать частное
    t3 = t3 + b;            //увеличить временную переменную на делитель
  }
  return quotient;          //вернуть частное
}

int main(void){
  int ans = int_div(24, 3); //вызов функции со знаениями 24 и 3 (функция вернёт 8)
  return 0;
}
