# How to Get OpenRouter API Key (FREE)

## Why OpenRouter?

OpenRouter provides access to multiple AI models, including **FREE** models like Meta's Llama. This is better than Google Gemini because:
- ✅ **Completely FREE** models available
- ✅ No credit card required
- ✅ Easy to set up
- ✅ Multiple model options

## Steps to Get Your API Key:

### 1. Sign Up for OpenRouter

1. Go to https://openrouter.ai/
2. Click "Sign In" or "Get Started"
3. Sign up with:
   - GitHub account (recommended)
   - Google account
   - Or email

### 2. Get Your API Key

1. After signing in, go to https://openrouter.ai/keys
2. Click "Create Key"
3. Give it a name (e.g., "Graph Learning Platform")
4. Click "Create"
5. **Copy the API key** (starts with `sk-or-v1-...`)

### 3. Add to Vercel Environment Variables

1. Go to your Vercel project dashboard
2. Click "Settings" → "Environment Variables"
3. Add a new variable:
   - **Name:** `OPENROUTER_API_KEY`
   - **Value:** (paste your API key from step 2)
4. Click "Save"
5. **Redeploy** your project for changes to take effect

### 4. Test Your Setup

After redeploying:
1. Go to your dashboard
2. Upload a PDF
3. Click "Generate Graph"
4. Wait 30-60 seconds
5. The graph should appear!

## Free Models Available

The code is configured to use: `meta-llama/llama-3.2-3b-instruct:free`

Other free options you can try (edit `backend/ai_engine.py`):
- `meta-llama/llama-3.2-1b-instruct:free`
- `google/gemma-2-9b-it:free`
- `mistralai/mistral-7b-instruct:free`

## Troubleshooting

### "API Key missing" error
- Make sure you added `OPENROUTER_API_KEY` to Vercel environment variables
- Redeploy after adding the variable

### "Rate limit exceeded"
- Free models have rate limits
- Wait a few minutes and try again
- Or upgrade to a paid plan on OpenRouter (very cheap)

### Processing takes too long
- Free models are slower than paid ones
- Be patient, it can take 30-60 seconds
- Check Vercel function logs for progress

## Cost Information

**FREE tier includes:**
- ✅ Llama 3.2 models (1B and 3B)
- ✅ Gemma 2 9B
- ✅ Mistral 7B
- ✅ And more!

**Paid models** (if you want faster/better results):
- GPT-4: ~$0.03 per 1K tokens
- Claude 3: ~$0.015 per 1K tokens
- Much cheaper than using APIs directly!

## Links

- OpenRouter Website: https://openrouter.ai/
- API Keys: https://openrouter.ai/keys
- Model Pricing: https://openrouter.ai/models
- Documentation: https://openrouter.ai/docs

## Need Help?

If you have issues:
1. Check Vercel function logs
2. Verify API key is set correctly
3. Make sure you redeployed after adding the key
4. Check OpenRouter dashboard for usage/errors
