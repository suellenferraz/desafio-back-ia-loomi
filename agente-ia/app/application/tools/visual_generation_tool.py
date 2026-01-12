from langchain.tools import tool
import time
from app.infrastructure.llm.openai_client import OpenAIClient
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


def create_visual_generation_tool(openai_client: OpenAIClient):
    @tool
    async def visual_generation_tool(
        description: str,
        color: str,
        environment: str,
        room_type: str = "sala"
    ) -> str:
        """
        Gera uma imagem simulando a aplicação da tinta em um ambiente.
        
        Args:
            description: Descrição do ambiente
            color: Cor da tinta (ex: "azul sereno")
            environment: "interno" ou "externo"
            room_type: Tipo de cômodo (ex: "quarto", "sala", "varanda")
        
        Returns:
            URL da imagem gerada
        """
        start_time = time.time()
        logger.info(
            "visual_generation_tool_started",
            tool="visual_generation_tool",
            color=color,
            environment=environment,
            room_type=room_type,
            description=description
        )
        
        try:
            clean_color = color.lower().replace(" ", "_")
            
            if environment == "externo":
                prompt = f"Modern building exterior painted {clean_color}, architectural photo, professional lighting"
            else:
                room_term = room_type if room_type else "room"
                prompt = f"Modern {room_term} with {clean_color} walls, interior design photo, professional lighting"
            
            logger.debug("dalle_prompt_created", prompt=prompt)
            image_url = await openai_client.generate_image(prompt)
            
            elapsed_time = time.time() - start_time
            logger.info(
                "visual_generation_tool_success",
                tool="visual_generation_tool",
                image_url=image_url,
                elapsed_time=round(elapsed_time, 3)
            )
            
            return image_url
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "visual_generation_tool_error",
                tool="visual_generation_tool",
                error=str(e),
                error_type=type(e).__name__,
                elapsed_time=round(elapsed_time, 3),
                exc_info=True
            )
            raise
    
    return visual_generation_tool
