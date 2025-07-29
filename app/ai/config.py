import os
from typing import Dict, List, Optional

class AIConfig:
    """Configuration for AI providers and models"""
    
    def __init__(self):
        # Provider settings
        self.openai_enabled = bool(os.getenv("OPENAI_API_KEY"))
        self.huggingface_enabled = bool(os.getenv("HUGGINGFACE_API_KEY"))
        
        # OpenAI settings
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        self.openai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
        
        # Hugging Face settings
        self.hf_summarization_model = os.getenv("HF_SUMMARIZATION_MODEL", "facebook/bart-large-cnn")
        self.hf_qa_model = os.getenv("HF_QA_MODEL", "deepset/roberta-base-squad2")
        
        # Local model settings
        self.use_local_models = os.getenv("USE_LOCAL_MODELS", "true").lower() == "true"
        self.local_model_device = os.getenv("LOCAL_MODEL_DEVICE", "auto")  # auto, cpu, cuda
        
        # Processing settings
        self.max_content_length = int(os.getenv("MAX_CONTENT_LENGTH", "4000"))
        self.max_summary_length = int(os.getenv("MAX_SUMMARY_LENGTH", "200"))
        self.max_tags_count = int(os.getenv("MAX_TAGS_COUNT", "5"))
        
        # Provider priority (can be customized)
        self.provider_priority = self._get_provider_priority()
    
    def _get_provider_priority(self) -> List[str]:
        """Get provider priority based on availability and configuration"""
        priority = []
        
        # Add OpenAI if available
        if self.openai_enabled:
            priority.append("openai")
        
        # Add Hugging Face (always available for local models)
        priority.append("huggingface")
        
        # Always add fallback
        priority.append("fallback")
        
        return priority
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers"""
        providers = []
        
        if self.openai_enabled:
            providers.append("OpenAI")
        
        if self.huggingface_enabled or self.use_local_models:
            providers.append("Hugging Face")
        
        providers.append("Rule-based Fallback")
        
        return providers
    
    def get_model_info(self) -> Dict[str, any]:
        """Get information about configured models"""
        return {
            "openai": {
                "enabled": self.openai_enabled,
                "model": self.openai_model if self.openai_enabled else None,
                "max_tokens": self.openai_max_tokens,
                "temperature": self.openai_temperature
            },
            "huggingface": {
                "enabled": self.huggingface_enabled or self.use_local_models,
                "api_enabled": self.huggingface_enabled,
                "local_models_enabled": self.use_local_models,
                "summarization_model": self.hf_summarization_model,
                "qa_model": self.hf_qa_model,
                "device": self.local_model_device
            },
            "processing": {
                "max_content_length": self.max_content_length,
                "max_summary_length": self.max_summary_length,
                "max_tags_count": self.max_tags_count
            },
            "provider_priority": self.provider_priority
        }

# Global configuration instance
ai_config = AIConfig()

def get_ai_config() -> AIConfig:
    """Get AI configuration instance"""
    return ai_config 