"""C-phase local AI runtime package."""
from .local_ai_controller import LocalAIController
from .model_contracts import GenerationRequest, GenerationResponse, ModelDescriptor
__all__=["LocalAIController","GenerationRequest","GenerationResponse","ModelDescriptor"]
