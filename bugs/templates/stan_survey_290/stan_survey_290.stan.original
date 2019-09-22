data{
int nmax;
int k[5];
int m;
}
transformed data{
int <lower=0> nmin ;
nmin <- max(k);
}
parameters {
real<lower=0,upper=1> theta;
}
transformed parameters{
vector [ nmax ] lp_parts ;
for(n in 1:nmax){
if (n<nmin){ 
lp_parts[n] <- log(1.0/nmax)+negative_infinity();

} 
 else {
lp_parts[n] <- log(1.0/nmax)+binomial_log(k,n,theta);
}
}
}
model {
increment_log_prob(log_sum_exp(lp_parts));
}
generated quantities{
int <lower=1,upper=nmax> n ;
simplex [ nmax ] prob_n ;
prob_n <- softmax(lp_parts);
n <- categorical_rng(prob_n);
}
