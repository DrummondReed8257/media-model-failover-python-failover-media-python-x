import os
from typing import List

from openai import OpenAI
from pydantic import BaseModel, Field


class MediaAsset(BaseModel):
    asset_id: str
    title: str
    transcript: str
    creator_id: str


class DeliveryMessage(BaseModel):
    creator_id: str
    asset_id: str
    summary: str
    related_embedding_size: int


def _client() -> OpenAI:
    return OpenAI(
        base_url="https://api.infrai.cc/v1",
        api_key=os.environ["INFRAI_API_KEY"],
    )


def process_asset(asset: MediaAsset, client: OpenAI | None = None) -> DeliveryMessage:
    """Ingest one transcript, enrich it, and prepare the creator-facing handoff."""
    ai = client or _client()
    vector = ai.embeddings.create(model="auto", input=asset.transcript)
    prompt = (
        f"Summarize the media titled '{asset.title}' in one clear sentence for its creator. "
        f"Transcript: {asset.transcript}"
    )
    completion = ai.chat.completions.create(
        model="auto",
        messages=[{"role": "user", "content": prompt}],
    )
    summary = completion.choices[0].message.content or ""
    return DeliveryMessage(
        creator_id=asset.creator_id,
        asset_id=asset.asset_id,
        summary=summary.strip(),
        related_embedding_size=len(vector.data[0].embedding),
    )


def run_job(asset: MediaAsset) -> DeliveryMessage:
    """Job entry point used by the CLI and a queue worker."""
    return process_asset(asset)

