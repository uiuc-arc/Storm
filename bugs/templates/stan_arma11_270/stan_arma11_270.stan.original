data{
real y[1000];
int T;
}
parameters {
real mu;
real phi;
real theta;
real<lower=0> sigma;
}
model {
vector [ T ] nu ;
vector [ T ] err ;
nu[1] <- mu+phi*mu;
err[1] <- y[1]-nu[1];
for(t in 2:T){
nu[t] <- mu+phi*y[t-1]+theta*err[t-1];
err[t] <- y[t]-nu[t];
}
mu ~ normal(0.0,10.0);
phi ~ normal(0.0,2.0);
theta ~ normal(0.0,2.0);
sigma ~ cauchy(0.0,5.0);
err ~ normal(0.0,sigma);
}
