import os, uuid, datetime, logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
try:
    from motor.motor_asyncio import AsyncIOMotorClient
except Exception:
    AsyncIOMotorClient = None

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Empire Core - Voice AI Agent (Ultra Demo)")

# Simple DB wrapper: try MongoDB if URI provided, else fallback to in-memory store (demo safe)
MONGODB_URI = os.getenv('MONGODB_URI')
db = {"users": [], "agents": [], "bookings": []}
mongo_client = None
if MONGODB_URI and AsyncIOMotorClient is not None:
    try:
        mongo_client = AsyncIOMotorClient(MONGODB_URI)
        db_conn = mongo_client.get_default_database()
        logging.info("Connected to MongoDB Atlas")
    except Exception as e:
        logging.warning("MongoDB connect failed, using in-memory store. Error: %s", e)

class BookRequest(BaseModel):
    name: str
    phone: str
    requested: Optional[str] = None

@app.get('/health', response_class=PlainTextResponse)
async def health():
    return "OK - Empire Core (FastAPI)"

@app.post('/book')
async def book(req: BookRequest):
    booking_id = "BK-" + uuid.uuid4().hex[:8]
    record = {"id": booking_id, "name": req.name, "phone": req.phone, "requested": req.requested, "created": datetime.datetime.utcnow().isoformat()}
    if mongo_client:
        try:
            await db_conn.bookings.insert_one(record)
        except Exception as e:
            logging.warning("Mongo insert failed: %s", e)
            db['bookings'].append(record)
    else:
        db['bookings'].append(record)
    confirm_text = f"Booked {req.name} at {req.requested or 'client requested time'} (id {booking_id})"
    return JSONResponse({'status':'ok','booking_id':booking_id,'confirm_text':confirm_text})

@app.post('/payments/webhook')
async def payments_webhook(request: Request):
    # Receives webhook from LemonSqueezy or payment provider. Validate signature in production.
    try:
        payload = await request.json()
    except Exception:
        payload = await request.body()
    # For demo: log and return
    logging.info("Payment webhook received: %s", str(payload)[:400])
    return JSONResponse({'received': True})

@app.post('/twilio-voice')
async def twilio_voice(request: Request):
    # Minimal TwiML response for demo. Twilio will POST call data to this endpoint.
    # For production, use twilio.twiml.VoiceResponse to build safe TwiML.
    twiml = '<?xml version="1.0" encoding="UTF-8"?><Response><Say voice="alice">Hello, connecting you to the appointment assistant. For demo, this is a test response.</Say></Response>'
    return PlainTextResponse(content=twiml, media_type='application/xml')

@app.get('/users')
async def get_users():
    if mongo_client:
        try:
            items = await db_conn.users.find().to_list(100)
            return items
        except Exception as e:
            return db['users']
    return db['users']

@app.post('/users')
async def create_user(request: Request):
    payload = await request.json()
    payload['id'] = uuid.uuid4().hex[:8]
    if mongo_client:
        try:
            await db_conn.users.insert_one(payload)
        except Exception as e:
            db['users'].append(payload)
    else:
        db['users'].append(payload)
    return JSONResponse({'status':'ok','user':payload})

