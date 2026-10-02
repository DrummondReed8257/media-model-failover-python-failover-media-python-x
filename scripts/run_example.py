import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.media_pipeline import MediaAsset, run_job


asset = MediaAsset(
    asset_id="clip-42",
    title="Morning surf report",
    transcript="Small waves arrive before noon, with clear skies through the afternoon.",
    creator_id="creator-7",
)
print(json.dumps(run_job(asset).model_dump(), indent=2))
