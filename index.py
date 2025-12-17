#!/usr/bin/env python3
"""
Sistema Oráculo - Agente de IA Local
Consulta documentos PDF, DOCX e Excel usando IA totalmente local

Autor: Marcus Xavier
Versão: 1.0.0
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
import os
import warnings

# Suprimir warnings e logs de bibliotecas externas
warnings.filterwarnings('ignore')
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Silenciar logs de bibliotecas externas
logging.getLogger('sentence_transformers').setLevel(logging.WARNING)
logging.getLogger('chromadb').setLevel(logging.WARNING)
logging.getLogger('gpt4all').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('transformers').setLevel(logging.WARNING)

# Criar pasta de logs se não existir
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Nome do arquivo de log com data
log_filename = logs_dir / f"oraculo_{datetime.now().strftime('%Y%m%d')}.log"

# Configurar logging com níveis diferentes
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Handler para arquivo - VERBOSO (tudo)
file_handler = logging.FileHandler(log_filename, encoding='utf-8', mode='a')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Handler para console - LIMPO (apenas essencial)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)  # Apenas warnings e erros no console
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)

# Adicionar handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger = logging.getLogger(__name__)
logger.info(f"[SISTEMA] Iniciado - Log: {log_filename}")

# Importar o sistema
from modules.oracle_system import OracleSystem
from modules.model_manager import ModelManager


def print_banner():
    """Exibe o banner do sistema"""
    banner = """
    ===============================================================
                                                                   
                      SISTEMA ORACULO                            
                                                                   
              Agente de Inteligencia Artificial Local             
                  para Consulta de Documentos                     
                                                                   
                         Versao 1.0.0                             
                                                                   
    ===============================================================
    """
    print(banner)


def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    required_packages = [
        ('PyPDF2', 'PyPDF2'),
        ('docx', 'python-docx'),
        ('openpyxl', 'openpyxl'),
        ('sentence_transformers', 'sentence-transformers'),
        ('chromadb', 'chromadb'),
    ]
    
    missing = []
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        logger.error("[ERRO] Dependencias faltando!")
        print("\n[ERRO] Dependencias necessarias nao instaladas:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n[INFO] Instale com: pip install " + " ".join(missing))
        return False
    
    logger.info("[SISTEMA] Todas as dependencias instaladas")
    return True


def show_menu():
    """Exibe o menu principal"""
    menu = """
    ===============================================================
                        MENU PRINCIPAL
    ===============================================================
    
    GERENCIAMENTO DE DOCUMENTOS:
    [1] Indexar documentos (primeira vez ou atualizacao)
    [2] Consultar sistema (pergunta unica)
    [3] Modo interativo (multiplas consultas)
    [4] Visualizar estatisticas do sistema
    [5] Reindexar documentos (reconstruir indice)
    
    GERENCIAMENTO DE MODELOS:
    [6] Listar modelos disponiveis
    [7] Visualizar detalhes de modelo
    [8] Selecionar modelo ativo
    
    SERVIDOR API:
    [10] Iniciar servidor API REST
    
    [0] Encerrar sistema
    
    ===============================================================
    """
    print(menu)


def main():
    """Função principal do sistema"""
    print_banner()
    
    # Verificar dependências
    if not check_dependencies():
        logger.error("[ERRO] Sistema nao pode iniciar sem dependencias")
        return 1
    
    # Configurações
    DOCUMENTS_PATH = "training"
    VECTORSTORE_PATH = "src/vectorstore"
    
    # Verificar se a pasta de documentos existe
    if not Path(DOCUMENTS_PATH).exists():
        logger.error(f"[ERRO] Pasta de documentos nao encontrada: {DOCUMENTS_PATH}")
        print(f"\n[ERRO] Crie a pasta '{DOCUMENTS_PATH}' e adicione seus documentos!")
        return 1
    
    try:
        # Inicializar gerenciador de modelos
        model_manager = ModelManager()
        
        # Inicializar sistema
        print("\n[SISTEMA] Inicializando Sistema Oraculo...")
        print("[SISTEMA] Detectando modelo LLM disponivel...")
        
        # Usar modelo selecionado
        selected_model = model_manager.get_selected_model()
        
        oracle = OracleSystem(
            documents_path=DOCUMENTS_PATH,
            vectorstore_path=VECTORSTORE_PATH,
            use_gpt4all=True,
            model_name=selected_model  # Usar modelo configurado
        )
        
        # Loop principal
        while True:
            show_menu()
            choice = input("Escolha uma opcao: ").strip()
            
            if choice == '1':
                print("\n[SISTEMA] Indexando documentos...")
                oracle.index_documents(force_reindex=False)
                input("\n[INFO] Pressione Enter para continuar...")
                
            elif choice == '2':
                question = input("\n[CONSULTA] Digite sua pergunta: ").strip()
                if question:
                    print("\n[SISTEMA] Processando consulta...\n")
                    response = oracle.query(question)
                    print(f"[RESPOSTA]\n{response}")
                input("\n[INFO] Pressione Enter para continuar...")
                
            elif choice == '3':
                oracle.interactive_mode()
                
            elif choice == '4':
                stats = oracle.get_stats()
                print("\n[ESTATISTICAS] Informacoes do Sistema:")
                print(f"   - Total de chunks indexados: {stats.get('total_documents', 0)}")
                print(f"   - Colecao: {stats.get('collection_name', 'N/A')}")
                input("\n[INFO] Pressione Enter para continuar...")
                
            elif choice == '5':
                confirm = input("\n[ATENCAO] Tem certeza que deseja reindexar todos os documentos? (s/n): ")
                if confirm.lower() == 's':
                    print("\n[SISTEMA] Reindexando documentos...")
                    oracle.index_documents(force_reindex=True)
                input("\n[INFO] Pressione Enter para continuar...")
            
            elif choice == '6':
                # Listar modelos disponíveis
                model_manager.print_all_models()
                input("\n[INFO] Pressione Enter para continuar...")
            
            elif choice == '7':
                # Ver detalhes de um modelo
                model_manager.print_all_models()
                model_idx = input("\n[MODELO] Digite o numero do modelo para ver detalhes (ou Enter para voltar): ").strip()
                if model_idx.isdigit():
                    idx = int(model_idx) - 1
                    models = list(model_manager.AVAILABLE_MODELS.keys())
                    if 0 <= idx < len(models):
                        model_manager.print_model_info(models[idx])
                    else:
                        print("[ERRO] Numero invalido!")
                input("\n[INFO] Pressione Enter para continuar...")
            
            elif choice == '8':
                # Selecionar modelo ativo
                installed = model_manager.get_installed_models()
                
                if not installed:
                    print("\n[AVISO] Nenhum modelo instalado!")
                    print("[INFO] O modelo sera baixado automaticamente na primeira execucao.")
                    print("       Selecione um modelo abaixo e execute uma consulta.\n")
                
                model_manager.print_all_models()
                model_idx = input("\n[MODELO] Digite o numero do modelo para ativar (ou Enter para voltar): ").strip()
                
                if model_idx.isdigit():
                    idx = int(model_idx) - 1
                    models = list(model_manager.AVAILABLE_MODELS.keys())
                    if 0 <= idx < len(models):
                        selected = models[idx]
                        try:
                            model_manager.set_selected_model(selected)
                            print(f"\n[SUCESSO] Modelo '{model_manager.AVAILABLE_MODELS[selected]['name']}' selecionado!")
                            print("[AVISO] Reinicie o sistema para aplicar a mudanca.")
                        except ValueError as e:
                            print(f"\n[AVISO] {str(e)}")
                            print("[INFO] O modelo sera baixado na primeira execucao apos reiniciar.")
                    else:
                        print("[ERRO] Numero invalido!")
                input("\n[INFO] Pressione Enter para continuar...")
            
            elif choice == '10':
                # Iniciar servidor API REST
                try:
                    from modules.api_server import OracleAPI
                    
                    print("\n" + "="*63)
                    print("           SERVIDOR API REST")
                    print("="*63)
                    print("\n[API] Configuracao do servidor:")
                    
                    host = input("[API] Host (Enter para 127.0.0.1): ").strip() or "127.0.0.1"
                    port_input = input("[API] Porta (Enter para 5000): ").strip()
                    port = int(port_input) if port_input.isdigit() else 5000
                    
                    print(f"\n[API] Iniciando servidor em http://{host}:{port}")
                    print("[API] Pressione Ctrl+C para encerrar o servidor\n")
                    
                    api = OracleAPI(oracle, host=host, port=port)
                    api.run(debug=False)
                    
                except KeyboardInterrupt:
                    print("\n\n[API] Servidor encerrado")
                except ImportError:
                    print("\n[ERRO] Flask nao esta instalado!")
                    print("[INFO] Instale com: pip install flask")
                except Exception as e:
                    print(f"\n[ERRO] Erro ao iniciar servidor: {str(e)}")
                    logger.error(f"[API] Erro: {str(e)}")
                
                input("\n[INFO] Pressione Enter para continuar...")
                
            elif choice == '0' or choice == '9':
                print("\n[SISTEMA] Encerrando Sistema Oraculo. Ate logo!")
                break
                
            else:
                print("\n[ERRO] Opcao invalida! Tente novamente.")
                input("[INFO] Pressione Enter para continuar...")
    
    except KeyboardInterrupt:
        print("\n\n[SISTEMA] Sistema interrompido. Ate logo!")
        return 0
    except Exception as e:
        logger.error(f"[ERRO] Erro fatal: {str(e)}", exc_info=True)
        print(f"\n[ERRO FATAL] {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
