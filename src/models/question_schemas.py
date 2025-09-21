from pydantic import BaseModel
from typing import List, Optional


class ProfileSchema(BaseModel):
    name: str
    location: str
    craft_type: str


class ListingSchema(BaseModel):
    product_name: str
    craft_details: str


class FeedSchema(BaseModel):
    product_name: str


class FullListingSchema(BaseModel):
    seo_title: str
    description: str
    category: str
    profit: dict
    market_price: str
    metafields: str
    product_type: str
    tags: List[str]


class ListingInputSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    photo: Optional[str] = None  # filename, URL, or base64 string
    price: Optional[str] = None
    cost: Optional[str] = None
