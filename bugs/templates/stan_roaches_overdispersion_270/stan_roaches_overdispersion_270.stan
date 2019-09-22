data{
vector [262] roach1;
int N;
vector [262] treatment;
int y[262];
vector [262] senior;
vector [262] exposure2;
}
transformed data{
vector [ N ] log_expo ;
log_expo <- log(exposure2);
}
parameters {
vector[4] beta;
real<lower=0> tau;
vector[N] lambdax;
}
transformed parameters{
real <lower=0> sigma ;
sigma <- 1.0/sqrt(tau);
}
model {
tau ~ gamma(0.001,0.001);
for(i in 1:N){
lambdax[i] ~ normal(0.0,sigma);
y[i] ~ poisson_log(lambdax[i]+log_expo[i]+beta[1]+beta[2]*roach1[i]+beta[3]*senior[i]+beta[4]*treatment[i]);
}
}
