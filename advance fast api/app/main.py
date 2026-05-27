"""
=============================================================
  FastAPI — Sorting + Pagination + Filtering + Searching
  Ek complete runnable example — mock data ke saath
  
  RUN KARO:
      pip install fastapi uvicorn
      python main.py
  
  BROWSER MEIN OPEN KARO:
      http://127.0.0.1:8000/docs     <- Swagger UI (Interactive!)
      http://127.0.0.1:8000/redoc    <- ReDoc UI
      http://127.0.0.1:8000/products <- Direct API
=============================================================
"""

# ──────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────
from fastapi import FastAPI, Query, HTTPException  # FastAPI core
from pydantic import BaseModel                     # Data validation ke liye
from typing import Optional, List                  # Type hints ke liye
from enum import Enum                              # Whitelist ke liye
import math                                        # Ceil function ke liye


# ──────────────────────────────────────────────
# APP INITIALIZE KARO
# ──────────────────────────────────────────────
app = FastAPI(
    title="Products API",
    description="FastAPI — Sorting, Filtering, Pagination, Searching — Complete Demo",
    version="1.0.0",
)


# ──────────────────────────────────────────────
# MOCK DATABASE
# Real project mein yeh PostgreSQL/MySQL hoga
# Abhi ke liye — Python list hi database hai!
# ──────────────────────────────────────────────
PRODUCTS_DB = [
    {"id": 1,  "name": "Nike Air Max 270",        "price": 8999,   "category": "shoes",       "brand": "Nike",    "rating": 4.5, "in_stock": True},
    {"id": 2,  "name": "Adidas Ultraboost 22",     "price": 12499,  "category": "shoes",       "brand": "Adidas",  "rating": 4.7, "in_stock": True},
    {"id": 3,  "name": "Puma Running Shoes",       "price": 4999,   "category": "shoes",       "brand": "Puma",    "rating": 4.0, "in_stock": True},
    {"id": 4,  "name": "Salomon Trail Runner",     "price": 7999,   "category": "shoes",       "brand": "Salomon", "rating": 4.6, "in_stock": False},
    {"id": 5,  "name": "iPhone 15 Pro",            "price": 134900, "category": "electronics", "brand": "Apple",   "rating": 4.8, "in_stock": True},
    {"id": 6,  "name": "Samsung Galaxy S24",       "price": 74999,  "category": "electronics", "brand": "Samsung", "rating": 4.6, "in_stock": True},
    {"id": 7,  "name": "OnePlus 12",               "price": 64999,  "category": "electronics", "brand": "OnePlus", "rating": 4.4, "in_stock": True},
    {"id": 8,  "name": "boAt Airdopes 141",        "price": 1299,   "category": "electronics", "brand": "boAt",    "rating": 4.1, "in_stock": True},
    {"id": 9,  "name": "MacBook Pro M3",           "price": 199900, "category": "electronics", "brand": "Apple",   "rating": 4.9, "in_stock": False},
    {"id": 10, "name": "Levi's 511 Slim Jeans",    "price": 3499,   "category": "clothing",    "brand": "Levi's",  "rating": 4.2, "in_stock": True},
    {"id": 11, "name": "H&M Oversized T-Shirt",    "price": 699,    "category": "clothing",    "brand": "H&M",     "rating": 3.8, "in_stock": True},
    {"id": 12, "name": "Zara Casual Shirt",        "price": 2499,   "category": "clothing",    "brand": "Zara",    "rating": 4.0, "in_stock": True},
    {"id": 13, "name": "Nike Dri-FIT T-Shirt",     "price": 1999,   "category": "clothing",    "brand": "Nike",    "rating": 4.3, "in_stock": True},
    {"id": 14, "name": "Adidas Track Pants",       "price": 2799,   "category": "clothing",    "brand": "Adidas",  "rating": 4.1, "in_stock": False},
    {"id": 15, "name": "Apple Watch Series 9",     "price": 41900,  "category": "electronics", "brand": "Apple",   "rating": 4.7, "in_stock": True},
]


# ──────────────────────────────────────────────
# ENUMS — Sorting ke liye Whitelist
#
# SECURITY: User koi bhi field naam pass na kar sake
 # Agar direct string sort mein use karein to SQL Injection ho sakta hai
# Isliye ENUM use karte hain — sirf yahi valid values hain!
# ──────────────────────────────────────────────
class SortField(str, Enum):
    """
    Sirf yahi 4 fields pe sort allowed hai.
    Koi bhi aur field pass karne pe FastAPI automatically 422 error dega.

    Example:
        ?sort_by=price    OK - Valid
        ?sort_by=name     OK - Valid
        ?sort_by=password ERROR - 422 Unprocessable Entity
    """
    name     = "name"     # Alphabetically sort karo
    price    = "price"    # Price ke basis pe sort karo
    rating   = "rating"   # Rating ke basis pe sort karo
    id       = "id"       # ID ke basis pe sort karo (default order)

