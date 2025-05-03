# 📍 Sistema de Empréstimo de Cabos - README.md

```markdown
# 🚀 Sistema de Empréstimo de Cabos

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Flet](https://img.shields.io/badge/Flet-0.1.4-green)

Um sistema completo para gerenciamento de empréstimos de cabos, desenvolvido com Flet (Python) com armazenamento em JSON.

## 📦 Pré-requisitos

- Python 3.7 ou superior
- Biblioteca Flet

```bash
pip install flet
```

## 🏁 Como Executar

1. Salve o código como `emprestimo_cabos.py`
2. Execute:
```bash
python emprestimo_cabos.py
```

## 🎯 Funcionalidades Principais

### ✨ Novo Empréstimo
- Cadastro de colaboradores
- Seleção de cabos disponíveis
- Validação automática de dados

### 🔄 Devolução
- Listagem de cabos emprestados
- Registro de data/hora da devolução
- Atualização automática do status

### 📜 Histórico Completo
- Visualização em cards organizados
- Filtro por status (Ativo/Devolvido)
- Detalhes completos de cada empréstimo

## 🗃️ Estrutura de Dados
Os empréstimos são armazenados em `emprestimos.json`:

```json
[
  {
    "nome": "João Silva",
    "matricula": "12345",
    "numCabo": "3",
    "data": "25/05/2024 14:30",
    "status": "Ativo",
    "dataDevolucao": "26/05/2024 09:15"
  }
]
```

## ⚙️ Configuração

### Alterar Cabos Disponíveis
Modifique no código:
```python
cabos = ["1", "2", "3", "4", "5", "6", "7", "8"]
```

### Personalizar Interface
Edite as cores no AppBar:
```python
page.appbar = ft.AppBar(
    bgcolor="#e02444",  # Cor principal
    title=ft.Text("Empréstimo Cabos DH", color=ft.Colors.WHITE),
)
```

## 📌 Importante

- Os dados são persistidos automaticamente em `emprestimos.json`
- Para resetar os dados, basta excluir o arquivo JSON
- O sistema cria o arquivo automaticamente na primeira execução

## 📞 Suporte

Encontrou problemas? Abra uma issue ou entre em contato:

📧 email@exemplo.com  
🔗 [www.seusite.com](https://www.seusite.com)

---

Desenvolvido com ❤️ por [Seu Nome] - © 2024
```

### Como usar este arquivo:
1. Copie todo o conteúdo acima
2. Crie um novo arquivo chamado `README.md` no mesmo diretório do seu código
3. Cole o conteúdo
4. Salve o arquivo

### Personalizações recomendadas:
- Adicione screenshots reais do sistema (substitua os placeholders)
- Atualize as informações de contato
- Adicione seu nome como autor
- Inclua um logo se disponível

O arquivo está pronto para ser commitado no seu repositório Git!
