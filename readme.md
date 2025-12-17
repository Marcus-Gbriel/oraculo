# Sistema Oráculo 🔮

Sistema de Inteligência Artificial local para consulta de documentos empresariais usando RAG (Retrieval Augmented Generation).

## 📋 Descrição

O Sistema Oráculo é uma solução completa de IA que funciona totalmente offline, sem necessidade de APIs externas ou conexão com a internet. Ele processa documentos em PDF, DOCX e Excel, criando uma base de conhecimento consultável através de perguntas em linguagem natural.

## ✨ Características

- ✅ **100% Local**: Funciona completamente offline, sem APIs externas
- 📚 **Múltiplos Formatos**: Suporta PDF, DOCX e Excel (XLSX/XLS)
- 🧠 **RAG Avançado**: Usa Retrieval Augmented Generation para respostas precisas
- 🔍 **Vector Search**: ChromaDB para busca semântica eficiente
- 🌐 **Multilíngue**: Suporta português e outros idiomas
- 💾 **Persistente**: Indexação permanece entre execuções
- 🎯 **Profissional**: Arquitetura limpa e modular

## 🏗️ Arquitetura

```
oraculo/
├── index.py                    # Ponto de entrada único do sistema
├── config.json                 # Configurações persistentes (modelo ativo, etc)
├── BENCHMARK-PERGUNTAS.md      # Perguntas para testar precisão do sistema
├── training/                   # Documentos para indexação
│   └── desenvolvimento_seguro.pdf
├── logs/                       # Logs organizados por data
│   └── oraculo_YYYYMMDD.log
├── modules/                    # Módulos do sistema
│   ├── __init__.py
│   ├── document_loader.py     # Carregamento de documentos
│   ├── text_processor.py      # Processamento e chunking
│   ├── embedding_generator.py # Geração de embeddings
│   ├── vector_store.py        # Armazenamento vetorial
│   ├── llm.py                 # Modelos de linguagem (GPT4All, etc)
│   ├── model_manager.py       # Gerenciamento de modelos LLM
│   └── oracle_system.py       # Sistema principal RAG
├── src/                        # Recursos do sistema
│   ├── models/                # Modelos de IA (GPT4All)
│   └── vectorstore/           # Banco de vetores persistente
└── docs/                       # Documentação
    ├── README.md
    ├── INSTALLATION.md
    ├── ARCHITECTURE.md
    └── GPT4ALL-IMPLEMENTADO.md
```

## 🚀 Instalação Rápida

### 1. Requisitos

- Python 3.10-3.13 (recomendado: 3.13)
- 8GB RAM mínimo (16GB recomendado para GPU)
- 10GB de espaço em disco (para modelos)
- GPU NVIDIA (opcional, para aceleração)

### 2. Instalar Dependências (Windows)

Execute o instalador automático:

```bash
execute.bat
# Escolha opção 1 - Instalar dependências
```

Ou instale manualmente:

```bash
pip install PyPDF2>=3.0.0 python-docx>=1.0.0 openpyxl>=3.1.0
pip install sentence-transformers>=2.2.0 chromadb>=0.5.0
pip install gpt4all>=2.0.0
```

### 3. Modelos LLM

**O sistema usa GPT4All por padrão!**

✅ Vantagens:
- Download automático na primeira execução
- 100% Python (sem compiladores)
- 7 modelos disponíveis para escolha
- Gerenciamento integrado no menu

💾 Modelos disponíveis:
1. **Mistral 7B OpenOrca** (3.8 GB) - Recomendado!
2. **Mistral 7B Instruct** (3.8 GB) - Precisão literal
3. **Orca 2 7B** (3.8 GB) - Microsoft, raciocínio lógico
4. **Nous Hermes LLaMA2 13B** (7.3 GB) - Maior qualidade
5. **GPT4All Falcon** (3.9 GB) - Versátil
6. **WizardLM 13B** (7.3 GB) - Análise complexa
7. **Orca Mini 3B** (1.8 GB) - Leve e rápido

## 📖 Uso

### Iniciar o Sistema

```bash
python index.py
```

### Menu Principal

**📚 DOCUMENTOS:**
1. **Indexar documentos**: Processa documentos da pasta `training/`
2. **Fazer pergunta**: Consulta única ao sistema
3. **Modo interativo**: Múltiplas perguntas em sequência
4. **Ver estatísticas**: Informações sobre documentos indexados
5. **Reindexar**: Limpa e recria o índice

**🤖 MODELOS LLM:**
6. **Listar modelos disponíveis**: Ver todos os 7 modelos
7. **Ver detalhes de um modelo**: Informações completas
8. **Selecionar modelo ativo**: Trocar entre modelos

9. **Sair**: Encerra o sistema

