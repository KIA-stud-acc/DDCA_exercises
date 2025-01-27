#include <stdio.h>

void maxSumSubArray(int a[], int n){
  int start = 0;
  int end   = 0;
  int start_frame = 0;
  int max = a[0];
  int tmp = a[0];

  for (int i = 1; i<n; i++){
    if (tmp>0){
      tmp = tmp+a[i];
    }
    else {
      tmp = a[i];
      start_frame = i;
    }

    if (tmp>max){
      max = tmp;
      start = start_frame;
      end = i;
    }
  }
  for(; start<=end; start++){
    printf("%d ", a[start]);
  }
}

int main(void){
  int arr[] = {-2,3,-1,5,-10,-2,5,-1,15};
  maxSumSubArray(arr, 9);
  return 0;
}


