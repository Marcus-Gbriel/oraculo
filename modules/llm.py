"""
Módulo de Modelo de Linguagem Local
Responsável por gerenciar LLMs locais (GPT4All, LLaMA, etc)
"""

import logging
from typing import Optional, List, Dict
from pathlib import Path
import os

logger = logging.getLogger(__name__)


def detect_gpu():
    """
    Detecta se há GPU NVIDIA disponível
    
    Returns:
        bool: True se GPU está disponível, False caso contrário
    """
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_count = torch.cuda.device_count()
            logger.info(f"🎮 GPU Detectada: {gpu_name}")
            logger.info(f"   Quantidade: {gpu_count}")
            return True
    except ImportError:
        logger.debug("PyTorch não instalado, verificando alternativas...")
    
    # Verificar via nvidia-smi (método alternativo)
    try:
        import subprocess
        result = subprocess.run(['nvidia-smi'], 
                              capture_output=True, 
                              text=True, 
                              timeout=2)
        if result.returncode == 0:
            logger.info("🎮 GPU NVIDIA detectada via nvidia-smi")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    logger.info("💻 GPU não detectada, usando CPU")
    return False


class LocalLLM:
    """
    Classe para gerenciar o modelo de linguagem local
    Usa llama-cpp-python para rodar modelos GGUF localmente
    """
    
    def __init__(
        self, 
        model_path: str,
        n_ctx: int = 2048,
        n_threads: int = 4,
        temperature: float = 0.7,
        max_tokens: int = 512
    ):
        """
        Inicializa o modelo de linguagem local
        
        Args:
            model_path: Caminho para o arquivo do modelo GGUF
            n_ctx: Tamanho do contexto
            n_threads: Número de threads para usar
            temperature: Temperatura para geração (0.0-1.0)
            max_tokens: Máximo de tokens para gerar
        """
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.llm = None
        self._load_model()
    
    def _load_model(self):
        """Carrega o modelo LLaMA"""
        try:
            from llama_cpp import Llama
            
            logger.info(f"Carregando modelo LLM de: {self.model_path}")
            
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                verbose=False
            )
            
            logger.info("Modelo LLM carregado com sucesso")
        except FileNotFoundError:
            logger.error(f"Arquivo do modelo não encontrado: {self.model_path}")
            logger.info("INSTRUÇÕES: Baixe um modelo GGUF compatível (ex: Llama-2-7B)")
            logger.info("Coloque o modelo na pasta src/models/")
            raise
        except Exception as e:
            logger.error(f"Erro ao carregar modelo LLM: {str(e)}")
            raise
    
    def generate(
        self, 
        prompt: str, 
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stop: Optional[List[str]] = None
    ) -> str:
        """
        Gera resposta do modelo
        
        Args:
            prompt: Prompt para o modelo
            max_tokens: Máximo de tokens (sobrescreve o padrão)
            temperature: Temperatura (sobrescreve o padrão)
            stop: Lista de strings para parar a geração
            
        Returns:
            Texto gerado
        """
        try:
            if not self.llm:
                raise RuntimeError("Modelo não carregado")
            
            max_tok = max_tokens if max_tokens is not None else self.max_tokens
            temp = temperature if temperature is not None else self.temperature
            
            response = self.llm(
                prompt,
                max_tokens=max_tok,
                temperature=temp,
                stop=stop or [],
                echo=False
            )
            
            return response['choices'][0]['text'].strip()
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}")
            return "Desculpe, ocorreu um erro ao gerar a resposta."
    
    def create_prompt_with_context(
        self, 
        question: str, 
        context_documents: List[Dict]
    ) -> str:
        """
        Cria um prompt com contexto dos documentos relevantes
        
        Args:
            question: Pergunta do usuário
            context_documents: Lista de documentos relevantes
            
        Returns:
            Prompt formatado
        """
        # Construir contexto
        context_parts = []
        for i, doc in enumerate(context_documents, 1):
            filename = doc.get('metadata', {}).get('filename', 'Documento')
            text = doc.get('text', '')
            context_parts.append(f"[Fonte {i}: {filename}]\n{text}\n")
        
        context = "\n".join(context_parts)
        
        # Template do prompt
        prompt = f"""<s>[INST] <<SYS>>
Você é um assistente inteligente chamado Oráculo. Sua função é responder perguntas com base nos documentos fornecidos.
Use apenas as informações dos documentos para responder. Se não souber a resposta, diga que não encontrou a informação.
Seja claro, preciso e objetivo. Sempre cite a fonte quando possível.
<</SYS>>

Documentos de referência:

{context}

Pergunta: {question}

Resposta: [/INST]"""
        
        return prompt


