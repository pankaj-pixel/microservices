import redis




try:
    r = redis.StrictRedis()
   
    r.set('test_key', 'test_value')
   
    value = r.get('test_key')

    if value == 'test_value':
        print("Redis connection successful.")
    else:
        print("Redis connection failed.")

except redis.exceptions.ConnectionError as e:
    print(f"Error connecting to Redis: {e}")
