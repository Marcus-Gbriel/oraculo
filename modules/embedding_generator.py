"""
Módulo de Embeddings
Responsável por gerar embeddings de texto usando modelos locais
"""

from typing import List, Dict
import logging
import numpy as np
import os

# Desabilitar logs do sentence-transformers no console
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """
    Classe para gerar embeddings de texto usando sentence-transformers
    """
    
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Inicializa o gerador de embeddings
        
        Args:
            model_name: Nome do modelo a ser usado (multilingual para português)
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Carrega o modelo de embeddings"""
        try:
            from sentence_transformers import SentenceTransformer
            
            logger.info(f"Carregando modelo de embeddings: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Modelo de embeddings carregado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo de embeddings: {str(e)}")
            raise
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Gera embedding para um texto
        
        Args:
            text: Texto para gerar embedding
            
        Returns:
            Array numpy com o embedding
        """
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"Erro ao gerar embedding: {str(e)}")
            return np.array([])
    
    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 32) -> List[np.ndarray]:
        """
        Gera embeddings para múltiplos textos em batch
        
        Args:
            texts: Lista de textos
            batch_size: Tamanho do batch para processamento
            
        Returns:
            Lista de embeddings
        """
        try:
            logger.info(f"Gerando embeddings para {len(texts)} textos...")
            embeddings = self.model.encode(
                texts, 
                batch_size=batch_size,
                show_progress_bar=True,
                convert_to_numpy=True
            )
            logger.info("Embeddings gerados com sucesso")
            return embeddings
        except Exception as e:
            logger.error(f"Erro ao gerar embeddings em batch: {str(e)}")
            return []
