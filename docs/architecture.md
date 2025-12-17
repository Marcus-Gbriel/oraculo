# Arquitetura do Sistema Oráculo

## 🏛️ Visão Geral

O Sistema Oráculo utiliza uma arquitetura moderna de RAG (Retrieval Augmented Generation) implementada de forma totalmente local, seguindo princípios de Clean Architecture e SOLID.

## 📐 Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                        index.py                             │
│                   (Entry Point / CLI)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  modules/oracle_system.py                   │
│              (Orchestrator / RAG Pipeline)                  │
└──────┬──────────┬──────────┬──────────┬─────────┬───────────┘
       │          │          │          │         │
       ▼          ▼          ▼          ▼         ▼
┌──────────┐ ┌────────┐ ┌─────────┐ ┌────────┐ ┌────┐
│ Document │ │  Text  │ │Embedding│ │ Vector │ │LLM │
│  Loader  │ │Processor│ │Generator│ │ Store  │ │    │
└──────────┘ └────────┘ └─────────┘ └────────┘ └────┘
     │            │          │           │         │
     ▼            ▼          ▼           ▼         ▼
┌──────────┐ ┌────────┐ ┌─────────┐ ┌────────┐ ┌────┐
│  PyPDF2  │ │  Regex │ │sentence-│ │Chroma  │ │llama│
│   docx   │ │ String │ │transfor-│ │  DB    │ │.cpp│
│ openpyxl │ │  Ops   │ │  mers   │ │        │ │    │
└──────────┘ └────────┘ └─────────┘ └────────┘ └────┘
```

## 🔄 Fluxo de Dados

### 1. Fase de Indexação

```
Documentos (PDF/DOCX/Excel)
         ↓
   DocumentLoader
         ↓
   Texto Extraído
         ↓
   TextProcessor (Chunking)
         ↓
   Chunks de Texto
         ↓
   EmbeddingGenerator
         ↓
   Vetores (Embeddings)
         ↓
   VectorStore (ChromaDB)
         ↓
   Base de Conhecimento Indexada
```

### 2. Fase de Consulta (Query)

```
Pergunta do Usuário
         ↓
   EmbeddingGenerator
         ↓
   Vetor da Pergunta
         ↓
   VectorStore.search()
         ↓
   Top-K Documentos Relevantes
         ↓
   LocalLLM.create_prompt_with_context()
         ↓
   Prompt Contextualizado
         ↓
   LocalLLM.generate()
         ↓
   Resposta Final
