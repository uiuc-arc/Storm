parameters {
real x;
}
model {
vector [ 2 ] a_vec ;
vector [ 2 ] b_vec ;
vector [ 4 ] c_vec ;
a_vec <- rep_vector(1,2);
b_vec <- rep_vector(2,2);
c_vec <- append_row(a_vec,b_vec);
print("c_vec = ",c_vec);
x ~ normal(0.0,1.0);
}
