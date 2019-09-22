data{
vector [262] roach1;
int N;
vector [262] treatment;
int y[262];
vector [262] senior;
vector [262] exposure2;
}
transformed data{
vector [ N ] log_expo ;
log_expo <- log(exposure2);
}
parameters {
vector[4] beta;
}
model {
y ~ poisson_log(log_expo+beta[1]+beta[2]*roach1+beta[3]*treatment+beta[4]*senior);
}
