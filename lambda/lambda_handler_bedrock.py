from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3
import json

opensearch_host = ""

def product_recommend(input_text,language):
    # 构建bedrock与 es客户端
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, 'us-east-1', 'es')
    esClient = OpenSearch(
        hosts = [{'host': opensearch_host, 'port': 443}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection,
        pool_maxsize = 20
    )
    brt = boto3.client(service_name='bedrock-runtime')
    if language == 'en':
        index = 'product-details-index-en'
    else: 
        index = 'product-details-index-cn'
    query = {  
      "size": 10,
      "sort": [
        {
          "_score": {
            "order": "desc"
          }
        }
      ],
      "_source": {
        "includes": ["ProductName", "Category", "Description", "ProductID","Image"]
      },
      "query": {
        "neural": {
          "product_embedding": {
            "query_text": input_text,
            "model_id": "m6jIgowBXLzE-9O0CcNs",
            "k": 13
          }
        }
      }
    }
    # 拼接 prompt
    es_response = esClient.search(
        body = query,
        index = index
    )
    try:
        es_res = es_response['hits']['hits'][0]
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'no result in system'})
        }
    # llm 构建答案
    if language == 'en':
        llm_prompt = 'Human: You are currently a professional clothing store assistant. The customer has asked you the following question: ' + input_text + ',You must respond to the customer inquiry using the provided information. Feel free to ask the customer for additional details if needed. Has a wide variety of clothing options, especially for women\'s fashion' + str(es_res) + ' Assistant:'
    else: 
        llm_prompt = 'Human: 你现在是一个导购客服，需要帮助客户推荐商品，根据商品的描述信息，给客户推荐具体的商品名称和编号. 客户的问题如下: ' + input_text + ',你必须基于以下商品信息进行推荐.适当的时候如果客户问题不清晰，可以反问一些关键信息.有各种各样的服装选择，尤其是女性时尚' + str(es_res) + ' Assistant:'
    
    llm_request_body = json.dumps({
        "prompt": llm_prompt,
        "max_tokens_to_sample": 4000,
        "temperature": 0.1,
        "top_p": 0.9,
    })
    
    modelId = 'anthropic.claude-v2:1'
    accept = 'application/json'
    contentType = 'application/json'
    
    response = brt.invoke_model(body=llm_request_body, modelId=modelId, accept=accept, contentType=contentType)
    
    response_body = json.loads(response.get('body').read())
    
    llm_result = response_body.get('completion')
    return llm_result,es_response
    
def reviews_analytis(input_text,language):
    # 构建bedrock与 es客户端
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, 'us-east-1', 'es')
    esClient = OpenSearch(
        hosts = [{'host': opensearch_host, 'port': 443}],
        http_auth = auth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection,
        pool_maxsize = 20
    )
    brt = boto3.client(service_name='bedrock-runtime')
    if language == 'en':
        index = 'product-reviews-index-en'
    else: 
        index = 'product-reviews-index-cn'
    query = {  
        "size" :50,
        "_source": {
          "includes": "combined_field"
        },
        "query": {
            "neural": {
              "product_reviews_embedding": {
                "query_text": input_text,
                "model_id": "m6jIgowBXLzE-9O0CcNs",
                "k": 11
              }
            }
          }
    }
    es_response = esClient.search(
        body = query,
        index = index
    )
    try:
        es_res = es_response['hits']['hits'][0]
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'no result in system'})
        }
    # llm 构建答案
    if language == 'en':
        llm_prompt = 'Human: You are now a customer service representative assisting customers in analyzing product reviews. Based on the historical comments about the product, you need to provide customers with a summary of the reviews, focusing primarily on the product rating and the emotional expressions conveyed in the comments. The customer\'s inquiries are as follows: ' + input_text + ',You must respond to the customer inquiry using the provided information. Feel free to ask the customer for additional details if needed.' + str(es_res) + ' Assistant:'
    else: 
        llm_prompt = 'Human: 你现在是一个导购客服，需要帮助客户分析商品的评价，根据商品过去的评论信息，给客户做评论总结，主要关注商品的评分，评论内容的情绪表达. 客户的问题如下: ' + input_text + ',你必须基于以下商品评价信息进行总结.适当的时候如果客户问题不清晰，可以反问一些关键信息.' + str(es_res) + ' Assistant:'
    
    llm_request_body = json.dumps({
        "prompt": llm_prompt,
        "max_tokens_to_sample": 4000,
        "temperature": 0.1,
        "top_p": 0.9,
    })
    
    modelId = 'anthropic.claude-v2:1'
    accept = 'application/json'
    contentType = 'application/json'
    
    response = brt.invoke_model(body=llm_request_body, modelId=modelId, accept=accept, contentType=contentType)
    
    response_body = json.loads(response.get('body').read())
    
    llm_result = response_body.get('completion')
    return llm_result,es_response

def lambda_handler(event, context):
    
    #接收参数 判断类型 
    query_params = event.get('queryStringParameters')
    # 接口请求类型
    type = query_params.get('type')
    # 语言版本 cn 中文 en 英文
    language = query_params.get('language')
    if event.get('body') is not None:
        body = json.loads(event.get('body'))
    else:
        body = []
    input_text = body.get('input_text')
    if  type == 'product_recommend':
        llm_result,es_response = product_recommend(input_text,language)
    else:
        llm_result,es_response = reviews_analytis(input_text,language)

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False,
        'body': json.dumps({
            'llm_result': llm_result,
            'es_response': es_response
        })
    }
