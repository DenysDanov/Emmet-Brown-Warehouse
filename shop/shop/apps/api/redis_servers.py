import redis
r = redis.Redis()
user_cart_store = redis.Redis(host='127.0.0.1', port=6379, db = 1)