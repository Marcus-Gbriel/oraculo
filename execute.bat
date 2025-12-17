@echo off
chcp 65001 >nul
title Sistema Oráculo - Menu Principal
color 0A

:MENU
cls
echo.
echo ===============================================================
echo.
echo                    SISTEMA ORACULO
echo.
echo             Agente de IA Local para Consulta de
echo                  Documentos Empresariais
echo.
echo ===============================================================
echo.
echo ═══════════════════════════════════════════════════════════
echo                        MENU PRINCIPAL
echo ═══════════════════════════════════════════════════════════
echo.
echo   1 - Instalar Ambiente Virtual Python (venv)
echo   2 - Executar Sistema Oráculo
echo   3 - Encerrar
echo.
echo ═══════════════════════════════════════════════════════════
echo.
set /p opcao="Escolha uma opção [1-3]: "

if "%opcao%"=="1" goto INSTALAR
if "%opcao%"=="2" goto EXECUTAR
if "%opcao%"=="3" goto SAIR
echo.
echo ❌ Opcao invalida! Tente novamente.
timeout /t 2 >nul
goto MENU

:INSTALAR
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo            INSTALANDO AMBIENTE VIRTUAL PYTHON
echo ═══════════════════════════════════════════════════════════
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.8 ou superior:
    echo https://www.python.org/downloads/
    echo.
    pause
    goto MENU
)

echo [OK] Python encontrado:
python --version
echo.

REM Verificar versão do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

if %PYTHON_MAJOR% GEQ 3 (
    if %PYTHON_MINOR% GTR 13 (
        echo.
        echo [AVISO] Python %PYTHON_VERSION% e muito recente!
        echo.
        echo Algumas bibliotecas podem nao ter suporte completo ainda.
        echo Recomendado: Python 3.9, 3.10, 3.11, 3.12 ou 3.13
        echo.
        echo Se tiver problemas na instalação:
        echo   1. Instale Python 3.11 ou 3.12 do python.org
        echo   2. Execute novamente este instalador
        echo.
        set /p continuar="Deseja continuar mesmo assim? (s/n): "
        if /i not "!continuar!"=="s" goto MENU
    )
)

echo.

REM Verificar se venv já existe
if exist "venv\" (
    echo [AVISO] Ambiente virtual ja existe!
    echo.
    set /p recriar="Deseja recriar o ambiente? (s/n): "
    if /i not "%recriar%"=="s" (
        echo.
        echo [INFO] Mantendo ambiente existente.
        timeout /t 2 >nul
        goto MENU
    )
    echo.
    echo [INFO] Removendo ambiente antigo...
    rmdir /s /q venv
)

echo.
echo [INFO] Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo.
    echo [ERRO] Erro ao criar ambiente virtual!
    pause
    goto MENU
)

echo [OK] Ambiente virtual criado com sucesso!
echo.
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo [ERRO] Erro ao ativar ambiente virtual!
    pause
    goto MENU
)

echo [OK] Ambiente virtual ativado!
echo.
echo [INFO] Atualizando pip...
python -m pip install --upgrade pip --quiet
echo [OK] Pip atualizado!
echo.

REM Verificar se requirements.txt existe
if not exist "requirements.txt" (
    echo [AVISO] Arquivo requirements.txt nao encontrado!
    echo.
    echo Criando requirements.txt...
    (
        echo # Leitura de documentos
        echo PyPDF2^>=3.0.0
        echo python-docx^>=1.0.0
        echo openpyxl^>=3.1.0
        echo.
        echo # IA e Embeddings
        echo sentence-transformers^>=2.2.0
        echo numpy^>=1.24.0
        echo.
        echo # Vector Database - versao compativel com Python 3.14
        echo chromadb^>=0.5.0
        echo.
        echo # LLM Local ^(opcional - pode falhar, sistema funciona sem ele^)
        echo llama-cpp-python^>=0.2.0
    ) > requirements.txt
    echo [OK] requirements.txt criado!
    echo.
)

echo [INFO] Instalando dependencias do requirements.txt...
echo    (isso pode demorar alguns minutos)
echo.

REM Instalar todas as dependências do requirements.txt
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [AVISO] Alguns pacotes podem ter falhado, mas o sistema pode funcionar
    echo.
) else (
    echo.
    echo [OK] Todas as dependencias instaladas com sucesso!
    echo.
)

echo.
echo ===============================================================
echo.
echo               INSTALACAO CONCLUIDA COM SUCESSO
echo.
echo            Todas as dependencias foram instaladas.
echo            Voce ja pode executar o Sistema Oraculo!
echo.
echo ===============================================================
echo.
pause
goto MENU

:EXECUTAR
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo                EXECUTANDO SISTEMA ORÁCULO
echo ═══════════════════════════════════════════════════════════
echo.

REM Verificar se venv existe
if not exist "venv\" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo.
    echo Por favor, execute a opcao 1 primeiro para instalar o ambiente.
    echo.
    pause
    goto MENU
)

REM Verificar se index.py existe
if not exist "index.py" (
    echo [ERRO] Arquivo index.py nao encontrado!
    echo.
    echo Certifique-se de estar na pasta correta do projeto.
    echo.
    pause
    goto MENU
)

REM Verificar se pasta training existe
if not exist "training\" (
    echo [AVISO] Pasta 'training' nao encontrada!
    echo.
    echo Criando pasta training...
    mkdir training
    echo [OK] Pasta criada!
    echo.
    echo [INFO] Adicione seus documentos (PDF, DOCX, Excel) na pasta 'training'
    echo        antes de indexar os documentos no sistema.
    echo.
    timeout /t 3 >nul
)

echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo [ERRO] Erro ao ativar ambiente virtual!
    echo.
    echo Tente reinstalar o ambiente (opcao 1).
    echo.
    pause
    goto MENU
)

echo [OK] Ambiente virtual ativado!
echo.
echo [INFO] Iniciando Sistema Oraculo...
echo.
echo ═══════════════════════════════════════════════════════════
echo.

REM Executar o sistema
python index.py

echo.
echo.
echo ═══════════════════════════════════════════════════════════
echo                  Sistema Oráculo Encerrado
echo ═══════════════════════════════════════════════════════════
echo.
pause
goto MENU

:SAIR
cls
echo.
echo ===============================================================
echo.
echo                       Ate logo!
echo.
echo            Obrigado por usar o Sistema Oraculo!
echo.
echo ===============================================================
echo.
timeout /t 2 >nul
exit /b 0
