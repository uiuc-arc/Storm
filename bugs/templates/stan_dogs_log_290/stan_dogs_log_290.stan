data{
int y[31, 25];
int n_dogs;
int n_trials;
}
parameters {
real aux_param1;
real aux_param0;
vector[2] beta;
real aux_param3;
real aux_param2;
real aux_param4;
}
transformed parameters{
matrix [ n_dogs,n_trials ] n_avoid ;
matrix [ n_dogs,n_trials ] n_shock ;
matrix [ n_dogs,n_trials ] p ;
for(j in 1:n_dogs){
n_avoid[j,1] <- 0;
n_shock[j,1] <- 0;
for(t in 2:n_trials){
n_avoid[j,t] <- n_avoid[j,t-1]+1-y[j,t-1];
n_shock[j,t] <- n_shock[j,t-1]+y[j,t-1];
}
for(t in 1:n_trials){
p[j,t] <- inv_logit(beta[1]*n_avoid[j,t]+beta[2]*n_shock[j,t]);
}
}
}
model {
aux_param1 ~ normal(0.0,4.552333);
aux_param0 ~ normal(-100,4.027751);
beta[1] ~ uniform(aux_param0,aux_param1);
aux_param3 ~ normal(100.0,4.64364);
aux_param2 ~ normal(0.0,3.920872);
beta[2] ~ uniform(aux_param2,aux_param3);
for(i in 1:n_dogs){
for(j in 1:n_trials){
aux_param4 ~ beta(p[i,j],1-p[i,j]);
y[i,j] ~ bernoulli(aux_param4);
}
}
}
