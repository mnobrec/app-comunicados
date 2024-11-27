import requests
import pyperclip
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from datetime import datetime
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# ID do seu Gist
GIST_ID = 'ae1eabd4438d174ac45f7b2e50cb37d8'

# Recupera o token do GitHub a partir da variável de ambiente
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if GITHUB_TOKEN is None:
    print("Erro: O token do GitHub não foi encontrado nas variáveis de ambiente.")
else:
    # Função para buscar conteúdo do Gist
    def fetch_gist_content(gist_id):
        url = f"https://api.github.com/gists/{gist_id}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}  # Usando o token para autenticação
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()  # Retorna o conteúdo do Gist
        else:
            print(f"Erro ao buscar conteúdo do Gist: {response.status_code} - {response.text}")
            return None

# Função para extrair links de imagens do conteúdo do Gist
def extract_links(gist_content):
    files = gist_content.get("files", {})
    links = []
    for file in files.values():
        if "content" in file:
            lines = file["content"].splitlines()
            links.extend([line for line in lines if line.startswith("http")])
    return links

# Função para atualizar o Gist com o novo link da imagem
def update_gist_with_link(gist_id, link):
    url = f"https://api.github.com/gists/{gist_id}"
    gist_content = fetch_gist_content(gist_id)
    
    if gist_content:
        files = gist_content.get("files", {})
        file_name = list(files.keys())[0]  # Nome do arquivo para atualizar
        files[file_name]["content"] += f"\n{link}"
        data = {"files": files}
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}  # Usando o token para autenticação
        response = requests.patch(url, json=data, headers=headers)
        
        if response.status_code == 200:
            print("Gist atualizado com sucesso!")
        else:
            print("Erro ao atualizar o Gist:", response.status_code)

class ImageScreen(Screen):
    def __init__(self, image_url, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=0, padding=0)

        img = AsyncImage(source=image_url, allow_stretch=True, keep_ratio=True)
        img.size_hint = (1, 1)
        layout.add_widget(img)

        button = Button(text='Próximo Comunicado', size_hint_y=None, height=50)
        button.bind(on_release=self.next_image)
        layout.add_widget(button)

        self.add_widget(layout)

    def next_image(self, instance):
        app = App.get_running_app()
        current_screen_index = int(self.name)

        if current_screen_index + 1 < len(app.image_links):
            app.sm.current = str(current_screen_index + 1)
        else:
            app.sm.current = '0'  # Volta para a primeira imagem se for a última


class ImageApp(App):
    def build(self):
        current_date = datetime.now().strftime("%d/%m/%Y")
        self.title = f"App Comunicados - {current_date}"
        self.sm = ScreenManager()

        Window.bind(on_request_close=self.close_app) # Vincula o evento de fechar a função de encerramento total do app

        gist_content = fetch_gist_content(GIST_ID)

        if gist_content:
            self.image_links = extract_links(gist_content)
            print("Links encontrados:")
            for link in self.image_links:
                print(link)

            for index, link in enumerate(self.image_links):
                screen = ImageScreen(link, name=str(index))
                self.sm.add_widget(screen)

        # Layout fixo para os botões de atualizar e upload
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # Botão de atualizar (com tamanho igual ao botão de upload)
        update_button = Button(text="ATUALIZAR", size_hint=(0.5, 1))  # Ajustado para dividir igualmente
        update_button.bind(on_release=self.refresh_images)
        button_layout.add_widget(update_button)

        # Botão de upload (com tamanho igual ao botão de atualizar)
        upload_button = Button(text='UPLOAD', size_hint=(0.5, 1))  # Ajustado para dividir igualmente
        upload_button.bind(on_release=self.upload_image)
        button_layout.add_widget(upload_button)

        # Layout principal, que inclui o ScreenManager, a label e os botões
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.sm)  # Adiciona o ScreenManager
        main_layout.add_widget(button_layout)  # Adiciona os botões abaixo do ScreenManager

        return main_layout

    def close_app(self, *args):
        print("Fechando o aplicativo completamente.")
        self.stop()  # Encerra completamente o aplicativo
        return False  # Permite que a janela seja fechada

    def refresh_images(self, instance):
        # Função para atualizar as imagens ao clicar no botão "ATUALIZAR"
        gist_content = fetch_gist_content(GIST_ID)

        if gist_content:
            self.image_links = extract_links(gist_content)
            print("Links encontrados:")
            for link in self.image_links:
                print(link)

            # Atualiza o ScreenManager com as novas imagens
            self.sm.clear_widgets()  # Limpa as telas existentes
            for index, link in enumerate(self.image_links):
                screen = ImageScreen(link, name=str(index))
                self.sm.add_widget(screen)

    def upload_image(self, instance):
        root = Tk()
        root.withdraw()  # Esconde a janela principal do tkinter
        filepath = askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])

        if filepath:

            headers = {"Authorization": "Client-ID ee2d224be4af1b8"}  # Substitua "AAA" pelo seu Client-ID
            with open(filepath, "rb") as image_file:
                files = {"image": image_file}
                response = requests.post("https://api.imgur.com/3/upload", headers=headers, files=files)

            if response.status_code == 200:
                link = response.json()["data"]["link"]
                pyperclip.copy(link)
                messagebox.showinfo("Success", "Upload bem-sucedido!\nLink da imagem copiado para a área de transferência.")
                print("Link direto da imagem:", link)

                # Atualiza o Gist com o novo link
                update_gist_with_link(GIST_ID, link)
            else:
                messagebox.showerror("Error", f"Erro no upload: {response.status_code}\n{response.text}")

        root.destroy()

# Executa o aplicativo
if __name__ == "__main__":
    ImageApp().run()