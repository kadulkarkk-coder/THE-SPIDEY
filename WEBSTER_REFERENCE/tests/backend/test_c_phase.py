from WEBSTER_REFERENCE.ai.local_ai_controller import LocalAIController
from WEBSTER_REFERENCE.ai.model_contracts import ModelDescriptor
from WEBSTER_REFERENCE.ai.embedding_adapter import EmbeddingAdapter
from WEBSTER_REFERENCE.ai.model_permissions import ModelPermissions

def test_builtin_local_model():
    c=LocalAIController(); r=c.generate("hello"); assert r.model_id=="webster-local" and r.text

def test_registry():
    c=LocalAIController(); c.registry.register(ModelDescriptor("x")); assert c.registry.get("x") is not None

def test_embeddings():
    e=EmbeddingAdapter(); assert e.similarity(e.embed("a"),e.embed("a"))>0.9

def test_permissions():
    p=ModelPermissions(); assert p.allowed("local",p.INFER)
