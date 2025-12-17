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
logger.info(f"Sistema iniciado - Log: {log_filename}")

# Importar o sistema
from modules.oracle_system import OracleSystem
from modules.model_manager import ModelManager


def print_banner():
    """Exibe o banner do sistema"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🔮  SISTEMA ORÁCULO  🔮                      ║
    ║                                                           ║
    ║         Agente de IA Local para Consulta de              ║
    ║              Documentos Empresariais                      ║
    ║                                                           ║
    ║                   Versão 1.0.0                            ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
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
        logger.error("Dependências faltando!")
        print("\n❌ Dependências necessárias não instaladas:")
        for pkg in missing:
            print(f"   • {pkg}")
        print("\n📦 Instale com: pip install " + " ".join(missing))
        return False
    
    logger.info("✅ Todas as dependências estão instaladas")
    return True


def show_menu():
    """Exibe o menu principal"""
    menu = """
    ═══════════════════════════════════════
              MENU PRINCIPAL
    ═══════════════════════════════════════
    
    📚 DOCUMENTOS:
    1. Indexar documentos (primeira vez ou atualização)
    2. Fazer pergunta ao Oráculo
    3. Modo interativo (múltiplas perguntas)
    4. Ver estatísticas do sistema
    5. Reindexar documentos (limpar e recriar índice)
    
    🤖 MODELOS LLM:
    6. Listar modelos disponíveis
    7. Ver detalhes de um modelo
    8. Selecionar modelo ativo
    
    9. Sair
    
    ═══════════════════════════════════════
    """
    print(menu)


def main():
    """Função principal do sistema"""
    print_banner()
    
    # Verificar dependências
    if not check_dependencies():
        logger.error("Sistema não pode iniciar sem as dependências necessárias")
        return 1
    
    # Configurações
    DOCUMENTS_PATH = "training"
    VECTORSTORE_PATH = "src/vectorstore"
    
    # Verificar se a pasta de documentos existe
    if not Path(DOCUMENTS_PATH).exists():
        logger.error(f"Pasta de documentos não encontrada: {DOCUMENTS_PATH}")
        print(f"\n❌ Crie a pasta '{DOCUMENTS_PATH}' e adicione seus documentos!")
        return 1
    
    try:
        # Inicializar gerenciador de modelos
        model_manager = ModelManager()
        
        # Inicializar sistema
        print("\n🔄 Inicializando Sistema Oráculo...")
        print("   Detectando LLM disponível...")
        
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
            choice = input("Escolha uma opção: ").strip()
            
            if choice == '1':
                print("\n📚 Indexando documentos...")
                oracle.index_documents(force_reindex=False)
                input("\n✅ Pressione Enter para continuar...")
                
            elif choice == '2':
                question = input("\n🔮 Sua pergunta: ").strip()
                if question:
                    print("\n💭 Processando...\n")
                    response = oracle.query(question)
                    print(f"💡 Resposta:\n{response}")
                input("\n✅ Pressione Enter para continuar...")
                
            elif choice == '3':
                oracle.interactive_mode()
                
            elif choice == '4':
                stats = oracle.get_stats()
                print("\n📊 Estatísticas do Sistema:")
                print(f"   • Total de chunks indexados: {stats.get('total_documents', 0)}")
                print(f"   • Coleção: {stats.get('collection_name', 'N/A')}")
                input("\n✅ Pressione Enter para continuar...")
                
            elif choice == '5':
                confirm = input("\n⚠️  Tem certeza que deseja reindexar todos os documentos? (s/n): ")
                if confirm.lower() == 's':
                    print("\n🔄 Reindexando documentos...")
                    oracle.index_documents(force_reindex=True)
                input("\n✅ Pressione Enter para continuar...")
            
            elif choice == '6':
                # Listar modelos disponíveis
                model_manager.print_all_models()
                input("\n✅ Pressione Enter para continuar...")
            
            elif choice == '7':
                # Ver detalhes de um modelo
                model_manager.print_all_models()
                model_idx = input("\n📦 Digite o número do modelo para ver detalhes (ou Enter para voltar): ").strip()
                if model_idx.isdigit():
                    idx = int(model_idx) - 1
                    models = list(model_manager.AVAILABLE_MODELS.keys())
                    if 0 <= idx < len(models):
                        model_manager.print_model_info(models[idx])
                    else:
                        print("❌ Número inválido!")
                input("\n✅ Pressione Enter para continuar...")
            
            elif choice == '8':
                # Selecionar modelo ativo
                installed = model_manager.get_installed_models()
                
                if not installed:
                    print("\n❌ Nenhum modelo instalado!")
                    print("💡 Dica: O modelo será baixado automaticamente na primeira execução.")
                    print("   Selecione um modelo abaixo e execute uma consulta.\n")
                
                model_manager.print_all_models()
                model_idx = input("\n⭐ Digite o número do modelo para ativar (ou Enter para voltar): ").strip()
                
                if model_idx.isdigit():
                    idx = int(model_idx) - 1
                    models = list(model_manager.AVAILABLE_MODELS.keys())
                    if 0 <= idx < len(models):
                        selected = models[idx]
                        try:
                            model_manager.set_selected_model(selected)
                            print(f"\n✅ Modelo '{model_manager.AVAILABLE_MODELS[selected]['name']}' selecionado!")
                            print("⚠️  Reinicie o sistema para aplicar a mudança.")
                        except ValueError as e:
                            print(f"\n⚠️  {str(e)}")
                            print("💡 O modelo será baixado na primeira execução após reiniciar.")
                    else:
                        print("❌ Número inválido!")
                input("\n✅ Pressione Enter para continuar...")
                
            elif choice == '9':
                print("\n👋 Encerrando Sistema Oráculo. Até logo!")
                break
                
            else:
                print("\n❌ Opção inválida! Tente novamente.")
                input("Pressione Enter para continuar...")
    
    except KeyboardInterrupt:
        print("\n\n👋 Sistema interrompido. Até logo!")
        return 0
    except Exception as e:
        logger.error(f"Erro fatal: {str(e)}", exc_info=True)
        print(f"\n❌ Erro fatal: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
