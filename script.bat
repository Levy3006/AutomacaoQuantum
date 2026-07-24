@echo off

REM Entra na pasta onde o .bat está localizado.
pushd "%~dp0"

REM Define uma pasta local fixa no computador de cada usuário para o ambiente virtual
set "LOCAL_VENV=%USERPROFILE%\.venv_automacao_quantum"

if not exist "%LOCAL_VENV%\Scripts\activate" (
    echo Criando ambiente virtual local em %LOCAL_VENV%...

    python -m venv "%LOCAL_VENV%"

    if errorlevel 1 (
        echo Erro ao criar o ambiente virtual. Certifique-se de que o Python esta instalado e no PATH.
        popd
        pause
        exit /b 1
    )

    call "%LOCAL_VENV%\Scripts\activate"

    echo Instalando dependencias do requirements.txt...
    pip install -r requirements.txt

    if errorlevel 1 (
        echo Erro ao instalar dependencias.
        popd
        pause
        exit /b 1
    )
) else (
    call "%LOCAL_VENV%\Scripts\activate"
)

echo Executando o script principal...
python main.py

REM Desativa o ambiente virtual e volta para o diretorio original
call deactivate
popd

pause