# class SortField(str , Enum ):
#     id : int 
#     name: str
#     price : float
#     category : str
#     brand : str
#     rating : float 
#     in_stiock : bool 
    
class SortOrder(str, Enum):
    """
    Sort direction — sirf 2 valid values.

    Example:
        ?order=asc   OK - Valid (A->Z, 0->9)
        ?order=desc  OK - Valid (Z->A, 9->0)
        ?order=up    ERROR - 422 Error
    """
    asc  = "asc"   # Ascending: 1, 2, 3 ya A, B, C
    desc = "desc"  # Descending: 3, 2, 1 ya C, B, A


# ──────────────────────────────────────────────
# PYDANTIC MODELS — Response Schema
#
# Yeh define karta hai API ka response kaisa dikhega.
# Pydantic automatically validate bhi karta hai data.
# ──────────────────────────────────────────────
class Product(BaseModel):
    """Ek product ka schema"""
    id:       int
    name:     str
    price:    float
    category: str
    brand:    str
    rating:   float
    in_stock: bool


class PaginationMeta(BaseModel):
    """Pagination ki metadata — frontend ko yeh chahiye hoti hai"""
    total:       int    # Total kitne records hain (after filtering)
    page:        int    # Current page number
    limit:       int    # Items per page
    total_pages: int    # Total pages available
    has_next:    bool   # Kya aur page hai?
    has_prev:    bool   # Kya pichla page hai?
    showing:     str    # Human-readable: "Items 1-10 of 47"


class ProductListResponse(BaseModel):
    """Final response — data + meta + applied filters"""
    data:    List[Product]   # Actual products
    meta:    PaginationMeta  # Pagination info
    applied: dict            # Kaunse filters/sort apply hue


# ──────────────────────────────────────────────
# ROOT ENDPOINT — Just a welcome message
# ──────────────────────────────────────────────
@app.get("/", tags=["Info"])
async def root():
    """Welcome endpoint."""
    return {
        "message": "FastAPI Demo — Sorting, Filtering, Pagination, Searching",
        "docs":    "http://127.0.0.1:8000/docs",
        "endpoints": {
            "list_products": "GET /products",
            "get_one":       "GET /products/{id}",
            "categories":    "GET /categories",
            "brands":        "GET /brands",
            "stats":         "GET /stats",
        }
    }


