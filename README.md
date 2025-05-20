# AutoWhats

O **AutoWhats** é uma aplicação desenvolvida em Python com interface gráfica (Tkinter) para envio automatizado de mensagens via WhatsApp Web. A automação utiliza o Selenium WebDriver e permite gerenciar uma base de contatos localmente com SQLite, organizando-os por cidade e facilitando o envio em massa ou individual.

---

## 🚀 Como Usar

1. **Instale os requisitos**:
   
   Certifique-se de ter o Python 3 instalado e execute:

   pip install selenium tkinter sqlite3 

   
3. **Configure o WebDriver:**
   
    Baixe o ChromeDriver compatível com sua versão do Google Chrome e coloque-o no mesmo diretório do script ou no PATH do sistema.


4. Execute o programa:
   
   Basta rodar o arquivo .py para abrir a interface:
   
   python autowhats.py


## 🧩 Banco de Dados (contatos.db)

A base de dados utilizada é um arquivo SQLite chamado contatos.db. Se não existir, ele é automaticamente criado na primeira execução, contendo a tabela:

``sql``

CREATE TABLE contatos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cidade TEXT,
    nome TEXT,
    telefone TEXT,
    mensagem TEXT
);


## 📇 Formato dos Contatos
Telefone: Deve estar no formato internacional sem espaços ou símbolos, por exemplo:

✅ Correto: 5531999998888

❌ Incorreto: (31) 99999-8888


Mensagem personalizada (opcional):

Ao adicionar um contato, você pode inserir uma mensagem única para ele.

Se deixada em branco, o programa utilizará a mensagem padrão digitada na interface no momento do envio.



## ✅ Funcionalidades

✅ Adicionar novos contatos por cidade, nome, telefone e mensagem opcional.

✅ Excluir contatos por ID.

✅ Selecionar e desmarcar todos com um clique.

✅ Enviar mensagens individuais em lote com base na seleção.



## 🛑 Avisos

Esta ferramenta exige que o WhatsApp Web esteja logado no navegador controlado pelo Selenium.

A automação depende da estabilidade da interface do WhatsApp Web. Pequenas mudanças no site podem quebrar a funcionalidade.



## 📚 Passo a Passo para Utilizar

### 1. Inicie o programa

Execute o script principal com o Python:

python autowhats.py


### 2. Digite a mensagem padrão no campo de texto da interface.

Marque os contatos desejados (ou clique em "Selecionar Todos").

Clique em "Enviar Mensagens".


### 3. Faça loggin no WhatsApp Web

Ao clicar em "Enviar Mensagens", o navegador será aberto automaticamente.

Use seu celular para escanear o QR Code e fazer login no WhatsApp Web.

Após o login, clique em "OK" na caixa de diálogo da interface.

O sistema abrirá uma conversa por vez no WhatsApp Web e enviará a mensagem (padrão ou personalizada).

Ao finalizar todos os envios, o navegador será fechado automaticamente.


## 👨‍💻 Autor

Desenvolvido por Lucas Costa

🔗 [LinkedIn](https://www.linkedin.com/in/lucas-de-freitas-costa/)

##📄 Licença

Este projeto é de uso privado ou interno, salvo autorização. Consulte o autor para fins comerciais.
