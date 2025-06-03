import redis

r = redis.Redis(decode_responses=True)
print(r.mget("absaitovdev@gmail.com")[0])