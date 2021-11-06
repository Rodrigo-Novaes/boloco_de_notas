import os
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog, messagebox

class Notepad:
    app = Tk()
    areaTexto = Text(app, wrap='none', font='Consolas 11', bg='#F8F8FF', undo=True)
    # Construcão de Menu Arquivo
    barraDeMenus = Menu(app)
    menu_arquivo = Menu(barraDeMenus, tearoff=0)
    # Construcão de Menu Editar
    menu_editar = Menu(barraDeMenus, tearoff=0)
    # Construcão de Menu Ajuda
    menu_ajuda = Menu(barraDeMenus, tearoff=0)
    # Barra de Rolagem Vertical
    sb = Scrollbar(areaTexto, orient=VERTICAL)
    # Barra de Rolagem Horizontal
    sb1 = Scrollbar(areaTexto, orient=HORIZONTAL)
    # Variavel
    file = None


    def __init__(self, **kwargs):
        # Defina o texto da janela
        self.app.title('Sem título - Bloco de Notas')

        # Definir tamanho e posição janela
        self.app.geometry('500x300+300+130')
        self.app.protocol('WM_DELETE_WINDOW', self.saircadastro)
        # Configuração cor de fundo da janela
        self.app.configure(bg='#6A5ACD')

        # Area de digitação do texto
        self.areaTexto.pack(padx=1, pady=1, expand=True, fill='both')

        #Construção do menu arquivo
        self.menu_arquivo.add_command(label='Novo                       Ctrl+N', command=self.newFile)
        self.app.bind('<Control-Key-n>', self.newFile)
        self.menu_arquivo.add_command(label='Abrir...                     Ctrl+O', command=self.openFile)
        self.app.bind('<Control-Key-o>', self.openFile)
        self.menu_arquivo.add_command(label='Salvar                       Ctrl+S', command=self.saveFile)
        self.app.bind('<Control-Key-s>', self.saveFile)
        self.menu_arquivo.add_command(label='Salvar como...', command=self.saveAsFile)
        # Separado entre os Menus
        self.menu_arquivo.add_separator()
        self.menu_arquivo.add_command(label='Sair', command=self.saircadastro)
        self.barraDeMenus.add_cascade(label='Arquivo', menu=self.menu_arquivo)
        # Construção do menu editar
        self.menu_editar.add_command(label='Desfazer         Ctrl+Z', command=self.desfazer)
        self.app.bind('<Control-Key-z>', self.desfazer)
        self.menu_editar.add_command(label='Refazer           Ctrl+Y', command=self.refazer)
        self.app.bind('<Control-Key-y>', self.refazer)
        self.menu_editar.add_command(label='Cortar             Ctrl+X', command=self.cortar)
        self.app.bind('<Control-Key-x>', self.cortar)
        self.menu_editar.add_command(label='Copiar            Ctrl+C', command=self.copiar)
        self.app.bind('<Control-Key-c>', self.copiar)
        self.menu_editar.add_command(label='Colar               Ctrl+V', command=self.colar)
        self.app.bind('<Control-Key-v>', self.colar)
        self.barraDeMenus.add_cascade(label='Editar', menu=self.menu_editar)
        # Construção do menu Ajuda
        self.menu_ajuda.add_command(label='Sobre               ', command=self.showAbout)
        self.barraDeMenus.add_cascade(label='Ajuda', menu=self.menu_ajuda)
        # Mostrar os menus na janela
        self.app.config(menu=self.barraDeMenus)


        # Barra de Rolagem Vertical
        self.sb.pack(side=RIGHT, fill=Y)
        self.sb.configure(command=self.areaTexto.yview)
        self.areaTexto.configure(yscrollcommand=self.sb.set)

        # Barra de Rolagem Horizontal
        self.sb1.pack(side=BOTTOM, fill=X)
        self.sb1.configure(command=self.areaTexto.xview)
        self.areaTexto.configure(xscrollcommand=self.sb1.set)

    def semComando(self):
        pass

    def openFile(self, event=None):

        self.file = filedialog.askopenfilename(initialfile='*.txt', defaultextension='.txt',
                                    filetype=[('Documentos de texto', '.txt'),
                                            ('Todos arquivos', '*.*')])

        if self.file == '':
            self.file = None
        else:
            self.app.title(os.path.basename(self.file) + " - Bloco de Notas")
            self.areaTexto.delete(1.0, END)

            file = open(self.file, 'r')

            self.areaTexto.insert(1.0, file.read())

            file.close()

    def newFile(self, event=None):
        self.app.title('Sem título - Bloco de Notas')
        self.file = None
        self.areaTexto.delete(1.0, END)

    def saveFile(self, event=None):
        if self.file == None:
            # Save as new file
            self.file = filedialog.asksaveasfilename(initialfile='*.txt', defaultextension='.txt',
                                    filetype=[('Documentos de texto', '.txt'),
                                            ('Todos arquivos', '*.*')])

            if self.file == '':
                self.file = None
            else:
                file = open(self.file, 'w')
                file.write(self.areaTexto.get(1.0, END))
                file.close()


                self.app.title(os.path.basename(self.file) + ' - Bloco de Notas')


        else:
            file = open(self.file, 'w')
            file.write(self.areaTexto.get(1.0, END))
            file.close()

    def saveAsFile(self, event=None):

        self.new_as_file = filedialog.asksaveasfilename(initialfile='*.txt', defaultextension='.txt',
                                                   filetype=[('Documentos de texto', '.txt'),
                                                             ('Todos arquivos', '*.*')])
        if self.new_as_file == '':
            self.new_as_file = None
        else:
            self.new_as_file = open(self.new_as_file, "w")
            self.new_as_file.write(self.areaTexto.get(1.0, END))
            self.new_as_file.close()

    def refazer(self, event=None):
        try:
            self.areaTexto.edit_redo()

        except TclError:
            ...

    def desfazer(self, event=None):
        try:
            self.areaTexto.edit_undo()

        except TclError:
            ...

    def cortar(self, event=None):
        self.areaTexto.event_generate('<<Cut>>')

    def copiar(self, event=None):
        self.areaTexto.event_generate('<<Copy>>')

    def colar(self, event=None):
        self.areaTexto.event_generate('<<Paste>>')

    def showAbout(self):
        showinfo('Bloco de Notas', 'Rodrigo Novaes do Nascimento')

    def sair(self):
        self.app.quit()

    def saircadastro(self):
        if messagebox.askyesno('Sair', 'Deseja realmente sair?'):
            self.app.destroy()


    def iniciar(self):
        self.app.mainloop()



app = Notepad()
app.iniciar()
