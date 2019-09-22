data{
int y[6, 3];
real x[6];
int Nplates;
int Ndoses;
}
parameters {
real alpha;
real beta;
real gamma;
real<lower=0> tau;
vector[Nplates] lambdax[Ndoses];
}
transformed parameters{
real <lower=0> sigma ;
sigma <- 1.0/sqrt(tau);
}
model {
alpha ~ normal(0.0,100.0);
beta ~ normal(0.0,100.0);
gamma ~ normal(0.0,100000.0);
tau ~ gamma(0.001,0.001);
for(dose in 1:Ndoses){
lambdax[dose] ~ normal(0.0,sigma);
y[dose] ~ poisson_log(alpha+beta*log(x[dose]+10)+gamma*x[dose]+lambdax[dose]);
}
}