class GPT4AllLLM:
    """
    Classe para gerenciar o modelo GPT4All (100% Python)
    Baixa e gerencia modelos automaticamente
    """
    
    def __init__(
        self,
        model_name: str = "mistral-7b-openorca.Q4_0.gguf",
        model_path: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 512,
        n_threads: Optional[int] = None,
        use_gpu: Optional[bool] = None
    ):
        """
        Inicializa o modelo GPT4All
        
        Args:
            model_name: Nome do modelo (será baixado automaticamente)
            model_path: Caminho para a pasta de modelos
            temperature: Temperatura para geração (0.0-1.0)
            max_tokens: Máximo de tokens para gerar
            n_threads: Número de threads (None = detecta automaticamente)
            use_gpu: True para forçar GPU, False para CPU, None = auto-detectar
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = None
        
        # Detectar GPU se não especificado
        if use_gpu is None:
            self.use_gpu = detect_gpu()
        else:
            self.use_gpu = use_gpu
        
        # Detectar número de threads (cores lógicas) - usado quando GPU não disponível
        if n_threads is None:
            # Usa todos os cores disponíveis
            self.n_threads = os.cpu_count() or 4
        else:
            self.n_threads = n_threads
        
        # Definir pasta de modelos
        if model_path:
            self.model_path = Path(model_path)
        else:
            self.model_path = Path("src/models")
        
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        self._load_model()
    
    def _load_model(self):
        """Carrega o modelo GPT4All (baixa se necessário)"""
        try:
            from gpt4all import GPT4All
            import sys
            import contextlib
            
            logger.info(f"Inicializando GPT4All: {self.model_name}")
            logger.info(f"Pasta de modelos: {self.model_path}")
            
            # Configurar device baseado na detecção
            if self.use_gpu:
                device = 'gpu'
                logger.info(f"⚡ Aceleração GPU ATIVADA")
                logger.info(f"   Threads CPU: {self.n_threads} (auxílio)")
            else:
                device = 'cpu'
                logger.info(f"💻 Modo CPU")
                logger.info(f"   Threads: {self.n_threads}")
            
            # GPT4All baixa automaticamente se não existir
            try:
                # Suprimir warnings de DLL do GPT4All
                with contextlib.redirect_stderr(open(os.devnull, 'w')):
                    self.model = GPT4All(
                        model_name=self.model_name,
                        model_path=str(self.model_path),
                        allow_download=True,
                        n_threads=self.n_threads,
                        device=device,
                        verbose=False  # Desabilitar verbose
                    )
                
                if self.use_gpu:
                    logger.info(f"✅ Modelo carregado com GPU! (RTX 4070 Super detectada)")
                else:
                    logger.info(f"✅ Modelo carregado com CPU ({self.n_threads} threads)")
                    
            except Exception as gpu_error:
                if self.use_gpu:
                    logger.warning(f"Falha ao carregar com GPU: {gpu_error}")
                    logger.info("Tentando novamente com CPU...")
                    # Fallback para CPU
                    with contextlib.redirect_stderr(open(os.devnull, 'w')):
                        self.model = GPT4All(
                            model_name=self.model_name,
                            model_path=str(self.model_path),
                            allow_download=True,
                            n_threads=self.n_threads,
                            device='cpu',
                            verbose=False
                        )
                    self.use_gpu = False
                    logger.info(f"✅ Modelo carregado com CPU (fallback)")
                else:
                    raise
            
        except ImportError:
            logger.error("GPT4All não está instalado!")
            logger.info("Instale com: pip install gpt4all")
            raise
        except Exception as e:
            logger.error(f"Erro ao carregar GPT4All: {str(e)}")
            raise
    
    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Gera resposta do modelo
        
        Args:
            prompt: Prompt para o modelo
            max_tokens: Máximo de tokens (sobrescreve o padrão)
            temperature: Temperatura (sobrescreve o padrão)
            
        Returns:
            Texto gerado
        """
        try:
            if not self.model:
                raise RuntimeError("Modelo não carregado")
            
            max_tok = max_tokens if max_tokens is not None else self.max_tokens
            temp = temperature if temperature is not None else self.temperature
            
            # GPT4All usa chat() ou generate() com otimizações
            with self.model.chat_session():
                response = self.model.generate(
                    prompt=prompt,
                    max_tokens=max_tok,
                    temp=temp,
                    n_batch=256,  # Processar mais tokens por vez
                    n_predict=max_tok,  # Otimizar predição
                    repeat_penalty=1.2,  # Evitar repetições
                    top_k=40,  # Top-k sampling
                    top_p=0.9  # Nucleus sampling
                )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}")
            return "Desculpe, ocorreu um erro ao gerar a resposta."
    
    def create_prompt_with_context(
        self,
        question: str,
        context_documents: List[Dict]
    ) -> str:
        """
        Cria um prompt com contexto dos documentos relevantes
        
        Args:
            question: Pergunta do usuário
            context_documents: Lista de documentos relevantes
            
        Returns:
            Prompt formatado
        """
        # Agrupar por arquivo para não duplicar fontes
        docs_by_file = {}
        for doc in context_documents:
            filename = doc.get('metadata', {}).get('filename', 'Documento')
            text = doc.get('text', '')
            
            if filename not in docs_by_file:
                docs_by_file[filename] = []
            docs_by_file[filename].append(text)
        
        # Construir contexto agrupado e otimizado
        context_parts = []
        for filename, texts in docs_by_file.items():
            combined_text = "\n\n".join(texts)
            # Limitar tamanho para acelerar processamento
            if len(combined_text) > 2500:
                combined_text = combined_text[:2500] + "..."
            context_parts.append(f"=== {filename} ===\n{combined_text}")
        
        context = "\n\n".join(context_parts)
        
        # Template otimizado com instruções RIGOROSAS
        prompt = f"""Você é um assistente técnico PRECISO. Sua função é responder baseado EXCLUSIVAMENTE no documento fornecido.

DOCUMENTO:
{context}

INSTRUÇÕES CRÍTICAS:
1. Leia o documento COM ATENÇÃO antes de responder
2. Use APENAS informações EXPLÍCITAS do documento
3. NUNCA invente, interprete ou assuma informações que não estão escritas
4. CITE trechos literais do documento usando aspas quando possível
5. Se o documento contradiz a premissa da pergunta, CORRIJA o usuário
6. Seja ESPECÍFICO: mencione itens, números, requisitos exatos

EXEMPLOS DO QUE NÃO FAZER:
❌ "Sim, está correto" (quando o documento diz o contrário)
❌ "Ajuda a garantir isolamento" (se o documento não menciona isso)
❌ Confirmar práticas que o documento não valida

EXEMPLO DO QUE FAZER:
✓ "Não, segundo o item 4 do documento: '[citação literal]'"
✓ "O documento especifica que deve-se..."
✓ "Sua abordagem difere do recomendado. O documento indica..."

Pergunta: {question}

Resposta (seja PRECISO e LITERAL):"""
        
        return prompt


class SimpleLLM:
    """
    Implementação simplificada para testes sem modelo LLM
    Útil para desenvolvimento e testes iniciais
    """
    
    def __init__(self):
        logger.warning("Usando SimpleLLM - apenas para testes. Respostas serão limitadas.")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Gera resposta simples baseada no contexto"""
        return "Esta é uma resposta de teste. Configure um modelo LLM real para respostas completas."
    
    def create_prompt_with_context(self, question: str, context_documents: List[Dict]) -> str:
        """Cria prompt simples"""
        context = "\n\n".join([doc.get('text', '')[:200] + "..." for doc in context_documents])
        return f"Contexto:\n{context}\n\nPergunta: {question}"
