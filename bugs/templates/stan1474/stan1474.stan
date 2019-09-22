parameters {
vector<lower=0>[5] alpha;
}
model {
alpha ~ normal(0.0,0.0001);
}
generated quantities{
simplex [ 5 ] beta ;
beta <- dirichlet_rng(alpha);
}
