import pandas as pd
from typing import Type
from pydantic import BaseModel, create_model
from typing import List, Optional



class FormData(BaseModel):
    model : str
    fields: list
    url: str
    query: str
    
    
class FinalResult(BaseModel):
    df: Optional[pd.DataFrame] = None
    markdown: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_cost: Optional[float] = None
    timestamp: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    
def create_dynamic_listing_model(field_names: List[str]) -> Type[BaseModel]:
    """
    Dynamically creates a Pydantic model based on provided fields.
    field_name is a list of names of the fields to extract from the markdown.
    """
    # Create field definitions using aliases for Field parameters
    field_definitions = {field: (str, ...) for field in field_names}
    # Dynamically create the model with all field
    return create_model('DynamicListingModel', **field_definitions)

def create_listings_container_model(listing_model: Type[BaseModel]) -> Type[BaseModel]:
    """
    Create a container model that holds a list of the given listing model.
    """
    return create_model('DynamicListingsContainer', listings=(List[listing_model], ...))

