//#include <stdio.h>
//я прекрасно осознаю, что такой алгоритм максимально неэффективен, и делал так только ради тренировки.
int fib(int n){
  if (n<=1){      //вернуть n если n меньше 2-х
    return n;
  }
  else {          //иначе рекурсивно вызвать функцию fib для n-1 и n-2 и вернуть сумму их возвращённых значений
    return fib(n-1)+fib(n-2);
  }
}

/*
int main(void){
  int c;
  while (c = getchar()-'0'){
    printf("%d\n", fib(c));
  }
}
*/