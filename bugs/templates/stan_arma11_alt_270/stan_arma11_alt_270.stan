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
real err ;
mu ~ normal(0.0,10.0);
phi ~ normal(0.0,2.0);
theta ~ normal(0.0,2.0);
sigma ~ cauchy(0.0,5.0);
err <- y[1]-mu+phi*mu;
err ~ normal(0.0,sigma);
for(t in 2:T){
err <- y[t]-(mu+phi*y[t-1]+theta*err);
err ~ normal(0.0,sigma);
}
}
