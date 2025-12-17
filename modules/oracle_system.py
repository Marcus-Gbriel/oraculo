"""
Módulo do Sistema Oráculo
Sistema de RAG (Retrieval Augmented Generation) para consulta de documentos
"""

import logging
from typing import List, Dict, Optional
from pathlib import Path

from modules.document_loader import DocumentLoader
from modules.text_processor import TextProcessor
from modules.embedding_generator import EmbeddingGenerator
from modules.vector_store import VectorStore
from modules.llm import LocalLLM, SimpleLLM, GPT4AllLLM

logger = logging.getLogger(__name__)


class OracleSystem:
    """
    Sistema principal do Oráculo
    Integra todos os componentes para criar um sistema de perguntas e respostas
    baseado em documentos locais
    """
    
    def __init__(
        self,
        documents_path: str = "training",
        vectorstore_path: str = "src/vectorstore",
        model_path: Optional[str] = None,
        use_simple_llm: bool = False,
        use_gpt4all: bool = True,
        model_name: str = "mistral-7b-openorca.Q4_0.gguf"
    ):
        """
        Inicializa o sistema Oráculo
        
        Args:
            documents_path: Caminho para os documentos de treinamento
            vectorstore_path: Caminho para persistir o vector store
            model_path: Caminho para o modelo LLM (GGUF) se usar llama-cpp-python
            use_simple_llm: Se True, usa SimpleLLM para testes
            use_gpt4all: Se True, tenta usar GPT4All (padrão e recomendado)
            model_name: Nome do modelo GPT4All a usar
        """
        self.documents_path = documents_path
        self.vectorstore_path = vectorstore_path
        self.model_path = model_path
        self.model_name = model_name
        
        # Inicializar componentes
        logger.info("Inicializando Sistema Oráculo...")
        
        self.document_loader = DocumentLoader(documents_path)
        self.text_processor = TextProcessor(chunk_size=500, chunk_overlap=50)
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore(vectorstore_path)
        
        # Inicializar LLM com prioridade: GPT4All > LocalLLM > SimpleLLM
        if use_simple_llm:
            logger.warning("Usando SimpleLLM para testes.")
            self.llm = SimpleLLM()
        elif use_gpt4all:
            try:
                logger.info(f"Tentando inicializar GPT4All com modelo: {self.model_name}")
                self.llm = GPT4AllLLM(
                    model_name=self.model_name,
                    model_path="src/models",
                    max_tokens=300  # Respostas mais concisas e rápidas
                )
                logger.info("✅ GPT4All inicializado com sucesso!")
            except Exception as e:
                logger.warning(f"GPT4All não disponível: {str(e)}")
                logger.info("Tentando LocalLLM (llama-cpp-python)...")
                if model_path and Path(model_path).exists():
                    try:
                        self.llm = LocalLLM(model_path)
                        logger.info("✅ LocalLLM inicializado!")
                    except Exception as e2:
                        logger.warning(f"LocalLLM falhou: {str(e2)}")
                        logger.info("Usando SimpleLLM (modo teste)")
                        self.llm = SimpleLLM()
                else:
                    logger.info("Modelo GGUF não encontrado. Usando SimpleLLM (modo teste)")
                    self.llm = SimpleLLM()
        elif model_path and Path(model_path).exists():
            try:
                logger.info("Usando LocalLLM com modelo GGUF...")
                self.llm = LocalLLM(model_path)
            except Exception as e:
                logger.warning(f"LocalLLM falhou: {str(e)}")
                logger.info("Usando SimpleLLM (modo teste)")
                self.llm = SimpleLLM()
        else:
            logger.warning("Nenhum modelo configurado. Usando SimpleLLM para testes.")
            self.llm = SimpleLLM()
        
        logger.info("Sistema Oráculo inicializado com sucesso!")
    
    def index_documents(self, force_reindex: bool = False):
        """
        Indexa todos os documentos da pasta training
        
        Args:
            force_reindex: Se True, limpa o índice existente e reindexа
        """
        logger.info("\n" + "="*50)
        logger.info("INDEXANDO DOCUMENTOS")
        logger.info("="*50)
        
        # Verificar se já existem documentos
        stats = self.vector_store.get_collection_stats()
        if stats.get('total_documents', 0) > 0 and not force_reindex:
            logger.info(f"Já existem {stats['total_documents']} documentos indexados.")
            logger.info("Use force_reindex=True para reindexar.")
            return
        
        if force_reindex:
            logger.info("Limpando índice existente...")
            self.vector_store.clear_collection()
        
        # Carregar documentos
        logger.info("\n1. Carregando documentos...")
        documents = self.document_loader.load_all_documents()
        
        if not documents:
            logger.error("Nenhum documento encontrado para indexar!")
            return
        
        # Processar em chunks
        logger.info("\n2. Processando e dividindo em chunks...")
        chunks = self.text_processor.process_documents(documents)
        
        # Gerar embeddings
        logger.info("\n3. Gerando embeddings...")
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.embedding_generator.generate_embeddings_batch(texts)
        
        # Adicionar ao vector store
        logger.info("\n4. Adicionando ao vector store...")
        self.vector_store.add_documents(chunks, embeddings)
        
        # Estatísticas finais
        final_stats = self.vector_store.get_collection_stats()
        logger.info("\n" + "="*50)
        logger.info("INDEXAÇÃO CONCLUÍDA")
        logger.info(f"Total de documentos: {len(documents)}")
        logger.info(f"Total de chunks: {final_stats.get('total_documents', 0)}")
        logger.info("="*50 + "\n")
    
    def query(self, question: str, n_results: int = 5, show_sources: bool = True) -> str:
        """
        Consulta o sistema com uma pergunta
        
        Args:
            question: Pergunta do usuário
            n_results: Número de documentos relevantes a recuperar (padrão: 5)
            show_sources: Se True, mostra as fontes usadas
            
        Returns:
            Resposta gerada
        """
        logger.info(f"\nProcessando pergunta: {question}")
        
        # Verificar se há documentos indexados
        stats = self.vector_store.get_collection_stats()
        if stats.get('total_documents', 0) == 0:
            return "[ERRO] Nenhum documento indexado. Execute index_documents() primeiro."
        
        # Mensagem visual para o usuário (não é log)
        print("[SISTEMA] Buscando informacoes relevantes...", end='', flush=True)
        
        # Gerar embedding da pergunta
        logger.info("Buscando documentos relevantes...")
        question_embedding = self.embedding_generator.generate_embedding(question)
        
        # Buscar documentos relevantes
        relevant_docs = self.vector_store.search(question_embedding, n_results)
        
        if not relevant_docs:
            print("\r" + " "*50 + "\r", end='')  # Limpar linha
            return "[ERRO] Nao encontrei documentos relevantes para sua pergunta."
        
        print("\r" + " "*50 + "\r", end='')  # Limpar linha
        print("[SISTEMA] Analisando e gerando resposta...", end='', flush=True)
        
        # Criar prompt com contexto
        prompt = self.llm.create_prompt_with_context(question, relevant_docs)
        
        # Gerar resposta
        logger.info("Gerando resposta...")
        response = self.llm.generate(prompt)
        
        print("\r" + " "*50 + "\r", end='')  # Limpar linha de processamento
        
        # Log da resposta gerada (sem fontes)
        logger.info(f"Resposta gerada: {response[:200]}{'...' if len(response) > 200 else ''}")
        
        # Adicionar fontes se solicitado
        if show_sources:
            sources = "\n\n[FONTES CONSULTADAS]\n"
            seen_files = set()
            for doc in relevant_docs:
                filename = doc.get('metadata', {}).get('filename', 'Desconhecido')
                if filename not in seen_files:
                    sources += f"  - {filename}\n"
                    seen_files.add(filename)
            response += sources
        
        # Log completo da interação
        logger.info(f"\n{'='*60}")
        logger.info(f"PERGUNTA: {question}")
        logger.info(f"RESPOSTA COMPLETA: {response}")
        logger.info(f"{'='*60}\n")
        
        return response
    
    def interactive_mode(self):
        """
        Modo interativo de perguntas e respostas
        """
        logger.info("\n" + "="*50)
        logger.info("MODO INTERATIVO DO ORACULO")
        logger.info("="*50)
        logger.info("Digite suas perguntas (ou 'sair' para encerrar)\n")
        
        print("\n" + "="*63)
        print("               MODO INTERATIVO - SISTEMA ORACULO")
        print("="*63)
        print("  Digite suas perguntas. Para sair: 'sair', 'exit' ou 'q'")
        print("="*63)
        
        while True:
            try:
                question = input("\n[CONSULTA] Sua pergunta: ").strip()
                
                if question.lower() in ['sair', 'exit', 'quit', 'q']:
                    logger.info("\nEncerrando Oraculo. Ate logo!")
                    print("\n[SISTEMA] Encerrando modo interativo. Ate logo!\n")
                    break
                
                if not question:
                    continue
                
                # Timestamp da pergunta
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"\n[{timestamp}] Nova pergunta recebida")
                
                response = self.query(question)
                print(f"\n[RESPOSTA]\n{response}")
                
            except KeyboardInterrupt:
                logger.info("\n\nEncerrando Oraculo. Ate logo!")
                print("\n[SISTEMA] Sistema interrompido.\n")
                break
            except Exception as e:
                logger.error(f"Erro: {str(e)}")
                print(f"[ERRO] {str(e)}")
    
    def get_stats(self) -> Dict:
        """
        Retorna estatísticas do sistema
        
        Returns:
            Dicionário com estatísticas
        """
        return self.vector_store.get_collection_stats()