# ──────────────────────────────────────────────
# MAIN ENDPOINT — Sab kuch ek saath!
#
# URL format:
# GET /products
#   ?q=nike                 <- search
#   &category=shoes         <- filter by category
#   &brand=Nike             <- filter by brand
#   &min_price=1000         <- filter by min price
#   &max_price=10000        <- filter by max price
#   &in_stock=true          <- filter in-stock only
#   &sort_by=price          <- sort field
#   &order=desc             <- sort direction
#   &page=1                 <- page number
#   &limit=5                <- items per page
# ──────────────────────────────────────────────
@app.get(
    "/products",
    response_model=ProductListResponse,
    tags=["Products"],
    summary="List Products — with Search, Filter, Sort, Paginate",
)
async def list_products(

    # ══════════════════════════════════════
    # SEARCH PARAMETER
    # ══════════════════════════════════════
    q: Optional[str] = Query(
        default=None,
        min_length=2,    # Minimum 2 characters — "a" se search useless hai
        max_length=100,  # Maximum 100 characters — ReDoS attack se bachao
        description="Search karo product name mein (case-insensitive). Example: nike, running, apple",
        example="nike",
    ),

    # ══════════════════════════════════════
    # FILTER PARAMETERS
    # ══════════════════════════════════════
    category: Optional[str] = Query(
        default=None,
        description="Category filter: shoes | electronics | clothing",
        example="shoes",
    ),

    brand: Optional[str] = Query(
        default=None,
        description="Brand filter: Nike, Adidas, Apple, Samsung, etc.",
        example="Nike",
    ),

    min_price: Optional[float] = Query(
        default=None,
        ge=0,            # ge = greater than or equal to. Price 0 se kam nahi ho sakta!
        description="Minimum price filter (inclusive). Example: 1000",
        example=1000,
    ),

    max_price: Optional[float] = Query(
        default=None,
        ge=0,            # Max price bhi 0 se kam nahi ho sakta
        description="Maximum price filter (inclusive). Example: 10000",
        example=10000,
    ),

    in_stock: Optional[bool] = Query(
        default=None,
        description="Sirf in-stock products? true ya false",
        example=True,
    ),
    
    
    

    # ══════════════════════════════════════
    # SORT PARAMETERS
    # ══════════════════════════════════════
    sort_by: SortField = Query(
        default=SortField.id,
        description="Kaunse field pe sort karna hai? name | price | rating | id",
    ),

    order: SortOrder = Query(
        default=SortOrder.asc,
        description="Sort order: asc (low to high) ya desc (high to low)",
    ),

    # ══════════════════════════════════════
    # PAGINATION PARAMETERS
    # ══════════════════════════════════════
    page: int = Query(
        default=1,
        ge=1,            # Page number 1 se start hota hai (0 nahi!)
        description="Page number (1 se start). Default: 1",
        example=1,
    ),

    limit: int = Query(
        default=5,
        ge=1,            # Minimum 1 item per page
        le=100,          # SECURITY: Maximum 100 items — DoS attack se bachao!
        description="Items per page (max 100). Default: 5",
        example=5,
    ),
):
    # ──────────────────────────────
    # STEP 0: Cross-field Validation
    # Sirf Query params mein validation nahi hoti
    # Kuch validations multiple fields ke beech hoti hain
    # ──────────────────────────────
    if min_price is not None and max_price is not None:
        if min_price > max_price:
            # 400 = Bad Request — client ne galat data bheja
            raise HTTPException(
                status_code=400,
                detail=f"min_price ({min_price}) max_price ({max_price}) se bada nahi ho sakta!"
            )

    # ──────────────────────────────
    # STEP 1: Full dataset se start karo
    # Real DB mein: db.query(Product) hoga
    # ──────────────────────────────
    results = PRODUCTS_DB.copy()  # Original data ko modify nahi karte

    # ──────────────────────────────
    # STEP 2: SEARCH APPLY KARO
    #
    # ILIKE simulation (case-insensitive contains search)
    # Real SQL: WHERE LOWER(name) LIKE LOWER('%nike%')
    #
    # 'q' parameter agar diya hai tabhi search karo
    # ──────────────────────────────
    if q:
        q_lower = q.strip().lower()  # Lowercase mein convert karo comparison ke liye
        results = [
            product for product in results
            if q_lower in product["name"].lower()
        ]

    # ──────────────────────────────
    # STEP 3: FILTERS APPLY KARO
    #
    # Har filter ek alag condition hai.
    # Sab conditions AND hoti hain (sab true hona chahiye)
    # ──────────────────────────────

    # Category filter: Exact match (case-insensitive)
    # Real SQL: WHERE LOWER(category) = LOWER('shoes')
    if category:
        results = [p for p in results if p["category"].lower() == category.lower()]

    # Brand filter: Exact match (case-insensitive)
    # Real SQL: WHERE LOWER(brand) = LOWER('Nike')
    if brand:
        results = [p for p in results if p["brand"].lower() == brand.lower()]

    # Min price filter: Greater than or equal
    # Real SQL: WHERE price >= 1000
    if min_price is not None:
        results = [p for p in results if p["price"] >= min_price]

    # Max price filter: Less than or equal
    # Real SQL: WHERE price <= 10000
    if max_price is not None:
        results = [p for p in results if p["price"] <= max_price]

    # In-stock filter: Boolean exact match
    # Real SQL: WHERE in_stock = TRUE
    # None check zaroori hai! (False bhi valid value hai)
    if in_stock is not None:
        results = [p for p in results if p["in_stock"] == in_stock]

    # ──────────────────────────────
    # STEP 4: SORT KARO
    #
    # sort_by.value -> "price" / "name" / "rating" / "id"
    # reverse=True  -> Descending (9->1, Z->A)
    # reverse=False -> Ascending  (1->9, A->Z)
    #
    # Real SQL: ORDER BY price DESC
    # ──────────────────────────────
    results = sorted(
        results,
        key=lambda product: product[sort_by.value],  # Kaunse field pe sort karo
        reverse=(order == SortOrder.desc)             # Direction decide karo
    )

    # ──────────────────────────────
    # STEP 5: TOTAL COUNT KARO
    # Pagination OFFSET/LIMIT se PEHLE count karo!
    # Warna hamesha current page ke items count milenge
    # ──────────────────────────────
    total = len(results)                           # Filter ke baad total
    total_pages = max(1, math.ceil(total / limit)) # Kitne pages banenge?

    # Edge case: Agar requested page exist nahi karta
    if total > 0 and page > total_pages:
        raise HTTPException(
            status_code=404,
            detail=f"Page {page} exist nahi karta. Total pages sirf {total_pages} hain."
        )

    # ──────────────────────────────
    # STEP 6: PAGINATE KARO (LIMIT + OFFSET)
    #
    # Formula: offset = (page - 1) * limit
    # Page 1 -> offset=0  -> items[0:5]
    # Page 2 -> offset=5  -> items[5:10]
    # Page 3 -> offset=10 -> items[10:15]
    #
    # Real SQL: LIMIT 5 OFFSET 10
    # ──────────────────────────────
    offset    = (page - 1) * limit         # Kitne items skip karne hain
    paginated = results[offset : offset + limit]  # Python list slicing = SQL LIMIT/OFFSET

    # ──────────────────────────────
    # STEP 7: RESPONSE BANAO
    # Data + Pagination metadata + Applied filters info
    # ──────────────────────────────
    first_item = offset + 1 if total > 0 else 0
    last_item  = offset + len(paginated)
    showing    = f"Items {first_item}-{last_item} of {total}"

    return {
        "data": paginated,

        # Pagination metadata — frontend ko yeh chahiye hoti hai
        "meta": {
            "total":       total,
            "page":        page,
            "limit":       limit,
            "total_pages": total_pages,
            "has_next":    page < total_pages,
            "has_prev":    page > 1,
            "showing":     showing,
        },

        # Applied filters — debugging ke liye useful
        "applied": {
            "search":    q,
            "category":  category,
            "brand":     brand,
            "min_price": min_price,
            "max_price": max_price,
            "in_stock":  in_stock,
            "sort_by":   sort_by.value,
            "order":     order.value,
        },
    }


