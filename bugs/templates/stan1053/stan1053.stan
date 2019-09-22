model {
}
generated quantities{
real <lower=0> lambdax ;
real x ;
lambdax <- lognormal_rng(10E10,10);
x <- poisson_rng(lambdax);
if (x<0){ 
print("bug: ",x);
}
}
