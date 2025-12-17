"""
Módulo de Vector Store
Responsável por armazenar e buscar embeddings usando ChromaDB
"""

from typing import List, Dict, Optional
import logging
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Classe para gerenciar o armazenamento e busca de vetores usando ChromaDB
    """
    
    def __init__(self, persist_directory: str, collection_name: str = "oraculo_documents"):
        """
        Inicializa o vector store
        
        Args:
            persist_directory: Diretório para persistir os dados
            collection_name: Nome da coleção
        """
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self._initialize_chromadb()
    
    def _initialize_chromadb(self):
        """Inicializa o cliente ChromaDB"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            logger.info(f"Inicializando ChromaDB em: {self.persist_directory}")
            
            # Criar diretório se não existir
            self.persist_directory.mkdir(parents=True, exist_ok=True)
            
            # Inicializar cliente
            self.client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Obter ou criar coleção
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"ChromaDB inicializado. Coleção: {self.collection_name}")
        except Exception as e:
            logger.error(f"Erro ao inicializar ChromaDB: {str(e)}")
            raise
    
    def add_documents(self, chunks: List[Dict], embeddings: List[np.ndarray]):
        """
        Adiciona documentos ao vector store
        
        Args:
            chunks: Lista de chunks com texto e metadados
            embeddings: Lista de embeddings correspondentes
        """
        try:
            logger.info(f"Adicionando {len(chunks)} documentos ao vector store...")
            
            ids = [f"doc_{i}" for i in range(len(chunks))]
            documents = [chunk['text'] for chunk in chunks]
            metadatas = [
                {
                    'filename': chunk['metadata'].get('filename', ''),
                    'chunk_index': chunk.get('chunk_index', 0)
                }
                for chunk in chunks
            ]
            
            # ChromaDB espera embeddings como lista de listas
            embeddings_list = [emb.tolist() for emb in embeddings]
            
            # Adicionar em batches para evitar problemas de memória
            batch_size = 100
            for i in range(0, len(ids), batch_size):
                end_idx = min(i + batch_size, len(ids))
                
                self.collection.add(
                    ids=ids[i:end_idx],
                    documents=documents[i:end_idx],
                    metadatas=metadatas[i:end_idx],
                    embeddings=embeddings_list[i:end_idx]
                )
            
            logger.info(f"Documentos adicionados com sucesso. Total na coleção: {self.collection.count()}")
        except Exception as e:
            logger.error(f"Erro ao adicionar documentos: {str(e)}")
            raise
    
    def search(self, query_embedding: np.ndarray, n_results: int = 5) -> List[Dict]:
        """
        Busca documentos similares ao query
        
        Args:
            query_embedding: Embedding da consulta
            n_results: Número de resultados a retornar
            
        Returns:
            Lista de documentos relevantes com metadados
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results
            )
            
            # Formatar resultados
            formatted_results = []
            if results and results['documents']:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else None
                    })
            
            logger.info(f"Busca retornou {len(formatted_results)} resultados")
            return formatted_results
        except Exception as e:
            logger.error(f"Erro ao buscar documentos: {str(e)}")
            return []
    
    def clear_collection(self):
        """Limpa todos os documentos da coleção"""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Coleção limpa com sucesso")
        except Exception as e:
            logger.error(f"Erro ao limpar coleção: {str(e)}")
    
    def get_collection_stats(self) -> Dict:
        """
        Retorna estatísticas da coleção
        
        Returns:
            Dicionário com estatísticas
        """
        try:
            count = self.collection.count()
            return {
                'total_documents': count,
                'collection_name': self.collection_name
            }
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {str(e)}")
            return {}
