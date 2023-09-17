# random
from random import randint

# layout tela
from PySimpleGUI import PySimpleGUI as Sg

# importação de código assíncrono
import asyncio

# Caracteres especiais exigidos
caracteres_especiais = ['*', '@', '#', '%', '$', '&', '.', ',']

# matrizes
global emails_registrados
global senhas_registradas

# Tela der aviso
def tela_aviso(t_tela, texto_aviso):
    global janela_aviso
    Sg.theme('DarkBlack')

    layout_cod_verificacao = [
    [Sg.Text("Digite abaixo o código de verificação")],
    [Sg.Input(key='key_cod_verificação', size=(20, 1))],
    [Sg.Button("Verificar")]
    ]
    layout_aviso = [
    [Sg.Text(texto_aviso)],
    [Sg.Button("Ok")]
    ]

    if t_tela == "cod_verificacao":
        janela_aviso = Sg.Window("Código de Verificação", layout_cod_verificacao)
    elif t_tela == "aviso":
        janela_aviso = Sg.Window("Aviso", layout_aviso)

    esc = 0
    while esc == 0:
        eventos_, valores_ = janela_aviso.read()
        if eventos_ == Sg.WINDOW_CLOSED:
            Sg.WINDOW_CLOSED
            janela_aviso.close()
            esc = 1
            return 'fechado'
        elif eventos_ == 'Verificar':
            Sg.WINDOW_CLOSED
            janela_aviso.close()
            esc = 1
            return valores_['key_cod_verificação']
        elif eventos_ == "Ok":
            Sg.WINDOW_CLOSED
            janela_aviso.close()
            esc = 1
            return 'fechado'
        else:
            Sg.WINDOW_CLOSED
            janela_aviso.close()
            esc = 1
            return 'fechado'

# Telas ----------
def tela(tipo_tela):
    global janela
    Sg.theme('DarkBlack')
    layout_login = [
        [Sg.Text('E-mail')],
        [Sg.Input(key='key_login_email', size=(50, 1))],
        [Sg.Text('Senha')],
        [Sg.Input(key='key_login_senha', size=(50, 1))],
        [Sg.Text("Não tem cadastro? Clique em"), Sg.Button("registrar")],
        [Sg.Button("Login")]
    ]
    layout_registro = [
        [Sg.Text('E-mail')],
        [Sg.Input(key='key_registro_email', size=(50, 1))],
        [Sg.Text('Senha')],
        [Sg.Input(key='key_registro_senha', size=(50, 1))],
        [Sg.Text('Repetir senha')],
        [Sg.Input(key='key_registro_repetirsenha', size=(50, 1))],
        [Sg.Text("Já tem cadastro? Clique em"), Sg.Button("login")],
        [Sg.Button("Cadastrar")]
    ]
    if tipo_tela == 'login':
        janela = Sg.Window("Login", layout_login)
    elif tipo_tela == 'registro':
        janela = Sg.Window("Registro", layout_registro)

    while True:
        eventos, valores = janela.read()
        if eventos == Sg.WINDOW_CLOSED:
            Sg.WINDOW_CLOSED
            janela.close()
            return 0
        elif eventos == "registrar":
            Sg.WINDOW_CLOSED
            janela.close()
            return 1
        elif eventos == "login":
            Sg.WINDOW_CLOSED
            janela.close()
            return 2
        elif eventos == "Login":
            cod = iniciar_login(valores['key_login_email'], valores['key_login_senha'])
            if cod == 5:
                return 5
            elif cod == 6:
                return 6
        elif eventos == "Cadastrar":
            iniciar_registro(valores['key_registro_email'],valores['key_registro_senha'],valores['key_registro_repetirsenha'])

# simulação de banco de dados em txt

# ler txt
async def ler_info(arquivo):
    try:
        r = open('data\{}.txt'.format(arquivo))
        return r.read()
    
    except FileNotFoundError:
        print("arquivo não existe, tente cria-lo")
        tela_aviso("Arquivo não encontrado, tente cria-lo!")

# criar ou remover arquivo
async def criacao_arquivo_txt(arquivo):
    try:
        # Arquvio já existe
        open("data\{}.txt".format(arquivo))
    except FileNotFoundError:
        # Criar arquivo
        open("data\{}.txt".format(arquivo), 'a')


async def atualizacao(info, arquivo):
    emails_salvos = open('data\{}.txt'.format(arquivo), 'a')
    emails_salvos.write('{}'.format(info))
    emails_salvos.close()

# adicionar no array
async def adicionar_info(arr, info):
    return arr.append(info)

async def formatando_lista(arquivo):
    valores = asyncio.create_task(ler_info(arquivo))
    valor = await valores
    vetor = valor.split('\n')
    arr = []
    for string in vetor:
        if string != "":
            arr.append(string)
    
    return arr


