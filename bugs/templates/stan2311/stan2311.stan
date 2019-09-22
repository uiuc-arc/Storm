transformed data{
real lo ;
lo <- negative_infinity();
print("Finished transforming data.");
}
parameters {
real scale;
}
transformed parameters{
print("In transformed parameters");
}
model {
print("Starting model.");
scale ~ normal(0.0,1.0);
reject("QUIT");
}