```

## 🧩 Componentes Principais

### 1. index.py (Entry Point)

**Responsabilidades:**
- Interface CLI do usuário
- Verificação de dependências
- Inicialização do sistema
- Menu interativo
- Tratamento de erros globais

**Padrões:**
- Single Responsibility Principle
- Command Pattern (menu)

### 2. oracle_system.py (Orchestrator)

**Responsabilidades:**
- Coordenação de todos os módulos
- Pipeline RAG completo
- Gerenciamento de estado
- API pública do sistema

**Padrões:**
- Facade Pattern
- Pipeline Pattern
- Dependency Injection

**Métodos Públicos:**
```python
__init__(documents_path, vectorstore_path, model_path, use_simple_llm)
index_documents(force_reindex)
query(question, n_results, show_sources)
interactive_mode()
get_stats()
```

### 3. document_loader.py (Data Ingestion)

**Responsabilidades:**
- Leitura de múltiplos formatos
- Extração de texto
- Tratamento de erros por arquivo
- Logging de progresso

**Formatos Suportados:**
- PDF (PyPDF2)
- DOCX (python-docx)
- Excel XLSX/XLS (openpyxl)

**Interface:**
```python
DocumentLoader(documents_path)
load_pdf(file_path) -> str
load_docx(file_path) -> str
load_excel(file_path) -> str
load_all_documents() -> List[Dict]
```

### 4. text_processor.py (Text Processing)

**Responsabilidades:**
- Limpeza de texto
- Chunking com overlap
- Manutenção de contexto
- Metadados por chunk

**Estratégia de Chunking:**
- Tamanho configurável (default: 500 chars)
- Overlap configurável (default: 50 chars)
- Quebra em espaços (não corta palavras)
- Preserva metadados de origem

**Interface:**
```python
TextProcessor(chunk_size, chunk_overlap)
clean_text(text) -> str
split_into_sentences(text) -> List[str]
create_chunks(text, metadata) -> List[Dict]
process_documents(documents) -> List[Dict]
```

### 5. embedding_generator.py (Embeddings)

**Responsabilidades:**
- Geração de embeddings semânticos
- Cache de modelo
- Processamento em batch
- Suporte multilíngue

**Modelo Padrão:**
- `paraphrase-multilingual-MiniLM-L12-v2`
- 384 dimensões
- Suporta 50+ idiomas incluindo português

**Interface:**
```python
EmbeddingGenerator(model_name)
generate_embedding(text) -> np.ndarray
generate_embeddings_batch(texts, batch_size) -> List[np.ndarray]
```

### 6. vector_store.py (Vector Database)

**Responsabilidades:**
- Armazenamento persistente de vetores
- Busca por similaridade (cosine)
- Gerenciamento de coleções
- Batch operations

**Tecnologia:**
- ChromaDB (vector database local)
- Distância: Cosine Similarity
- Persistência em disco

**Interface:**
```python
VectorStore(persist_directory, collection_name)
add_documents(chunks, embeddings)
search(query_embedding, n_results) -> List[Dict]
clear_collection()
get_collection_stats() -> Dict
```

### 7. llm.py (Language Models)

**Responsabilidades:**
- Gerenciamento de múltiplos tipos de LLM
- Geração de respostas
- Criação de prompts contextualizados
- Detecção e uso de GPU
- Fallback automático entre modelos

**Modelos Suportados:**
- **GPT4AllLLM** (Padrão): 7 modelos pré-configurados
- **LocalLLM**: llama-cpp-python (legado)
- **SimpleLLM**: Modo teste

**Otimizações:**
- Temperature: 0.2 (precisão)
- GPU auto-detection (CUDA)
- Multi-threading CPU
- Batch processing (n_batch=256)

**Interface:**
```python
GPT4AllLLM(model_name, temperature, max_tokens, use_gpu)
generate(prompt, max_tokens, temperature) -> str
create_prompt_with_context(question, context_documents) -> str
detect_gpu() -> bool
```

### 8. model_manager.py (Model Management)

**Responsabilidades:**
- Gerenciamento de modelos LLM disponíveis
- Persistência de configurações (config.json)
- Listagem e seleção de modelos
- Validação de modelos instalados

**Modelos Disponíveis:**
1. Mistral 7B OpenOrca (3.8 GB)
2. Mistral 7B Instruct (3.8 GB)
3. Orca 2 7B (3.8 GB)
4. Nous Hermes LLaMA2 13B (7.3 GB)
5. GPT4All Falcon (3.9 GB)
6. WizardLM 13B (7.3 GB)
7. Orca Mini 3B (1.8 GB)

**Configuração (config.json):**
```json
{
  "selected_model": "mistral-7b-openorca.Q4_0.gguf",
  "temperature": 0.2,
  "max_tokens": 512
}
```

**Interface:**
```python
ModelManager(models_dir, config_file)
get_installed_models() -> List[str]
get_selected_model() -> str
set_selected_model(model_name)
list_available_models() -> Dict
print_all_models()
print_model_info(model_file)
```

## 🎯 Padrões de Design Utilizados

### 1. Facade Pattern
- `OracleSystem` como facade para todo o sistema
- Simplifica interface complexa

### 2. Strategy Pattern
- `LocalLLM` vs `SimpleLLM`
- Diferentes estratégias de geração

### 3. Template Method
- `DocumentLoader` com métodos específicos por formato
- Estrutura comum com variações

### 4. Dependency Injection
- Componentes injetados no `OracleSystem`
- Facilita testes e manutenção

### 5. Single Responsibility
- Cada módulo tem uma responsabilidade clara
- Alto coesão, baixo acoplamento

## 📊 Fluxo de Dados Detalhado

### Indexação (Primeira Execução)

```python
# 1. Carregar documentos
docs = DocumentLoader("training").load_all_documents()
# Output: [{'filename': 'doc.pdf', 'content': '...', 'path': '...'}]

# 2. Processar em chunks
processor = TextProcessor(chunk_size=500, chunk_overlap=50)
chunks = processor.process_documents(docs)
# Output: [{'text': '...', 'metadata': {...}, 'chunk_index': 0}]

# 3. Gerar embeddings
embedder = EmbeddingGenerator()
embeddings = embedder.generate_embeddings_batch([c['text'] for c in chunks])
# Output: [array([0.1, 0.2, ...]), ...]  # 384 dimensões

# 4. Armazenar
vector_store = VectorStore("src/vectorstore")
vector_store.add_documents(chunks, embeddings)
# Persistido em disco automaticamente
```

### Consulta (Query)

```python
# 1. Receber pergunta
question = "O que é desenvolvimento seguro?"

# 2. Gerar embedding da pergunta
q_embedding = embedder.generate_embedding(question)
# Output: array([0.15, 0.23, ...])  # 384 dimensões

# 3. Buscar documentos similares
relevant_docs = vector_store.search(q_embedding, n_results=3)
# Output: [
#   {'text': '...', 'metadata': {...}, 'distance': 0.23},
#   {'text': '...', 'metadata': {...}, 'distance': 0.31},
#   {'text': '...', 'metadata': {...}, 'distance': 0.35}
# ]

# 4. Criar prompt contextualizado
prompt = llm.create_prompt_with_context(question, relevant_docs)
# Output: "<s>[INST] ... Contexto: ... Pergunta: ... [/INST]"

