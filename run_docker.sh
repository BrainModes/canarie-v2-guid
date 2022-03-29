#docker build -t indoc/tokenizer:v0.1 .
docker run -d -p 5000:5000 -v /home/sliang/hdp/tokenizer:/app --add-host=psql_server:10.3.10.100 indoc/tokenizer:v0.1 