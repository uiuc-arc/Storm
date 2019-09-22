parameters {
vector[2] y;
vector[3] x;
}
transformed parameters{
vector [ 5 ] z ;
z <- append_row(x,y);
}
model {
z ~ normal(0.0,1.0);
}
