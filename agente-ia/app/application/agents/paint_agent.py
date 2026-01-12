from typing import List, Dict, Optional
import time
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from app.application.services.api_client import APIClient
from app.application.tools.paint_search_tool import create_paint_search_tool
from app.application.tools.visual_generation_tool import create_visual_generation_tool
from app.domain.services.llm_client import ILLMClient
from app.infrastructure.services.embedding_service import EmbeddingService
from app.infrastructure.llm.prompt_templates.paint_prompt import SYSTEM_PROMPT
from app.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class PaintAgent:
    def __init__(
        self,
        llm_client: ILLMClient,
        api_client: APIClient,
        embedding_service: EmbeddingService,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7
    ):
        self.llm_client = llm_client
        self.api_client = api_client
        self.embedding_service = embedding_service
        self.model = model
        self.temperature = temperature
        self._agent = None
        logger.info("paint_agent_initialized", model=model, temperature=temperature)

    def _create_agent(self):
        logger.debug("creating_agent", model=self.model, temperature=self.temperature)
        tools = [
            create_paint_search_tool(
                self.api_client,
                self.embedding_service
            ),
            create_visual_generation_tool(self.llm_client)
        ]
        
        # Criar modelo com temperature configurado
        llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature
        )
        
        # create_agent não aceita temperature diretamente, usar modelo configurado
        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=SYSTEM_PROMPT
        )
        
        logger.debug("agent_created", tools_count=len(tools))
        return agent

    async def invoke(self, message: str, chat_history: Optional[List[Dict]] = None) -> Dict:
        """
        Invoca o agente e retorna resposta com observabilidade.
        
        Returns:
            Dict com:
            - output: resposta do agente
            - reasoning: raciocínio do agente
            - tools_used: lista de ferramentas utilizadas
        """
        start_time = time.time()
        logger.info(
            "agent_invoke_started",
            message_length=len(message),
            chat_history_length=len(chat_history) if chat_history else 0
        )
        
        if self._agent is None:
            logger.debug("agent_not_initialized", creating_agent=True)
            self._agent = self._create_agent()

        if chat_history is None:
            chat_history = []

        # Preparar mensagens para a nova API
        from langchain_core.messages import HumanMessage, AIMessage
        messages = []
        
        # Adicionar histórico
        for msg in chat_history:
            if msg.get("role") == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg.get("role") == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        # Adicionar mensagem atual
        messages.append(HumanMessage(content=message))

        try:
            # Nova API: invoke com messages
            result = await self._agent.ainvoke({"messages": messages})

            # Extrair output da nova estrutura de resposta
            output = ""
            tools_used = []
            reasoning_parts = []
            
            # A nova API retorna um dict com "messages"
            if isinstance(result, dict):
                result_messages = result.get("messages", [])
                if result_messages:
                    # Pegar a última mensagem (resposta do agente)
                    last_message = result_messages[-1]
                    if hasattr(last_message, 'content'):
                        output = last_message.content
                    elif isinstance(last_message, dict):
                        output = last_message.get("content", "")
                    
                    # Extrair informações sobre tools usados das mensagens
                    for msg in result_messages:
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                tool_name = tool_call.get('name', '') if isinstance(tool_call, dict) else getattr(tool_call, 'name', '')
                                if tool_name and tool_name not in tools_used:
                                    tools_used.append(tool_name)
                                    
                                    if "retrieve_paint_context" in tool_name or "paint_search" in tool_name.lower():
                                        reasoning_parts.append("Busquei tintas na base de dados usando busca semântica")
                                    elif "visual_generation" in tool_name.lower():
                                        reasoning_parts.append("Gerei simulação visual do ambiente")
            elif hasattr(result, 'content'):
                output = result.content
            else:
                output = str(result)
            
            # Se não encontrou steps, mas tem output, inferir reasoning
            if not reasoning_parts and output:
                if "recomendo" in output.lower() or "sugiro" in output.lower():
                    reasoning_parts.append("Analisei a consulta e recomendei produtos baseado nas informações disponíveis")
                else:
                    reasoning_parts.append("Processei a consulta e forneci informações relevantes")
            
            reasoning = " | ".join(reasoning_parts) if reasoning_parts else "Agente processou a consulta usando as ferramentas disponíveis."
            
            elapsed_time = time.time() - start_time
            logger.info(
                "agent_invoke_success",
                output_length=len(output),
                tools_used=tools_used,
                tools_count=len(tools_used),
                elapsed_time=round(elapsed_time, 3)
            )
            
            return {
                "output": output,
                "reasoning": reasoning,
                "tools_used": list(set(tools_used)) if tools_used else []
            }
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "agent_invoke_error",
                error=str(e),
                error_type=type(e).__name__,
                elapsed_time=round(elapsed_time, 3),
                exc_info=True
            )
            raise
