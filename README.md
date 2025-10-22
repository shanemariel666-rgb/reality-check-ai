# Reality Check AI — Professional PWA

## What this contains
- Flask API (api/main.py) that accepts file or text and uses Replicate + Hugging Face.
- Frontend (templates/index.html) and styling (static/style.css).
- Static assets folder (static/logo.png, background optional).
- Vercel configuration (vercel.json).

## Required environment variables (set on your host)
- REPLICATE_API_TOKEN       (your replicate.com token)
- REPLICATE_IMAGE_MODEL     (Replicate model *version id* for images)
- REPLICATE_VIDEO_MODEL     (Replicate model *version id* for videos) — optional
- HUGGINGFACE_API_KEY       (your Hugging Face token)
- HF_TEXT_MODEL            (optional; default: openai-community/roberta-base-openai-detector)

## Deploy (Vercel)
1. Push this repo to GitHub.
2. Go to https://vercel.com/new and import the repository.
3. In Vercel project Settings → Environment Variables, add the keys above.
4. Deploy. Vercel will build and give you the site URL.

## Run locally
1. cd api
2. python -m venv venv && source venv/bin/activate
3. pip install -r requirements.txt
4. export REPLICATE_API_TOKEN="r8_xxx"
   export HUGGINGFACE_API_KEY="hf_xxx"
   export REPLICATE_IMAGE_MODEL="owner/model@sha256..."
5. python main.py
6. Open http://127.0.0.1:5000