# 5. Gerar resposta
response = llm.generate(prompt)
# Output: "Desenvolvimento seguro é..."
```

## 💾 Persistência

### Vector Store
- **Local**: `src/vectorstore/`
- **Formato**: SQLite + arquivos binários (ChromaDB)
- **Tamanho**: ~1-5KB por chunk

### Logs
- **Local**: `oraculo.log`
- **Rotação**: Manual
- **Formato**: Timestamp + Level + Message

### Modelos
- **Embeddings**: Cache automático em `~/.cache/torch/`
- **LLM**: `src/models/*.gguf` (usuário fornece)

## 🔒 Segurança e Privacidade

### Princípios
1. **Dados Locais**: Nunca saem da máquina
2. **Sem Telemetria**: ChromaDB configurado sem telemetria
3. **Sem Rede**: Funciona 100% offline após instalação
4. **Open Source**: Código auditável

### Considerações
- Documentos ficam em `training/` (não criptografados)
- Vector store não é criptografado
- Logs podem conter trechos de documentos
- Para ambiente de produção, considere criptografia de disco

## ⚡ Performance

### Otimizações

1. **Batch Processing**
   - Embeddings gerados em batches de 32
   - Reduz overhead de chamadas ao modelo

2. **Vector Search**
   - HNSW (Hierarchical Navigable Small World)
   - Complexidade O(log n) para busca

3. **Chunking Inteligente**
   - Quebra em espaços (mantém palavras completas)
   - Overlap preserva contexto

4. **Lazy Loading**
   - Modelos carregados apenas quando necessário
   - Cache automático de embeddings

### Benchmarks Típicos

| Operação | Tempo | Hardware |
|----------|-------|----------|
| Indexar 10 PDFs (100 páginas) | 2-5 min | CPU i5, 8GB RAM |
| Gerar embedding de query | 50-200ms | CPU i5 |
| Busca no vector store | 10-50ms | 1000 docs |
| Gerar resposta LLM | 5-30s | CPU i5 (Q4 model) |

## 🧪 Testes

### Estrutura Sugerida

```
tests/
├── test_document_loader.py
├── test_text_processor.py
├── test_embedding_generator.py
├── test_vector_store.py
├── test_llm.py
└── test_oracle_system.py
```

### Testes Unitários

```python
# Exemplo
def test_document_loader():
    loader = DocumentLoader("test_data")
    docs = loader.load_all_documents()
    assert len(docs) > 0
    assert 'content' in docs[0]
```

### Testes de Integração

```python
def test_full_pipeline():
    oracle = OracleSystem("test_data")
    oracle.index_documents()
    response = oracle.query("teste")
    assert response is not None
```

## 🔄 Extensibilidade

### Adicionar Novo Formato de Documento

```python
# Em document_loader.py
def load_txt(self, file_path: Path) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Adicionar ao __init__
self.supported_formats = ['.pdf', '.docx', '.xlsx', '.xls', '.txt']

# Adicionar ao load_all_documents
elif file_path.suffix.lower() == '.txt':
    content = self.load_txt(file_path)
```

### Trocar Vector Database

```python
# Criar novo módulo: modules/faiss_store.py
class FAISSStore:
    def __init__(self, persist_directory):
        # Implementação com FAISS
        pass
    
    def add_documents(self, chunks, embeddings):
        pass
    
    def search(self, query_embedding, n_results):
        pass
```

### Adicionar Novo Modelo de Embeddings

```python
# Em embedding_generator.py
class HuggingFaceEmbedding(EmbeddingGenerator):
    def __init__(self):
        from transformers import AutoModel, AutoTokenizer
        self.model = AutoModel.from_pretrained("model-name")
        self.tokenizer = AutoTokenizer.from_pretrained("model-name")
```

## 📈 Escalabilidade

### Limites Atuais
- **Documentos**: Até ~10.000 documentos (depende do tamanho)
- **Chunks**: Até ~100.000 chunks no vector store
- **Memória LLM**: 4-16GB dependendo do modelo

### Para Escalar
1. Usar PostgreSQL + pgvector ao invés de ChromaDB
2. Implementar sharding de collections
3. Usar GPU para embeddings e LLM
4. Adicionar cache de respostas
5. Implementar processamento assíncrono

## 🎓 Conceitos Técnicos

### RAG (Retrieval Augmented Generation)
Técnica que combina:
1. **Retrieval**: Busca de informação relevante
2. **Augmentation**: Enriquecimento do prompt
3. **Generation**: Geração de resposta contextualizada

### Embeddings
Representação vetorial de texto que captura significado semântico:
- Textos similares = vetores próximos
- Permite busca por similaridade
- Multilíngue: mesmo espaço vetorial para vários idiomas

### Vector Database
Banco de dados otimizado para busca de similaridade:
- Índices especializados (HNSW, IVF)
- Métricas de distância (cosine, euclidean)
- Busca aproximada (ANN - Approximate Nearest Neighbors)

### Quantização (GGUF)
Redução de precisão de modelos LLM:
- FP16 → INT8/INT4 (Q4, Q5, Q8)
- Reduz tamanho e requisitos de memória
- Pequena perda de qualidade

## 📚 Referências

- **sentence-transformers**: https://www.sbert.net/
- **ChromaDB**: https://docs.trychroma.com/
- **llama.cpp**: https://github.com/ggerganov/llama.cpp
- **RAG**: https://arxiv.org/abs/2005.11401
- **HNSW**: https://arxiv.org/abs/1603.09320

---

**Sistema Oráculo v1.0.0** - Arquitetura Profissional para RAG Local
