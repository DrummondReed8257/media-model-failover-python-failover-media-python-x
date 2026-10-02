from fastapi import FastAPI, HTTPException

from media_pipeline import DeliveryMessage, MediaAsset, run_job

app = FastAPI(title="Media processing handoff")


@app.post("/media/process", response_model=DeliveryMessage)
def process_media(asset: MediaAsset) -> DeliveryMessage:
    try:
        return run_job(asset)
    except KeyError as exc:
        raise HTTPException(status_code=500, detail=f"Missing environment setting: {exc.args[0]}") from exc

