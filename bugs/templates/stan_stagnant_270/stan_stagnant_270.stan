data{
real Y[29];
real x[29];
int N;
}
parameters {
simplex[N] theta;
real<lower=0> alpha;
real beta[2];
real<lower=0> sigma;
}
model {
real log_probs [ N ] ;
real mu [ N ] ;
theta ~ dirichlet(rep_vector(0.01,N));
alpha ~ normal(0.0,5.0);
beta ~ normal(0.0,5.0);
sigma ~ cauchy(0.0,5.0);
for(k in 1:N){
for(n in 1:N){
mu[n] <- alpha+if_else(n<=k,beta[1],beta[2])*(x[n]-x[k]);
}
log_probs[k] <- log(theta[k])+normal_log(Y,mu,sigma);
}
increment_log_prob(log_sum_exp(log_probs));
}
