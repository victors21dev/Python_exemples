# random
from random import randint

# layout tela
from PySimpleGUI import PySimpleGUI as Sg

# Simulando um banco de dados
emails_registrados = ['santos.victors2000@gmail.com', 'teste@gmail.com']
senhas_registradas = ['123456*', '1234']

# Caracteres especiais exigidos
caracteres_especiais = ['*', '@', '#', '%', '$', '&', '.', ',']


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
        elif eventos == "Cadastrar":
            iniciar_registro(valores['key_registro_email'],valores['key_registro_senha'],valores['key_registro_repetirsenha'])



def tela_aviso(t_tela):
    global janela_aviso
    Sg.theme('DarkBlack')

    layout_cod_verificacao = [
    [Sg.Text("Digite abaixo o código de verificação")],
    [Sg.Input(key='key_cod_verificação', size=(20, 1))],
    [Sg.Button("Verificar")]
    ]

    if t_tela == "cod_verificacao":
        janela_aviso = Sg.Window("Código de Verificação", layout_cod_verificacao)
    esc = 0
    while esc == 0:
        eventos_, valores_ = janela_aviso.read()
        if eventos_ == Sg.WINDOW_CLOSED:
            Sg.WINDOW_CLOSED
            janela.close()
            esc = 1
            return 'fechado'
        elif eventos_ == 'Verificar':
            Sg.WINDOW_CLOSED
            janela.close()
            esc = 1
            return valores_['key_cod_verificação']
        else:
            Sg.WINDOW_CLOSED
            janela.close()
            esc = 1
            return 'fechado'



# função de inicialização de Registro
def iniciar_registro(email, senha, repetir_senha):

    if email == '' or senha == '' or repetir_senha == '':
        print("Verifique os campos em branco e tente novamente")
    elif verificar_se_usuario(email):
        print("Email já cadastrado, tente outro email")
    else:
        result = verificar_se_senha_igual(senha, repetir_senha)
        if result != True:
            print(result)
        else:
            result = int(gerar_cod())
            print('Seu código de verificação é {}'.format(result))
            end_cod = False
            while end_cod == False:
                cod_verificacao = tela_aviso("cod_verificacao")
                if cod_verificacao == 'fechado':
                    print("Foi encerrado a verificação, por favor tente novamente.")
                    return 5
                else:
                    if int(cod_verificacao) == int(result):
                        print('Código validado')
                        salvar_info(email, senha)
                        end_cod = True
                    else:
                        print('Código invalido, por favor digite novamente: ')


# função inicialização login
def iniciar_login(email, senha):
    if email == '' or senha == '':
        print("Verifique os campos em branco e tente novamente")
    elif verificar_se_usuario(email):
        cont = 0
        global posicao_email
        for e in emails_registrados:
            if str(e) == str(email):
                posicao_email = cont
        if senha == str(senhas_registradas[posicao_email]):
            print("Login criado com sucesso! Carregar aplicação...")
            return 5
        else:
            print("Senhaincorreta, tente novamente")

    else:
        print("Email não cadastrado, tente fazer o registro")


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

# Salvamento no array
def salvar_info(e, s):
    emails_registrados.append(e)
    senhas_registradas.append(s)
    print('E-mail {} registrado com sucesso!'.format(e))

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
        else:
            opcao = 1

# Inicialização do projeto
inicializacao()
