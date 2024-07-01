from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI, HTTPException, Path


app = FastAPI()

# Redis connection configuration
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


# Define a Product model using HashModel from redis_om
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis  #Link the Product model to the Redis connection


# Endpoint to retrieve all products
@app.get('/products')
def all_products():
    return [format(pk) for pk in Product.all_pks()]  #wCorrected method name from all_pks to all()

def format(pk:str):
    product =Product.get(pk)
    return{
        'id':product.pk,
        'name':product.name,
        'price':product.price,
        'quantity':product.quantity
    }



# Endpoint to create a new product
@app.post('/addproducts')
def create_product(product: Product):
    product.save()  # Save the product to Redis
    return {"message": "Product created successfully"}


#get product by hashid
@app.get('/products/{hashid}')
def get_product(hashid: str = Path(...)):
    try:
        product = Product.get(hashid)
        return product
    except KeyError:
        raise HTTPException(status_code=404)
    
@app.delete('/products/{hashid}')  
def delete_product(hashid: str):
    product = Product.get(hashid)
    return product.delete(hashid)