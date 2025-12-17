"""
Módulo de Processamento de Texto
Responsável por chunking e processamento de texto para embeddings
"""

from typing import List, Dict
import re
import logging

logger = logging.getLogger(__name__)


class TextProcessor:
    """
    Classe para processar e dividir texto em chunks para embeddings
    """
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Inicializa o processador de texto
        
        Args:
            chunk_size: Tamanho máximo de cada chunk em caracteres
            chunk_overlap: Sobreposição entre chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def clean_text(self, text: str) -> str:
        """
        Limpa o texto removendo caracteres desnecessários
        
        Args:
            text: Texto a ser limpo
            
        Returns:
            Texto limpo
        """
        # Remove múltiplos espaços
        text = re.sub(r'\s+', ' ', text)
        # Remove espaços no início e fim
        text = text.strip()
        return text
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Divide o texto em sentenças
        
        Args:
            text: Texto a ser dividido
            
        Returns:
            Lista de sentenças
        """
        # Padrão para dividir em sentenças
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def create_chunks(self, text: str, metadata: Dict = None) -> List[Dict[str, any]]:
        """
        Cria chunks de texto com overlap
        
        Args:
            text: Texto a ser dividido em chunks
            metadata: Metadados do documento
            
        Returns:
            Lista de chunks com metadados
        """
        text = self.clean_text(text)
        chunks = []
        
        if len(text) <= self.chunk_size:
            chunks.append({
                'text': text,
                'metadata': metadata or {},
                'chunk_index': 0
            })
            return chunks
        
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Se não é o último chunk, tenta terminar em um espaço
            if end < len(text):
                # Procura o último espaço antes do limite
                last_space = text.rfind(' ', start, end)
                if last_space > start:
                    end = last_space
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append({
                    'text': chunk_text,
                    'metadata': metadata or {},
                    'chunk_index': chunk_index
                })
                chunk_index += 1
            
            # Move o início com overlap
            start = end - self.chunk_overlap
            if start >= len(text):
                break
        
        logger.info(f"Texto dividido em {len(chunks)} chunks")
        return chunks
    
    def process_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, any]]:
        """
        Processa uma lista de documentos criando chunks
        
        Args:
            documents: Lista de documentos com 'filename' e 'content'
            
        Returns:
            Lista de todos os chunks de todos os documentos
        """
        all_chunks = []
        
        for doc in documents:
            metadata = {
                'filename': doc.get('filename', 'unknown'),
                'path': doc.get('path', '')
            }
            
            chunks = self.create_chunks(doc['content'], metadata)
            all_chunks.extend(chunks)
        
        logger.info(f"Total de chunks criados: {len(all_chunks)}")
        return all_chunks
