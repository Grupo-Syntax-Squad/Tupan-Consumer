# Serviço de recepção de dados para a aplicação Tupan

## Pré requisitos
- Python
- Redis
- PostgreSQL

## Criando e ativando o ambiente virtual (Opcional)
```bash
python -m venv .venv & ./.venv/Scripts/activate
```

[!WARNING] É possível que a política de execução de scripts do Windows impossibilite a criação do ambiente virtual, caso aconteça segue o artigo sobre políticas de execução: [https://learn.microsoft.com/pt-br/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4](https://learn.microsoft.com/pt-br/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4)

## Instalando dependências
```bash
pip install -r ./requirements.txt
```

## Variáveis de ambiente
Copie o arquivo .env_sample e adapte os valores das variáveis de ambiente para seu ambiente de execução.
```bash
cp ./.env_sample ./.env
```