from types import SimpleNamespace

from src.media_pipeline import MediaAsset, process_asset


class FakeEmbeddings:
    def create(self, *, model, input):
        assert model == "auto"
        return SimpleNamespace(data=[SimpleNamespace(embedding=[0.1, 0.2, 0.3])])


class FakeChat:
    class completions:
        @staticmethod
        def create(*, model, messages):
            assert model == "auto"
            assert "Morning surf report" in messages[0]["content"]
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="Waves arrive before noon."))])


class FakeClient:
    embeddings = FakeEmbeddings()
    chat = FakeChat()


def test_processing_job_builds_creator_delivery():
    asset = MediaAsset(asset_id="clip-42", title="Morning surf report", transcript="Waves arrive.", creator_id="creator-7")
    result = process_asset(asset, FakeClient())
    assert result.asset_id == "clip-42"
    assert result.creator_id == "creator-7"
    assert result.summary == "Waves arrive before noon."
    assert result.related_embedding_size == 3

