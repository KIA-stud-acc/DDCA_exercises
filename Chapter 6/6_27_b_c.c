void func(int a0, char a1[]){
  int t2 = 31;
  int t3;

  do {
    t3 = a0>>t2;
    t3 = t3 & 1;
    a1[1] = t3;
    a1++;
    t2--;
  } while(t2 >= 0);
}

//запись числа в бинарном виде в виде строки? Да.