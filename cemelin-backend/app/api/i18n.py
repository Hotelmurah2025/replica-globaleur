from fastapi import APIRouter, HTTPException
from typing import Dict, List
from pydantic import BaseModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Simple in-memory storage for translations
translations = {
    "en": {
        "common": {
            "search": "Search",
            "destinations": "Destinations",
            "plans": "Plans",
            "contact": "Contact",
            "login": "Login",
            "register": "Register",
            "profile": "Profile",
            "logout": "Logout",
            "loading": "Loading...",
            "error": "An error occurred",
            "success": "Success",
            "submit": "Submit",
            "cancel": "Cancel",
            "save": "Save",
            "delete": "Delete",
            "edit": "Edit"
        },
        "contact": {
            "form": {
                "name": "Name",
                "email": "Email",
                "subject": "Subject",
                "message": "Message",
                "phone": "Phone (optional)",
                "submit": "Send Message",
                "success": "Thank you for your message. We will respond shortly.",
                "error": "An error occurred while sending your message"
            }
        },
        "destinations": {
            "search": {
                "placeholder": "Search for destinations...",
                "noResults": "No destinations found",
                "searching": "Searching...",
                "location": "Near current location"
            },
            "details": {
                "overview": "Overview",
                "activities": "Activities",
                "reviews": "Reviews",
                "location": "Location",
                "addToTrip": "Add to Trip",
                "price": "Price Level",
                "rating": "Rating",
                "website": "Website",
                "phone": "Phone",
                "hours": "Opening Hours",
                "address": "Address"
            }
        },
        "trips": {
            "create": "Create Trip",
            "edit": "Edit Trip",
            "delete": "Delete Trip",
            "title": "Trip Title",
            "description": "Description",
            "startDate": "Start Date",
            "endDate": "End Date",
            "destinations": "Destinations",
            "addDestination": "Add Destination",
            "removeDestination": "Remove Destination",
            "dayNumber": "Day",
            "duration": "Duration",
            "notes": "Notes",
            "visibility": {
                "public": "Public",
                "private": "Private"
            },
            "errors": {
                "invalidDates": "End date cannot be before start date",
                "notFound": "Trip not found",
                "unauthorized": "You are not authorized to access this trip"
            }
        },
        "auth": {
            "login": {
                "title": "Login",
                "email": "Email",
                "password": "Password",
                "submit": "Login",
                "forgotPassword": "Forgot Password?",
                "noAccount": "Don't have an account?",
                "register": "Register here"
            },
            "register": {
                "title": "Register",
                "name": "Full Name",
                "email": "Email",
                "password": "Password",
                "confirmPassword": "Confirm Password",
                "submit": "Register",
                "hasAccount": "Already have an account?",
                "login": "Login here"
            }
        }
    },
    "id": {
        "common": {
            "search": "Cari",
            "destinations": "Destinasi",
            "plans": "Rencana",
            "contact": "Kontak",
            "login": "Masuk",
            "register": "Daftar",
            "profile": "Profil",
            "logout": "Keluar",
            "loading": "Memuat...",
            "error": "Terjadi kesalahan",
            "success": "Berhasil",
            "submit": "Kirim",
            "cancel": "Batal",
            "save": "Simpan",
            "delete": "Hapus",
            "edit": "Ubah"
        },
        "contact": {
            "form": {
                "name": "Nama",
                "email": "Email",
                "subject": "Subjek",
                "message": "Pesan",
                "phone": "Telepon (opsional)",
                "submit": "Kirim Pesan",
                "success": "Terima kasih atas pesan Anda. Kami akan segera merespons.",
                "error": "Terjadi kesalahan saat mengirim pesan Anda"
            }
        },
        "destinations": {
            "search": {
                "placeholder": "Cari destinasi...",
                "noResults": "Destinasi tidak ditemukan",
                "searching": "Mencari...",
                "location": "Dekat lokasi saat ini"
            },
            "details": {
                "overview": "Ikhtisar",
                "activities": "Aktivitas",
                "reviews": "Ulasan",
                "location": "Lokasi",
                "addToTrip": "Tambahkan ke Perjalanan",
                "price": "Tingkat Harga",
                "rating": "Penilaian",
                "website": "Situs Web",
                "phone": "Telepon",
                "hours": "Jam Buka",
                "address": "Alamat"
            }
        },
        "trips": {
            "create": "Buat Perjalanan",
            "edit": "Ubah Perjalanan",
            "delete": "Hapus Perjalanan",
            "title": "Judul Perjalanan",
            "description": "Deskripsi",
            "startDate": "Tanggal Mulai",
            "endDate": "Tanggal Selesai",
            "destinations": "Destinasi",
            "addDestination": "Tambah Destinasi",
            "removeDestination": "Hapus Destinasi",
            "dayNumber": "Hari",
            "duration": "Durasi",
            "notes": "Catatan",
            "visibility": {
                "public": "Publik",
                "private": "Pribadi"
            },
            "errors": {
                "invalidDates": "Tanggal selesai tidak boleh sebelum tanggal mulai",
                "notFound": "Perjalanan tidak ditemukan",
                "unauthorized": "Anda tidak memiliki akses ke perjalanan ini"
            }
        },
        "auth": {
            "login": {
                "title": "Masuk",
                "email": "Email",
                "password": "Kata Sandi",
                "submit": "Masuk",
                "forgotPassword": "Lupa Kata Sandi?",
                "noAccount": "Belum punya akun?",
                "register": "Daftar di sini"
            },
            "register": {
                "title": "Daftar",
                "name": "Nama Lengkap",
                "email": "Email",
                "password": "Kata Sandi",
                "confirmPassword": "Konfirmasi Kata Sandi",
                "submit": "Daftar",
                "hasAccount": "Sudah punya akun?",
                "login": "Masuk di sini"
            }
        }
    }
}

class TranslationResponse(BaseModel):
    locale: str
    translations: Dict
    timestamp: datetime

class LocaleInfo(BaseModel):
    code: str
    name: str
    native_name: str

@router.get("/translations/{locale}", response_model=TranslationResponse)
async def get_translations(locale: str):
    """Get translations for a specific locale"""
    if locale not in translations:
        raise HTTPException(
            status_code=404,
            detail=f"Translations for locale '{locale}' not found"
        )
    
    return TranslationResponse(
        locale=locale,
        translations=translations[locale],
        timestamp=datetime.utcnow()
    )

@router.get("/locales", response_model=List[LocaleInfo])
async def get_available_locales():
    """Get list of available locales with their details"""
    locales = [
        LocaleInfo(
            code="en",
            name="English",
            native_name="English"
        ),
        LocaleInfo(
            code="id",
            name="Indonesian",
            native_name="Bahasa Indonesia"
        )
    ]
    return locales

@router.get("/translations", response_model=Dict[str, Dict])
async def get_all_translations():
    """Get all available translations"""
    return translations