### Exemplo de Uso

```python
# O sistema será usado via menu interativo, mas também pode ser usado programaticamente:

from modules.oracle_system import OracleSystem

# Inicializar
oracle = OracleSystem(
    documents_path="training",
    vectorstore_path="src/vectorstore"
)

# Indexar documentos (primeira vez)
oracle.index_documents()

# Fazer perguntas
resposta = oracle.query("O que é desenvolvimento seguro?")
print(resposta)

# Modo interativo
oracle.interactive_mode()
```

## 🔧 Configuração

### Ajustar Parâmetros

Edite os parâmetros em `modules/oracle_system.py`:

```python
# Tamanho dos chunks
text_processor = TextProcessor(chunk_size=500, chunk_overlap=50)

# Número de documentos relevantes por consulta
n_results = 3  # na função query()

# Modelo de embeddings
embedding_generator = EmbeddingGenerator(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
```

## 📚 Adicionando Documentos

1. Coloque seus arquivos PDF, DOCX ou Excel na pasta `training/`
2. Execute o sistema: `python index.py`
3. Escolha opção "1" para indexar os documentos
4. Aguarde o processamento
5. Comece a fazer perguntas!

## 🧪 Teste Inicial

O sistema já inclui um documento de exemplo (`desenvolvimento_seguro.pdf`). Para testar:

```bash
python index.py
# Escolha: 1 (Indexar documentos)
# Escolha: 2 (Fazer pergunta)
# Pergunta: "O que é desenvolvimento seguro?"
```

## ⚙️ Tecnologias Utilizadas

- **Python 3.10-3.13**: Linguagem base
- **PyPDF2**: Leitura de PDFs
- **python-docx**: Leitura de DOCX
- **openpyxl**: Leitura de Excel
- **sentence-transformers**: Embeddings multilíngues (384 dimensões)
- **ChromaDB**: Vector database local
- **GPT4All**: LLMs locais com 7 modelos disponíveis
- **CUDA** (opcional): Aceleração GPU NVIDIA

## 🎯 Casos de Uso

- 📋 Base de conhecimento empresarial
- 📚 Consulta de manuais técnicos
- 📊 Análise de relatórios e planilhas
- 🔍 Busca inteligente em documentação
- 💼 Compliance e políticas internas
- 🎓 Material de treinamento

## 🔐 Privacidade e Segurança

- ✅ **Totalmente Offline**: Seus dados nunca saem da máquina
- ✅ **Sem APIs Externas**: Nenhuma conexão externa necessária
- ✅ **Dados Locais**: Tudo armazenado localmente
- ✅ **Open Source**: Código auditável

## 🐛 Solução de Problemas

### Erro: Dependências faltando
```bash
pip install -r requirements.txt
```

### Erro: Modelo LLM não encontrado
- O sistema funcionará em modo teste
- Para respostas completas, baixe um modelo GGUF

### Erro: Memória insuficiente
- Use um modelo menor (quantizado Q4 ou Q5)
- Reduza o `chunk_size` em `text_processor.py`
- Feche outros aplicativos

### Documentos não são encontrados
- Verifique se estão na pasta `training/`
- Verifique as extensões: .pdf, .docx, .xlsx, .xls

## 📝 Logs

Sistema de logging dual:

**Console (Interface):**
- ✅ Apenas mensagens essenciais para o usuário
- ✅ Indicadores visuais de progresso
- ✅ Warnings e erros críticos

**Arquivos (Detalhado):**
- 📁 Pasta: `logs/`
- 📄 Formato: `oraculo_YYYYMMDD.log` (diário)
- 📊 Conteúdo: Todas as operações, perguntas e respostas completas
- 🔍 Ideal para: debugging, auditoria, análise

**Exemplo:**
```
logs/
├── oraculo_20251217.log
├── oraculo_20251216.log
└── oraculo_20251215.log
```

## 🤝 Contribuições

Este é um sistema profissional e extensível. Áreas para melhorias:

- [ ] Suporte a mais formatos (TXT, MD, CSV)
- [ ] Interface web com Flask/FastAPI
- [ ] Processamento de imagens em PDFs (OCR)
- [ ] Cache de embeddings
- [ ] Suporte a múltiplos idiomas de prompt
- [ ] Exportação de conversas

## 📄 Licença

Este projeto é de código aberto para uso educacional e empresarial.

## 👤 Autor

**Marcus Xavier**
- Sistema desenvolvido com arquitetura limpa e padrões profissionais
- Foco em performance, escalabilidade e manutenibilidade

## 📞 Suporte

Para questões e melhorias, consulte a documentação em `docs/` ou os logs do sistema.

---

**Sistema Oráculo v1.0.0** - Inteligência Artificial Local para Consulta de Documentos 🔮
