#mvn clean package
time=`date +%s`
mkdir -p out/diag_$time
java -cp target/testmin-0.1.0.jar:. tool.testmin.Main $time | tee out/diag_$time/run_log
