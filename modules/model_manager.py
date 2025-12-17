"""
Módulo de Gerenciamento de Modelos LLM
Permite listar, baixar e selecionar modelos GPT4All
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ModelManager:
    """Gerencia modelos LLM disponíveis"""
    
    # Modelos recomendados do GPT4All
    AVAILABLE_MODELS = {
        "mistral-7b-openorca.Q4_0.gguf": {
            "name": "Mistral 7B OpenOrca",
            "size": "3.8 GB",
            "quality": "⭐⭐⭐⭐⭐",
            "speed": "⚡⚡⚡⚡",
            "description": "Excelente equilíbrio entre qualidade e velocidade. Recomendado!",
            "best_for": "Uso geral, perguntas técnicas"
        },
        "mistral-7b-instruct-v0.1.Q4_0.gguf": {
            "name": "Mistral 7B Instruct",
            "size": "3.8 GB",
            "quality": "⭐⭐⭐⭐⭐",
            "speed": "⚡⚡⚡⚡",
            "description": "Otimizado para seguir instruções com precisão",
            "best_for": "Tarefas que exigem precisão literal"
        },
        "orca-2-7b.Q4_0.gguf": {
            "name": "Orca 2 7B",
            "size": "3.8 GB",
            "quality": "⭐⭐⭐⭐",
            "speed": "⚡⚡⚡⚡",
            "description": "Treinado pela Microsoft, bom raciocínio lógico",
            "best_for": "Análise de documentos técnicos"
        },
        "nous-hermes-llama2-13b.Q4_0.gguf": {
            "name": "Nous Hermes LLaMA2 13B",
            "size": "7.3 GB",
            "quality": "⭐⭐⭐⭐⭐",
            "speed": "⚡⚡⚡",
            "description": "Maior e mais preciso, mas mais lento",
            "best_for": "Quando precisão é crítica"
        },
        "gpt4all-falcon-q4_0.gguf": {
            "name": "GPT4All Falcon",
            "size": "3.9 GB",
            "quality": "⭐⭐⭐⭐",
            "speed": "⚡⚡⚡⚡",
            "description": "Modelo aberto da TII, boa versatilidade",
            "best_for": "Uso geral, respostas criativas"
        },
        "wizardlm-13b-v1.2.Q4_0.gguf": {
            "name": "WizardLM 13B",
            "size": "7.3 GB",
            "quality": "⭐⭐⭐⭐⭐",
            "speed": "⚡⚡⚡",
            "description": "Excelente para raciocínio complexo",
            "best_for": "Perguntas complexas que exigem análise profunda"
        },
        "orca-mini-3b.ggmlv3.q4_0.gguf": {
            "name": "Orca Mini 3B",
            "size": "1.8 GB",
            "quality": "⭐⭐⭐",
            "speed": "⚡⚡⚡⚡⚡",
            "description": "Modelo pequeno e rápido, ideal para testes",
            "best_for": "Máquinas com pouca memória, respostas rápidas"
        }
    }
    
    def __init__(self, models_dir: str = "src/models", config_file: str = "config.json"):
        """
        Inicializa o gerenciador de modelos
        
        Args:
            models_dir: Diretório onde os modelos são armazenados
            config_file: Arquivo de configuração
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Carrega configuração do arquivo JSON"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"[AVISO] Erro ao carregar config: {e}")
        
        # Configuração padrão
        return {
            "selected_model": "mistral-7b-openorca.Q4_0.gguf",
            "temperature": 0.2,
            "max_tokens": 512
        }
    
    def _save_config(self):
        """Salva configuração no arquivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, indent=2, fp=f, ensure_ascii=False)
            logger.info(f"[CONFIG] Configuracao salva em {self.config_file}")
        except Exception as e:
            logger.error(f"[ERRO] Erro ao salvar config: {e}")
    
    def get_installed_models(self) -> List[str]:
        """Retorna lista de modelos instalados"""
        installed = []
        for model_file in self.AVAILABLE_MODELS.keys():
            if (self.models_dir / model_file).exists():
                installed.append(model_file)
        return installed
    
    def get_selected_model(self) -> str:
        """Retorna o modelo atualmente selecionado"""
        return self.config.get("selected_model", "mistral-7b-openorca.Q4_0.gguf")
    
    def set_selected_model(self, model_name: str):
        """
        Define o modelo a ser usado
        
        Args:
            model_name: Nome do arquivo do modelo
        """
        if model_name not in self.AVAILABLE_MODELS:
            raise ValueError(f"Modelo '{model_name}' não está na lista de modelos disponíveis")
        
        if not (self.models_dir / model_name).exists():
            raise ValueError(f"Modelo '{model_name}' não está instalado")
        
        self.config["selected_model"] = model_name
        self._save_config()
        logger.info(f"[CONFIG] Modelo selecionado: {model_name}")
    
    def list_available_models(self) -> Dict:
        """Retorna dicionário de modelos disponíveis"""
        return self.AVAILABLE_MODELS
    
    def print_model_info(self, model_file: str):
        """
        Imprime informações detalhadas sobre um modelo
        
        Args:
            model_file: Nome do arquivo do modelo
        """
        if model_file not in self.AVAILABLE_MODELS:
            print(f"[ERRO] Modelo '{model_file}' nao encontrado")
            return
        
        info = self.AVAILABLE_MODELS[model_file]
        is_installed = (self.models_dir / model_file).exists()
        is_selected = (model_file == self.get_selected_model())
        
        print(f"\n{'='*63}")
        print(f"  {info['name']}")
        print(f"{'='*63}")
        print(f"   Arquivo:     {model_file}")
        print(f"   Tamanho:     {info['size']}")
        print(f"   Qualidade:   {info['quality']}")
        print(f"   Velocidade:  {info['speed']}")
        print(f"   Descricao:   {info['description']}")
        print(f"   Melhor para: {info['best_for']}")
        print(f"   Status:      {'[INSTALADO]' if is_installed else '[NAO INSTALADO]'}")
        if is_selected:
            print(f"   {'[MODELO ATIVO]' }")
        print(f"{'='*63}\n")
    
    def print_all_models(self):
        """Imprime tabela com todos os modelos disponíveis"""
        installed = self.get_installed_models()
        selected = self.get_selected_model()
        
        print("\n" + "="*90)
        print(" "*25 + "MODELOS LLM DISPONIVEIS")
        print("="*90)
        print(f"{'#':<4} {'Nome':<30} {'Tamanho':<10} {'Qualidade':<12} {'Status':<15}")
        print("-"*90)
        
        for idx, (model_file, info) in enumerate(self.AVAILABLE_MODELS.items(), 1):
            is_installed = model_file in installed
            is_selected = model_file == selected
            
            status = ""
            if is_selected:
                status = "[ATIVO]"
            elif is_installed:
                status = "[INSTALADO]"
            else:
                status = "[NAO INSTALADO]"
            
            print(f"{idx:<4} {info['name']:<30} {info['size']:<10} {info['quality']:<12} {status:<15}")
        
        print("="*90)
        print(f"\n  Modelos instalados: {len(installed)}/{len(self.AVAILABLE_MODELS)}")
        print(f"  Modelo ativo: {self.AVAILABLE_MODELS[selected]['name']}\n")
    
    def download_model(self, model_file: str) -> bool:
        """
        Baixa um modelo (será feito pelo GPT4All automaticamente)
        
        Args:
            model_file: Nome do arquivo do modelo
            
        Returns:
            True se já instalado ou False se precisa instalar
        """
        if model_file not in self.AVAILABLE_MODELS:
            print(f"[ERRO] Modelo '{model_file}' nao esta na lista de modelos disponiveis")
            return False
        
        if (self.models_dir / model_file).exists():
            print(f"[INFO] Modelo '{model_file}' ja esta instalado")
            return True
        
        info = self.AVAILABLE_MODELS[model_file]
        print(f"\n[SISTEMA] Preparando download de: {info['name']}")
        print(f"          Tamanho: {info['size']}")
        print(f"\n[AVISO] O modelo sera baixado automaticamente pelo GPT4All na primeira execucao.")
        print(f"        Selecione este modelo no menu e execute uma consulta para iniciar o download.\n")
        
        return False
