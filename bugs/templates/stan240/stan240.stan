parameters {
corr_matrix[100] Omega;
}
transformed parameters{
corr_matrix [ 100 ] OmegaCopy ;
OmegaCopy <- Omega;
}
model {
}
