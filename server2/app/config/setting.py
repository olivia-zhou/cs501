TOKEN_EXPIRATION = 30 * 24 *  3600  #jwt 有效时间

# optional pooling params
FLASK_PIKA_POOL_PARAMS = {
    'pool_size': 8,
    'pool_recycle': 600
}