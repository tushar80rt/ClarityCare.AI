from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.toolkits import SearchToolkit
from camel.configs import MistralConfig
from dotenv import load_dotenv

load_dotenv("api.env") 


def get_therapist_agent():
    mistral_model = ModelFactory.create(
        model_platform=ModelPlatformType.MISTRAL,
        model_type=ModelType.MISTRAL_LARGE, 
        model_config_dict=MistralConfig(temperature=0.7).as_dict(),
    )

    agent = ChatAgent(
        system_message="You are a compassionate AI therapist. Provide empathetic and helpful guidance.",
        model=mistral_model,
    )
    return agent


def search_outside_agent(query: str) -> str:
    search_tool = SearchToolkit().search_duckduckgo
    result = search_tool(query)
    return result
