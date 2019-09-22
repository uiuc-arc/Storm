data{
vector [228] Y2;
matrix [10, 3] Z;
int nB2;
int nB1;
int M;
int nB;
int N;
vector [228] Y1;
int nZ;
matrix [228, 3] X2;
matrix [228, 2] X1;
int ID[228];
}
parameters {
matrix[5,3] mu;
matrix[5,10] error_beta;
real<lower=-1,upper=1> rho_eq;
real<lower=0> sigma_eq;
vector<lower=0>[nB] sigma_beta;
}
transformed parameters{
matrix [ N,nB ] beta ;
beta <- Z*mu'+(diag_matrix(sigma_beta)*error_beta)';
}
model {
matrix [ N,nB1 ] beta1 ;
matrix [ N,nB2 ] beta2 ;
vector [ M ] lp ;
vector [ M ] value ;
print("sigma_eq=",sigma_eq);
sigma_eq ~ cauchy(0.0,2.0);
print("sigma_beta=",sigma_beta);
sigma_beta ~ cauchy(0.0,2.0);
to_vector(mu) ~ normal(0.0,3.0);
to_vector(error_beta) ~ normal(0.0,1.0);
beta1 <- block(beta,1,1,N,nB1);
beta2 <- block(beta,1,nB1+1,N,nB2);
for(m in 1:M){
if (Y1[m]==0){ 
lp[m] <- normal_cdf_log(-X1[m]*beta1[ID[m]]',0,1);

} 
 else {
value[m] <- (X1[m]*beta1[ID[m]]'+rho_eq/sigma_eq*(Y2[m]-X2[m]*beta2[ID[m]]'))/(1-rho_eq^2)^0.5;
lp[m] <- normal_cdf_log(value[m],0,1)-log(sigma_eq)-(Y2[m]-X2[m]*beta2[ID[m]]')^2/2/sigma_eq^2;
}
}
increment_log_prob(log_sum_exp(lp));
}
generated quantities{
vector [ nB ] m_beta ;
vector [ nB ] sd_beta ;
for(i in 1:nB){
m_beta[i] <- mean(col(beta,i));
sd_beta[i] <- sd(col(beta,i));
}
}
