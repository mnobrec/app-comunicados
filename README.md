# app-comunicados - README

## Descrição

Este projeto é um aplicativo Kivy para visualização e gerenciamento de imagens carregadas em um Gist do GitHub. Ele permite a visualização de imagens de um Gist, com a funcionalidade de avançar para a próxima imagem. Além disso, oferece a possibilidade de atualizar o Gist com novos links de imagens e fazer upload de novas imagens usando a API do Imgur.

## Funcionalidades

1. **Visualização de Imagens:**
   - O aplicativo recupera links de imagens de um Gist do GitHub e exibe as imagens de forma sequencial.
   - Um botão de "Próximo Comunicado" permite navegar pelas imagens do Gist.

2. **Upload de Imagens:**
   - Observação: Esta funcionalidade só está habilitada para a versão do adm (esta) visto que a versão do visualizador não permite upar imagens, apenas vê-las.
   - O aplicativo permite que o usuário admnistrador faça o upload de imagens para o Imgur e copie o link da imagem para a área de transferência.
   - O link gerado é adicionado ao Gist, atualizando seu conteúdo.

3. **Atualização de Gist:**
   - Você pode atualizar o Gist com links de novas imagens ao fazer upload de uma imagem usando a API do Imgur.
   - Após o upload, o link da imagem é copiado para a área de transferência e o Gist é atualizado com o novo link.

## Dependências

Este projeto requer as seguintes bibliotecas:

- `requests`: Para realizar chamadas HTTP (instalação: `pip install requests`).
- `pyperclip`: Para copiar o link da imagem para a área de transferência (instalação: `pip install pyperclip`).
- `tkinter`: Para criar a interface gráfica para o upload de imagens.
- `kivy`: Para criar a interface gráfica principal do aplicativo (instalação: `pip install kivy`).
- `python-dotenv`: Para carregar variáveis de ambiente a partir de um arquivo `.env` (instalação: `pip install python-dotenv`).

## Variáveis de Ambiente

Antes de rodar o aplicativo, crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

- `GITHUB_TOKEN`: O token de autenticação do GitHub para acessar o Gist. Você pode obter um token de acesso pessoal no GitHub [aqui](https://github.com/settings/tokens).

Exemplo de arquivo `.env`:

```dotenv
GITHUB_TOKEN=seu_token_do_github (sem aspas)
```

## Como Usar

1. Clone ou faça o download do repositório.
2. Instale as dependências mencionadas acima.
3. Crie e configure o arquivo `.env` com seu token do GitHub.
4. Execute o aplicativo com o comando:

   ```bash
   python app.py
   ```

5. O aplicativo será iniciado e exibirá as imagens do Gist de forma sequencial. Você pode clicar em "Próximo Comunicado" para avançar para a próxima imagem.

6. Para fazer o upload de novas imagens para o Imgur, clique em "UPLOAD", escolha uma imagem do seu computador e aguarde o upload ser concluído. O link da imagem será copiado para a área de transferência e o Gist será atualizado.
7. Se desejar atualizar o Gist com novos links, clique em "ATUALIZAR".

## Estrutura do Projeto

O projeto possui a seguinte estrutura:

```
.
├── main.py                   #(Arquivo principal com o código do aplicativo)
├── .env                      #(Arquivo de configuração para variáveis de ambiente)
└── requirements.txt          #(Arquivo com as dependências do projeto)
```

## Como Contribuir

1. Faça um fork deste repositório.
2. Crie uma nova branch para suas alterações.
3. Envie um pull request com suas alterações.

## Notas Finais

- **Versão Administrador:** Esta versão do aplicativo permite ao usuário não só visualizar os comunicados, mas também fazer upload de novas imagens e atualizar os links do Gist com as imagens carregadas. Ideal para administradores ou usuários que precisam gerenciar o conteúdo do Gist.
- **Versão do Usuário Final:** Em contrapartida, a versão para o usuário final permite apenas visualizar as imagens dos comunicados e atualizar a lista de imagens a partir do Gist, mas não possibilita o upload de novas imagens.
- Certifique-se de que o seu Gist está configurado corretamente e contém links válidos para as imagens.
- O aplicativo foi desenvolvido para ser simples e direto, mas pode ser expandido com novas funcionalidades, como exibição em tela cheia ou suporte a outros serviços de armazenamento de imagens.
