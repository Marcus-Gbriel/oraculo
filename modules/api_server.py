"""
API REST para o Sistema Oraculo
Permite consultas via HTTP POST
"""

from flask import Flask, request, jsonify
from pathlib import Path
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class OracleAPI:
    """
    Servidor API REST para o Sistema Oraculo
    """
    
    def __init__(self, oracle_system, host: str = "127.0.0.1", port: int = 5000):
        """
        Inicializa o servidor API
        
        Args:
            oracle_system: Instância do OracleSystem
            host: Host para o servidor (padrão: 127.0.0.1)
            port: Porta para o servidor (padrão: 5000)
        """
        self.oracle = oracle_system
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        
        # Configurar rotas
        self._setup_routes()
        
        logger.info(f"[API] API REST inicializada em {host}:{port}")
    
    def _setup_routes(self):
        """Configura as rotas da API"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check do servidor"""
            return jsonify({
                "status": "online",
                "service": "Sistema Oraculo API",
                "version": "1.0.0"
            }), 200
        
        @self.app.route('/stats', methods=['GET'])
        def get_stats():
            """Retorna estatísticas do sistema"""
            try:
                stats = self.oracle.get_stats()
                return jsonify({
                    "success": True,
                    "stats": stats
                }), 200
            except Exception as e:
                logger.error(f"[API] Erro ao obter estatísticas: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @self.app.route('/query', methods=['POST'])
        def query():
            """
            Endpoint principal para consultas
            
            Body JSON esperado:
            {
                "question": "Sua pergunta aqui",
                "n_results": 5 (opcional),
                "show_sources": true (opcional)
            }
            
            Retorna JSON:
            {
                "success": true,
                "response": "Resposta do sistema",
                "sources": [...] (se show_sources=true)
            }
            """
            try:
                # Validar request
                if not request.is_json:
                    return jsonify({
                        "success": False,
                        "error": "Content-Type deve ser application/json"
                    }), 400
                
                data = request.get_json()
                
                # Validar campo obrigatório
                if 'question' not in data or not data['question'].strip():
                    return jsonify({
                        "success": False,
                        "error": "Campo 'question' é obrigatório"
                    }), 400
                
                question = data['question'].strip()
                n_results = data.get('n_results', 5)
                show_sources = data.get('show_sources', False)
                
                logger.info(f"[API] Nova consulta recebida: {question[:50]}...")
                
                # Processar consulta
                response = self.oracle.query(
                    question=question,
                    n_results=n_results,
                    show_sources=False  # Sempre False para API
                )
                
                # Preparar resposta
                result = {
                    "success": True,
                    "response": response,
                    "question": question
                }
                
                # Adicionar fontes se solicitado
                if show_sources:
                    # Buscar documentos relevantes para incluir como fontes
                    question_embedding = self.oracle.embedding_generator.generate_embedding(question)
                    relevant_docs = self.oracle.vector_store.search(question_embedding, n_results=n_results)
                    
                    sources = []
                    for doc in relevant_docs:
                        sources.append({
                            "filename": doc.get('metadata', {}).get('filename', 'unknown'),
                            "text": doc.get('text', '')[:200] + "..."  # Primeiros 200 chars
                        })
                    result['sources'] = sources
                
                logger.info(f"[API] Consulta processada com sucesso")
                return jsonify(result), 200
                
            except Exception as e:
                logger.error(f"[API] Erro ao processar consulta: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @self.app.route('/index', methods=['POST'])
        def reindex():
            """
            Endpoint para reindexar documentos
            
            Body JSON esperado:
            {
                "force_reindex": true/false (opcional)
            }
            """
            try:
                data = request.get_json() if request.is_json else {}
                force_reindex = data.get('force_reindex', False)
                
                logger.info(f"[API] Solicitação de reindexação (force={force_reindex})")
                
                # Executar indexação
                self.oracle.index_documents(force_reindex=force_reindex)
                
                stats = self.oracle.get_stats()
                
                return jsonify({
                    "success": True,
                    "message": "Indexação concluída",
                    "stats": stats
                }), 200
                
            except Exception as e:
                logger.error(f"[API] Erro ao reindexar: {str(e)}")
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
    
    def run(self, debug: bool = False):
        """
        Inicia o servidor API
        
        Args:
            debug: Se True, ativa modo debug do Flask
        """
        logger.info(f"[API] Iniciando servidor em http://{self.host}:{self.port}")
        logger.info("[API] Endpoints disponíveis:")
        logger.info("[API]   GET  /health  - Health check")
        logger.info("[API]   GET  /stats   - Estatísticas do sistema")
        logger.info("[API]   POST /query   - Fazer consulta")
        logger.info("[API]   POST /index   - Reindexar documentos")
        
        # Desabilitar logs do Flask (exceto erros)
        if not debug:
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
        
        try:
            self.app.run(
                host=self.host,
                port=self.port,
                debug=debug,
                use_reloader=False  # Evitar reload automático
            )
        except Exception as e:
            logger.error(f"[API] Erro ao iniciar servidor: {str(e)}")
            raise
