data{
int K;
}
parameters {
corr_matrix[100] Omega;
vector<lower=0>[100] sigma;
}
transformed parameters{
cov_matrix [ K ] Sigma ;
Sigma <- multiply_lower_tri_self_transpose(diag_pre_multiply(sigma,Omega));
}
model {
}
