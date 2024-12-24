from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from app.deps import get_db
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class ContactMessage(BaseModel):
    name: constr(min_length=2, max_length=100)
    email: EmailStr
    subject: constr(min_length=3, max_length=200)
    message: constr(min_length=10, max_length=2000)
    phone: Optional[constr(regex=r'^\+?[1-9]\d{1,14}$')] = None
    locale: str = "en"  # Default to English

class ContactResponse(BaseModel):
    message: str
    ticket_id: str

router = APIRouter()

def log_contact_message(message: ContactMessage, ticket_id: str):
    """Log contact form submission for tracking"""
    try:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "ticket_id": ticket_id,
            "name": message.name,
            "email": message.email,
            "subject": message.subject,
            "phone": message.phone,
            "message": message.message,
            "locale": message.locale
        }
        logger.info(f"Contact form submission: {log_entry}")
        
        # In a real application, you might:
        # 1. Send an email to support staff
        # 2. Create a ticket in a ticketing system
        # 3. Store in a database
        # 4. Send confirmation email to user
        
    except Exception as e:
        logger.error(f"Error logging contact message: {e}")

@router.post("/", response_model=ContactResponse)
async def submit_contact_form(
    message: ContactMessage,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Submit a contact form message
    
    - Validates input fields
    - Generates a ticket ID
    - Logs the message (and would typically send emails/create tickets in production)
    - Returns a success response with tracking ID in the user's preferred language
    """
    try:
        # Generate a simple ticket ID
        ticket_id = f"TKT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Log the message in the background
        background_tasks.add_task(log_contact_message, message, ticket_id)
        
        # Get response message based on locale
        success_messages = {
            "en": "Thank you for your message. We will respond shortly.",
            "id": "Terima kasih atas pesan Anda. Kami akan segera merespons."
        }
        
        response_message = success_messages.get(
            message.locale,
            success_messages["en"]  # Fallback to English
        )
        
        return ContactResponse(
            message=response_message,
            ticket_id=ticket_id
        )
        
    except Exception as e:
        logger.error(f"Error processing contact form: {e}")
        error_messages = {
            "en": "An error occurred while processing your message",
            "id": "Terjadi kesalahan saat memproses pesan Anda"
        }
        error_message = error_messages.get(message.locale, error_messages["en"])
        raise HTTPException(status_code=500, detail=error_message)
