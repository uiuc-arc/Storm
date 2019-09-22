data{
int Nobs;
int y[100];
int SubjIdx[100];
int Nsubj;
}
parameters {
real<lower=0> omega;
real<lower=0,upper=1> kappa;
vector<lower=0,upper=1>[Nsubj] theta;
}
transformed parameters{
real <lower=0> A ;
real <lower=0> B ;
A <- kappa*omega;
B <- (1-kappa)*omega;
}
model {
omega ~ gamma(2.0,3.0);
kappa ~ beta(7.0,3.0);
theta ~ beta(A,B);
for(obs in 1:Nobs){
y[obs] ~ bernoulli(theta[SubjIdx[obs]]);
}
}
