from fastapi import FastAPI, HTTPException
from services.loader import load_data

app = FastAPI()

@app.get("/all_products/")
def get_all_products():
    return {"products": load_data()}

@app.get("/products/{product_name}")
def get_product_by_name(product_name: str):
    for product in load_data():
        if product.get("name", "").lower() == product_name.lower():
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/{product_name}/{product_field}")
def get_product_field(product_name: str, product_field: str):
    for product in load_data():
        if product.get("name", "").lower() == product_name.lower():
            if product_field in product:
                return {product_field: product[product_field]}
            raise HTTPException(status_code=404, detail="Field not found")
    raise HTTPException(status_code=404, detail="Product not found")