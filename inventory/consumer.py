from main import redis,Product
import time

key ='complete_status'
group ='inventory-group'

try:
    redis.xgroup_create(key,group)
except:
    print('Group Already Exists!') 

while True:
    try:
        results =redis.xreadgroup(group,key,{key:'>'},None)
        if results != []:
            for result in results:
               obj = result[1][0][1]
            try:
                  
               product = Product.get(obj['product_id'])
               product.quantity = product.quantity - int(obj['quantity'])
               product.save()
               print(product)
            except:
                redis.xadd('refund_order',obj,'*')   
        
        print(results)
    except Exception as e:
        print(str(e))
    time.sleep(2)    



