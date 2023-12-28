import boto3
import json
from decimal import Decimal
from datetime import datetime

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

# 获取全部商品列表
def get_products(language):
    dynamodb = boto3.resource('dynamodb')
    if language == 'en':
        table = dynamodb.Table('ProductDetails')
    else: 
        table = dynamodb.Table('ProductDetailsCN')
    response = table.scan()
    return response['Items']

# 获取指定商品的全部评价按时间排序
def get_product_reviews(product_id,language):
    dynamodb = boto3.resource('dynamodb')
    if language == 'en':
        table = dynamodb.Table('ProductReviews')
    else:
        table = dynamodb.Table('ProductReviewsCN')
    response = table.query(
        KeyConditionExpression='ProductID = :pk',
        ExpressionAttributeValues={
            ':pk': product_id,
        },
        ScanIndexForward=False  # 设置为 False 表示按排序键降序排序
    )
    return response['Items']

# 对指定商品添加评价
def add_product_review(product_id,product_name,rate,comment,user_id,language):
    dynamodb = boto3.resource('dynamodb')
    if language == 'en':
        table = dynamodb.Table('ProductReviews')
    else:
        table = dynamodb.Table('ProductReviewsCN')
    timestamp = int(datetime.now().timestamp())
    item = {
        'ProductID': product_id,
        'Timestamp': timestamp,
        'Comment': comment,
        'ProductName': product_name,
        'Rating': rate,
        'UserID': user_id
    }

    # 写入数据
    table.put_item(Item=item)
    return ['success']
    
def lambda_handler(event, context):
    # 根据URL 参数判断请求
    query_params = event.get('queryStringParameters', {})
    if event.get('body') is not None:
        post_params = json.loads(event.get('body'))
    else:
        post_params = []
    # 接口请求类型
    type = query_params.get('type')
    # 语言版本 cn 中文 en 英文
    language = query_params.get('language')
    
    result = []
    if  type == 'get_products':
        result = get_products(language)
    elif type == 'get_product_reviews':
        result = get_product_reviews(query_params.get('product_id'),language)
    elif type == 'add_product_review':
        product_id = post_params.get('product_id')
        product_name = post_params.get('product_name')
        rate = post_params.get('rate')
        comment = post_params.get('comment')
        user_id = post_params.get('user_id')
        result = add_product_review(product_id,product_name,rate,comment,user_id,language)
    else:
        result = ['request type error']
    # 返回api gateway 请求
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False,
        'body': json.dumps(result, cls=DecimalEncoder)
    }

