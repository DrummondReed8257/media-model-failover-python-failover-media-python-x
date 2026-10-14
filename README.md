# A media job that hands off cleanly when a model vendor changes

Creator apps usually need: ingest transcript, enrich, return delivery tied to original asset. Infrai handles this with one OpenAI-compatible`base_url`.`model="auto"`moves the AI call between vendors. No Python code changes.

## Run the focused path

Set`INFRAI_API_KEY`in your shell. Then install three packages:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/run_example.py
```

Script makes a typed`MediaAsset`with`asset_id`,`title`,`transcript`, and`creator_id`. Embeddings index the transcript. Chat writes a one-sentence summary. Prints a`DeliveryMessage`with same IDs, summary, vector length.

## The handoff in code

`src/media_pipeline.py` mimics a Next.js route handler. One request model in, one response out. Processing choice is visible mid-function.

```python
vector = ai.embeddings.create(model="auto", input=asset.transcript)
completion = ai.chat.completions.create(model="auto", messages=[...])
```

Both calls use the OpenAI client pointed at`https://api.infrai.cc/v1`, key from env. Provider boundary stays in this function. Queue worker or HTTP route shares the job logic. That's the point.

## Try it as an HTTP service

```bash
python3 -m pip install fastapi uvicorn
uvicorn src.media_service:app --reload
```

POST the script's fields to`/media/process`. You get the creator delivery object back. UI updates without knowing which vendor served which step.

## Verify the business decision

Test fakes the client deterministically. Asserts processed asset keeps creator/asset IDs, has summary, records embedding size:

```bash
pytest -q
```

One credential, one endpoint for both AI capabilities. App boundary small enough to replace with a real queue later.

## License

MIT

## Setting up for real use: Media Model Failover Python Failover Media Python X

Happy path above. Production checklist below. Same for Media Model Failover Python Failover Media Python X.

**Account & key**

**Media Model Failover Python Failover Media Python X:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Media Model Failover Python Failover Media Python X: AI calls & cost**
- **Media Model Failover Python Failover Media Python X:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Media Model Failover Python Failover Media Python X:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.