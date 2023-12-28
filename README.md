# ShopAnalytica
Using DynamoDB zero-ETL for near real-time vectorization of business data, transferring it to OpenSearch. Combining Bedrock embedded model and LLM model for product recommendations and sentiment analysis on customer reviews.
 ## 部署步骤
 ![Alt text](workshop-ddb-opensearch-llm.jpg)
 1. 创建dynamodb tables 并导入示例数据；
 2. 创建opensearch 集群及对应的IAM Roles；
 3. 配置dynamodb 到 opensearch数据集成的pipeline；
 4. 部署lambda function及apigateway;
 5. 部署前端服务，修改接口地址到对应的 apigateway url.