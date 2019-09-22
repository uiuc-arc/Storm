data{
vector [10] alpha_user;
int word[326];
int I;
int K;
int N;
int item[326];
vector [17] beta;
int U;
int user[326];
int V;
vector [10] alpha_item;
}
parameters {
simplex[K] item_topics[I];
simplex[K] user_topics[U];
simplex[V] word_topics[K];
}
model {
for(i in 1:I){
item_topics[i] ~ dirichlet(alpha_item);
}
for(u in 1:U){
user_topics[u] ~ dirichlet(alpha_user);
}
for(k in 1:K){
word_topics[k] ~ dirichlet(beta);
}
for(n in 1:N){
real gamma [ K ] ;
for(k in 1:K){
gamma[k] <- log(item_topics[item[n],k]+user_topics[user[n],k])+log(word_topics[k,word[n]]);
}
increment_log_prob(log_sum_exp(gamma));
}
}
