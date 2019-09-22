functions {
  matrix foo(vector v, int m, int n) {
    matrix[m,n] result;
    int i;
    result <- rep_matrix(0,m,n);
    i <- 0;
    return result;
  }
}
parameters {
  vector[6] y;
}
transformed parameters {
  matrix[3,2] z;
  z <- foo(y,3,2);
}
model {
  y ~ normal(0,1);
}