async def criar_txt(tipo, email, senha):
    global emails_registrados
    global senhas_registradas
    if tipo == 0:
        criar_arquivo_email = asyncio.create_task(criacao_arquivo_txt('email'))
        await criar_arquivo_email
        criar_arquivo_senhas = asyncio.create_task(criacao_arquivo_txt('senha'))
        await criar_arquivo_senhas
    elif tipo == 1:
        valor_email = '{}\n'.format(email)
        valor_senha = '{}\n'.format(senha)
        atualizar_email = asyncio.create_task(atualizacao(valor_email, 'email'))
        atualizar_senha = asyncio.create_task(atualizacao(valor_senha, 'senha'))
        await atualizar_email
        await atualizar_senha
        tela_aviso("aviso", "Usuário cadastrado!")
    elif tipo == 2:
        emails = asyncio.create_task(formatando_lista('email'))
        senhas = asyncio.create_task(formatando_lista('senha'))
        emails_registrados = await emails
        senhas_registradas = await senhas

# Iniciar banco de dados
asyncio.run(criar_txt(2, '', ''))


# função de inicialização de Registro
def iniciar_registro(email, senha, repetir_senha):

    if email == '' or senha == '' or repetir_senha == '':
        tela_aviso("aviso", "Verifique os campos em branco e tente novamente")
    elif verificar_se_usuario(email):
        tela_aviso("aviso", "Email já cadastrado, tente outro email")
    else:
        result = verificar_se_senha_igual(senha, repetir_senha)
        if result != True:
            tela_aviso("aviso", result)
        else:
            result = int(gerar_cod())
            tela_aviso("aviso", 'Seu código de verificação é {}'.format(result))
            print('Seu código de verificação é {}'.format(result))
            end_cod = False
            while end_cod == False:
                cod_verificacao = tela_aviso("cod_verificacao", '')
                if cod_verificacao == 'fechado':
                    tela_aviso("aviso", 'Foi encerrado a verificação, por favor tente novamente.')
                    return 5
                else:
                    if int(cod_verificacao) == int(result):
                        tela_aviso("aviso", 'Código validado')
                        asyncio.run(criar_txt(1, email, senha))
                        end_cod = True
                    else:
                        tela_aviso("aviso", 'Código invalido, por favor digite novamente: ')


# função inicialização login
def iniciar_login(email, senha):
    if email == '' or senha == '':
        tela_aviso("aviso", "Verifique os campos em branco e tente novamente")
    elif verificar_se_usuario(email):
        cont = 0
        global posicao_email
        for e in emails_registrados:
            if str(e) == str(email):
                posicao_email = cont
            cont += 1
                
        if senha == str(senhas_registradas[posicao_email]):
            tela_aviso("aviso", "Login criado com sucesso! Carregar aplicação...")
            return 6
        else:
            tela_aviso("aviso", "Senha incorreta, tente novamente")

    else:
        tela_aviso("aviso", "Email não cadastrado, tente fazer o registro")


# Verificar se usuario já cadastrado no banco
def verificar_se_usuario(email_):
    resultado = False
    for email_reg in emails_registrados:
        if email_reg == email_:
            resultado = True

    return resultado


# Verificador de senhas
def verificar_se_senha_igual(senha_, rep_senha):
    cont = 0
    qtd_caract = 0

    for s in senha_:
        s
        qtd_caract += 1

    for caract in caracteres_especiais:
        cont += senha_.count(caract)

    if cont == 0:
        return 'Coloque caractares especias na senha'
    elif qtd_caract < 6:
        return 'A senha deve ter no mínimo 6 digitos'
    elif senha_ != rep_senha:
        return 'Senhas não se coincidem'
    else:
        return True


# Gerador de código de verificação
def gerar_cod():
    numero_cod = ''
    i = 0
    while i < 6:
        numero_cod = '{}{}'.format(numero_cod, randint(0, 9))
        i += 1

    return numero_cod


# chamando_tela
def chamar_tela(t):
    c = tela(t)
    return c


# controlador
def inicializacao():
    numeracao_retorno = 1
    opcao = 0
    while opcao == 0:
        if numeracao_retorno == 1:
            valor = chamar_tela('registro')
            numeracao_retorno = valor
        elif numeracao_retorno == 2:
            valor = chamar_tela('login')
            numeracao_retorno = valor
        elif numeracao_retorno == 5:
            opcao = 1
        elif numeracao_retorno == 6:
            class Banco:
                def __init__(self, email, senha):
                    self.email = email
                    self.senha = senha

            banco_email = []
            banco_senha = []

            matriz = [emails_registrados, senhas_registradas]

            for email in matriz[0]:
                banco_email.append(email)

            for senha in matriz[1]:
                banco_senha.append(senha)

            geral = Banco(banco_email, banco_senha)

            index = 0
            for valor in geral.email:
                print("Email: {}. Senha: {}".format(valor, geral.senha[index]))
                index += 1

            opcao = 1
        else:
            opcao = 1


# Inicialização do projeto
inicializacao()
