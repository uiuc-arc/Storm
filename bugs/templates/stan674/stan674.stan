parameters {
real<lower=0> a;
real<lower=0> x;
}
model {
real c ;
c <- gamma_p(a,x);
a ~ normal(20.0,1.0);
x ~ normal(20.0,1.0);
}
