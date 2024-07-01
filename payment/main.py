from fastapi import FastAPI,BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI, HTTPException, Path
from starlette.requests import Request
import requests,time


app = FastAPI()

#it should be new data base for paymnet
redis = get_redis_connection(
   host='redis-12500.c212.ap-south-1-1.ec2.redns.redis-cloud.com',
   port=12500,
   password='cYQ7CUTgN4ZiEzN4Ce5zBBa42TaW3Jq3',
   decode_responses=True
)





# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5000'],  # Corrected 'allow_origins' spelling and URL format
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Order(HashModel):
    product_id: str
    price :float
    fee : float
    total:float
    quantity:int
    status:str 

    class Meta:
        database =redis

@app.get('/orders/{pk}')
def get(pk:str):
    print(pk)
    order =Order.get(pk)
    redis.xadd('refund_order',[],'*')
    return Order.get(pk)


@app.post('/orders')
async def create (request: Request,background_task:BackgroundTasks): #id, quantity
    body = await request.json()
    print(body)

    req = requests.get('http://127.0.0.1:8086/products/%s' % body['id'])
    product = req.json()
    print(req)

    order = Order(
        product_id =body['id'],
        price = product['price'],
        fee = 0.2 * product['price'],
        total =1.2*product['price'],
        quantity = body['quantity'],
        status = 'pending'

    )

    order.save()
    background_task.add_task(complete_status,order)
    return order

def complete_status(order):
    time.sleep(5)
    order.status ="complete"
    print(order.status)
    order.save()
    redis.xadd('complete_status',order.dict(),'*')
    print(redis)
    print(order.status)

































  


