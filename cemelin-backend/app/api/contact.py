from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter()

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

@router.post("/")
def submit_contact_form(form_data: ContactForm):
    # In a real application, this would send an email or store the message
    # For now, we'll just return a success message
    return {"status": "success", "message": "Thank you for your message"}
