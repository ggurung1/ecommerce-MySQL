#!/bin/env/python

import random 
from faker import Faker
from datetime import datetime,timedelta

fake=Faker()

#---------config--------
NUM_CUSTOMERS=400
NUM_ORDERS=800
EMAIL_DOMAINS=["gmail.com","yahoo.com","hotmail.com"]
ORDER_STATUSES=["Pending","Shipped","Delivered","Cancelled"]
PAYMENT_METHODS=["Credit Card","PayPal","Bank Transfer","Apple Pay"]
COUNTRIES=['UK','USA','China','EU']


## Categories with realistic price ranges (min,max)
#categories={"Electronics": (50,2000),"Clothing": (10,500), "Books":(10,100),"Furniture": (50,1500),"Sports":(30,400),"Toys":(10,300)}

# Using product catalog with category Id,[product_1, min price,max price],...

categories = {
    "Electronics": (1,["Phone",600,1500], ["Laptop",800,3000], ["Tablet",300,1200], ["Headphones",50,1000], ["Smartwatch",80,500],
                    ["Monitor",100,900], ["Camera",400,1800], ["Speaker",20,600]),
    "Clothing": (2,["T-Shirt",10,800], ["Jeans",50,900], ["Jacket",25,1200], ["Dress",60,500], ["Shoes",40,800], ["Sweater",25,500], 
                 ["Hoodie",20,300]),
    "Books": (3,["Anime",15,200], ["Novel",15,300], ["Poem",10,100], ["Story",10,100], ["Series",50,500], ["Essay",10,100]),
    "Furniture": (4,["Sofa",40,1500], ["Chair",30,400], ["Table",40,600], ["Desk",50,800], ["Bed",80,1000],
                  ["Wardrobe",80,1000], ["Bookshelf",10,300], ["Couch",100,1200]),
    "Sports":(5,["Football",30,100], ["Tennis Racket",20,400], ["Basketball",30,200], ["Yoga Mat",10,100],
              ["Bicycle",80,1000], ["Helmet",30,200]),
    "Toys": (6,["Legos",10,300],[ "Puzzle",10,80], ["Doll",10,200], ["Vehiclemodel",10,300])
}


#Date range for orders
start_date=datetime(2024,1,1)
end_date=datetime(2024,12,31)


def random_date(start,end):
	delta=end-start
	return start+timedelta(days=random.randint(0,delta.days))

# Generate customers

customers=[]
used_emails = set()  # track unique emails

for _ in range(NUM_CUSTOMERS):
    while True:
        first = fake.first_name()
        last = fake.last_name()
        email = f"{first.lower()}.{last.lower()}@{random.choice(EMAIL_DOMAINS)}"

        # Ensure uniqueness
        if email not in used_emails:
            used_emails.add(email)
            break  # exit the loop only when we find a unique email

    country = random.choice(COUNTRIES)
    customers.append((first, last, email, country))

# Generate products
products=[]
product_id=1
category_names=list(categories.keys())
#for cat in category_names:
#	for i in range(5): # 5 products per category that is total 30 products
#		name=fake.word().capitalize()
#		price=round(random.uniform(categories[cat][0],categories[cat][1]),2)
#		products.append((product_id,name,price,category_names.index(cat)+1))
#		product_id+=1


products=[]
product_id=1
for category, items in categories.items():
    for item in items[1:]:
        name=item[0]
        price=round(random.uniform(item[1],item[2]),2)
        products.append((product_id,name,price,items[0]))
        product_id+=1

#---------Generate Orders and Items
orders=[]
order_items=[]
payments=[]

order_id_counter=1
order_item_id_counter=1
payment_id_counter=1

for _ in range(NUM_ORDERS):
	cust_id=random.randint(1,NUM_CUSTOMERS)
	order_status=random.choice(ORDER_STATUSES)
	order_date=random_date(start_date,end_date)

	orders.append((order_id_counter,cust_id,order_date.strftime("%Y-%m-%d"),order_status))
	
	# Each order has 1-5 items
	num_items=random.randint(1,5)
	subtotal=0
	
	for _ in range(num_items):
		product=random.choice(products)
		product_id=product[0]
		price=product[2]
		category_id=product[3]

		# Quantity depends on category
		if category_id==1: # Electronics
			quantity=random.randint(1,3)
		elif category_id in [2,3]: # Clothing, Books
			quantity=random.randint(1,10)
		else: #Furniture,Sports,Toys
			quantity=random.randint(1,5)

		subtotal +=price*quantity

		order_items.append((order_item_id_counter,order_id_counter,product_id,quantity))

		order_item_id_counter+=1

	# Payments only for shipped/Delivered orders
	if order_status in ["Shipped","Delivered"]:
		payment_date=order_date+timedelta(days=random.randint(0,7))
		method=random.choice(PAYMENT_METHODS)
		payments.append((payment_id_counter,order_id_counter,round(subtotal,2),method,payment_date.strftime("%Y-%m-%d")))		
		payment_id_counter+=1

	order_id_counter+=1


#-------- Write SQL file-----

with open("ecommerce_data.sql","w") as f:
	f.write("-- Generated e-commerce data\n\n")

	#customers
	f.write("INSERT INTO customers (first_name,last_name,email,country) VALUES\n")
	f.write(",\n".join([f"('{c[0]}','{c[1]}','{c[2]}','{c[3]}')" for c in customers]))
	f.write(";\n\n")

	#categories
	f.write("INSERT INTO categories (category_name) VALUES\n")
	f.write(",\n".join([f"('{cat}')" for cat in category_names]))
	f.write(";\n\n")

	#products
	f.write("INSERT INTO products (product_name,price,category_id) VALUES\n")
	f.write(",\n".join([f"('{p[1]}',{p[2]},{p[3]})" for p in products]))
	f.write(";\n\n")

	#Orders
	f.write("INSERT INTO orders (customer_id,order_date,order_status) VALUES\n")
	f.write(",\n".join([f"({o[1]},'{o[2]}','{o[3]}')" for o in orders]))
	f.write(";\n\n")

	#order Items
	f.write("INSERT INTO order_items (order_id,product_id,quantity) VALUES\n")
	f.write(",\n".join([f"({oi[1]},{oi[2]},{oi[3]})" for oi in order_items]))
	f.write(";\n\n")


	#payments
	f.write("INSERT INTO payments (order_id,amount,method,payment_date) VALUES\n")
	f.write(",\n".join([f"({p[1]},{p[2]},'{p[3]}','{p[4]}')" for p in payments]))
	f.write(";\n\n")


print("data generated successfully!")
