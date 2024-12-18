from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError


class NewUser(BaseModel):
    first_name:str = Field(min_length=2)
    last_name:str = Field(min_length=2)
    age:int = Field(ge=18, le=120)
    email:EmailStr
    height:int = Field(ge=50, le=250, description="Height in centimetres, between 50 and 250")

    @field_validator('email')
    def validate_email(cls,email):
        if "@example" in email:
            raise ValueError("Enter a real email address")
        return email

    model_config = {
        "json_schema_extra": {
            "example":
                {
                    "first_name": "Lola",
                    "last_name": "Afam",
                    "age": 25,
                    "email": "alola@gmail.com",
                    "height": 180
                }

        }}
