import together

import logging
from typing import Any, Dict, List, Mapping, Optional

from pydantic import Extra, Field, root_validator

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.utils import get_from_dict_or_env
import os

os.environ["TOGETHER_API_KEY"] = "c0b815ee709f842ce09a40379f4a6969292429e7f794a47519895aeffbeeaaf4"
# set your API key
together.api_key = os.environ["TOGETHER_API_KEY"]

class TogetherLLM(LLM):
    """Together large language models."""
    model: str = "togethercomputer/llama-2-70b-chat"
    """model endpoint to use"""
    together_api_key: str = os.environ["TOGETHER_API_KEY"]
    """Together API key"""
    temperature: float = 0.7
    """What sampling temperature to use."""
    max_tokens: int = 512
    """The maximum number of tokens to generate in the completion."""
    class Config:
        extra = "forbid"

    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the API key is set."""
        api_key = get_from_dict_or_env(
            values, "together_api_key", "TOGETHER_API_KEY"
        )
        values["together_api_key"] = api_key
        return values

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "together"

    def _call(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """Call to Together endpoint."""
        together.api_key = self.together_api_key
        output = together.Complete.create(prompt,
                                          model=self.model,
                                          max_tokens=self.max_tokens,
                                          temperature=self.temperature,
                                          )
        text = output['output']['choices'][0]['text']
        return text
