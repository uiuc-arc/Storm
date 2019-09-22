data{
int y[3];
int N;
}
parameters {
simplex[N] x;
}
model {
y ~ multinomial(x);
}
generated quantities{
int y_rep [ N ] ;
y_rep <- multinomial_rng(x,50);
}
