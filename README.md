# Empire Ultra Bundle — Voice AI Agent Full Starter (Zero-cost deploy)

This bundle gets you from zero → deployed demo quickly using free tiers:
- FastAPI backend (Render-ready)
- Simple frontend (Vercel-ready)
- Twilio inbound voice webhook (demo response)
- LemonSqueezy / Payments webhook placeholder
- MongoDB Atlas optional integration (free tier)
- Deployment configs + step-by-step deploy instructions

## What's included
- `backend/` — FastAPI app with endpoints:
    - `/health` — health check
    - `/book` — create demo booking (returns fake booking id)
    - `/payments/webhook` — receive LemonSqueezy webhooks (placeholder)
    - `/twilio-voice` — Twilio voice webhook (returns TwiML)
    - `/users`, `/agents` — simple CRUD placeholders
- `frontend/` — static landing page + simple dashboard + payment button placeholder
- `render.yaml` — Render service definition (edit repo field)
- `vercel.json` — Vercel static config
- `.env.example` — environment variables to set

## Quick deploy (5–15 minutes)
1. Create a GitHub repo (e.g., `empire-core`) and push this bundle.
2. Create free accounts: Render, Vercel, MongoDB Atlas, Lemon Squeezy, Twilio (trial).
3. Deploy backend to Render:
   - Connect your GitHub repo, branch `main`
   - Set environment variables (see `.env.example`)
   - Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
4. Deploy frontend to Vercel (import project — it will auto-deploy the `frontend/` folder).
5. Create a LemonSqueezy product and copy its product URL into `frontend/index.html` (replace the placeholder).
6. Provision a Twilio number (trial) and point its Voice webhook to `https://<render-url>/twilio-voice`.

## Test the demo
- Visit the frontend landing page on Vercel and click "Book Pilot" (payment link should go to LemonSqueezy product).
- Call the Twilio number — Twilio will POST to `/twilio-voice` and the endpoint will respond with a demo message.
- Use `/book` to simulate bookings.

## Notes & Next steps
- This starter is intentionally minimal to keep things free and simple. After pilots convert to revenue, upgrade TTS/StT and move to paid production plans (ElevenLabs, Twilio production tiers).
- Add your real Google Calendar integration to `/book` to create events.

Good luck — deploy and start collecting dollars. Say "I'M DEPLOYING" when you begin and I'll give exact copy-paste commands for each platform.
