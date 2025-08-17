Deploy notes:
- Push to GitHub main branch.
- On Render: create a new web service, connect GitHub, and select repo + branch.
  - Build Command: pip install -r backend/requirements.txt
  - Start Command: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
- On Vercel: import project and set output directory to /frontend
- Replace the placeholder LEMONSQUEEZY_PRODUCT_URL in frontend/index.html with your product URL
- Point Twilio phone number's Voice webhook to https://<render-url>/twilio-voice
