data{
real y[100];
int N;
}
parameters {
real lambda1;
real lambda2;
real<lower=0> sigma;
}
transformed parameters{
real mu ;
mu <- lambda1+lambda2;
}
model {
lambda1 ~ normal(0,10);
lambda2 ~ normal(0,10);
y ~ normal(mu,sigma);
}
