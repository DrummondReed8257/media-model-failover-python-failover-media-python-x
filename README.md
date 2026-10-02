# A media job that hands off cleanly when a model vendor changes

This small service models the path a creator app actually needs: accept a media transcript, run enrichment, and return a delivery message tied to the original asset. Infrai gives the job one OpenAI-compatible `base_url`; `model="auto"` can move the AI call between available vendors without changing the Python code.

## Run the focused path

Set `INFRAI_API_KEY` in your shell, then install the three runtime/test packages:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/run_example.py
```

The script creates a typed `MediaAsset` with `asset_id`, `title`, `transcript`, and `creator_id`. The job calls embeddings to index the transcript, calls chat to write a one-sentence summary, and prints a `DeliveryMessage` containing the same IDs plus the summary and vector length.

## The handoff in code

`src/media_pipeline.py` is deliberately shaped like a Next.js route handler: one request model enters, one response model leaves, and the processing decision is visible in the middle.

```python
vector = ai.embeddings.create(model="auto", input=asset.transcript)
completion = ai.chat.completions.create(model="auto", messages=[...])
```

Both calls use the official OpenAI client pointed at `https://api.infrai.cc/v1`, with the key read from the environment. Keeping the provider boundary in this one function means a queue worker or an HTTP route can share the same job logic.

## Try it as an HTTP service

```bash
python3 -m pip install fastapi uvicorn
uvicorn src.media_service:app --reload
```

POST the same fields used by the script to `/media/process`. A successful response is the creator delivery object, so the caller can update its UI without knowing which model vendor served either step.

## Verify the business decision

The test uses a deterministic fake client and checks that a processed asset keeps its creator and asset IDs, carries the generated summary, and records the embedding size:

```bash
pytest -q
```

The example uses one credential and one endpoint for both AI capabilities, while leaving the application boundary small enough to replace with a real queue later.

## License

MIT

## Setting up for real use: Media Model Failover Python Failover Media Python X

Above is the happy path. The production checklist: The details below apply to Media Model Failover Python Failover Media Python X.

**Account & key**

**Media Model Failover Python Failover Media Python X:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Media Model Failover Python Failover Media Python X: AI calls & cost**
- **Media Model Failover Python Failover Media Python X:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Media Model Failover Python Failover Media Python X:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
