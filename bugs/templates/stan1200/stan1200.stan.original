data{
int n_vars;
matrix [1000, 10] X_train;
vector [10] prior_mean;
matrix [10, 10] prior_cov;
int y_train[1000];
int n_train_data;
}
parameters {
vector[n_vars] beta;
}
model {
beta ~ multi_normal(prior_mean,prior_cov);
y_train ~ poisson_log(X_train*beta);
}