# ──────────────────────────────────────────────
# BONUS ENDPOINT: Single Product by ID
# ──────────────────────────────────────────────
@app.get("/products/{product_id}", response_model=Product, tags=["Products"])
async def get_product(product_id: int):
    """
    Ek specific product detail lao by ID.
    Example: GET /products/5  -> iPhone 15 Pro
    """
    product = next(
        (p for p in PRODUCTS_DB if p["id"] == product_id),
        None  # Agar nahi mila to None
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product ID {product_id} nahi mila."
        )

    return product


# ──────────────────────────────────────────────
# BONUS ENDPOINT: Available Categories
# ──────────────────────────────────────────────
@app.get("/categories", tags=["Helpers"])
async def get_categories():
    """Sabhi available categories ki list. Filtering ke liye valid values yahan dekho."""
    categories = sorted(set(p["category"] for p in PRODUCTS_DB))
    return {
        "categories": categories,
        "count": len(categories),
        "usage": "GET /products?category=shoes"
    }


# ──────────────────────────────────────────────
# BONUS ENDPOINT: Available Brands
# ──────────────────────────────────────────────
@app.get("/brands", tags=["Helpers"])
async def get_brands():
    """Sabhi available brands ki list. Brand filter ke liye valid values yahan dekho."""
    brands = sorted(set(p["brand"] for p in PRODUCTS_DB))
    return {
        "brands": brands,
        "count": len(brands),
        "usage": "GET /products?brand=Nike"
    }


# ──────────────────────────────────────────────
# BONUS ENDPOINT: Stats
# ──────────────────────────────────────────────
@app.get("/stats", tags=["Helpers"])
async def get_stats():
    """Database ka quick overview"""
    prices = [p["price"] for p in PRODUCTS_DB]
    return {
        "total_products": len(PRODUCTS_DB),
        "in_stock":       sum(1 for p in PRODUCTS_DB if p["in_stock"]),
        "out_of_stock":   sum(1 for p in PRODUCTS_DB if not p["in_stock"]),
        "price_range":    {"min": min(prices), "max": max(prices)},
        "avg_price":      round(sum(prices) / len(prices), 2),
        "categories":     len(set(p["category"] for p in PRODUCTS_DB)),
        "brands":         len(set(p["brand"] for p in PRODUCTS_DB)),
    }


# ──────────────────────────────────────────────
# DIRECT RUN SUPPORT
# python main.py -> uvicorn automatically start hoga
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*55)
    print("  FastAPI Server Starting...")
    print("="*55)
    print("  Swagger UI  -> http://127.0.0.1:8000/docs")
    print("  ReDoc       -> http://127.0.0.1:8000/redoc")
    print("  API Root    -> http://127.0.0.1:8000/")
    print("="*55)
    print("\n  Kuch example URLs try karo:\n")
    print("  Sab products:           /products")
    print("  Search:                 /products?q=nike")
    print("  Filter by category:     /products?category=shoes")
    print("  Price range:            /products?min_price=1000&max_price=10000")
    print("  Sort by price desc:     /products?sort_by=price&order=desc")
    print("  Page 2, 3 items:        /products?page=2&limit=3")
    print("  Sab ek saath:           /products?q=a&category=shoes&sort_by=price&order=desc&page=1&limit=3")
    print("  Stats:                  /stats")
    print("\n  Server band karne ke liye: CTRL + C\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)