# Como rodar o arquivo .ipynb

1. Criar um ambiente virtual python
    > python -m venv ./venv

1. Ativar o ambiente virtual
    > venv/Scripts/Activate

1. Instalar as bibliotecas
    > pip install -r .\Trabalho-Algoritmo-Genético\requirements.txt

1. Rodar uma célula
    - Ao tentar rodar uma célula, o VSCode vai pedir um caminho para um executável do Python. Escolher a opção "Python Enviroments" e em seguida, procurar pela opção que leve ao executável do ambiente virtual, ou seja, a opção em que o path possua "venv/Scripts/"

    - Talvez o VSCode solicite a instalação de dependências para o kernel, só aceita

1. Estrutura de um Notebook (arquivo .ipynb)
    - Células de texto
        - Células escritas com Markdown
        - Não são executadas (tipo comentários)

    - Células de código
        - Células onde são escritos os códigos em Python
        - Cada célula é executada individualmente
        - É possível acessar variáveis criadas em outra célula, desde que a célula contendo a variável já tenha sido executada