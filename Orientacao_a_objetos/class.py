class Pessoa():
    def __init__(self, nome, sexo, cpf, ativo):
        self.nome = nome
        self.sexo = sexo
        self.cpf = cpf
        self.ativo = ativo
    
    def desativar(self):
        self.ativo = False
        print("A pessoa foi desativada com sucesso")
    

if __name__ == '__main__':
    pessoa1 = Pessoa("João", "M", "123.456.789-11", True)
    pessoa1.desativar()
    
