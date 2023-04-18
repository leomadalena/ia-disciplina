#!/usr/bin/env python3
from pymongo import MongoClient
import pymongo
import tkinter as tk


client = MongoClient('mongodb://localhost:27017/')
db = client['local']
colecao = db['disciplinas']



class PrototipoIA():
    """
        Prototipo de sistema inteligente para escolha de disciplina.
    """

    def __init__(self) -> None:
        self.listAreaDisponivel = []
        self.listAreaSelecionada = []
        self.listRecomendacao = []
        self.disciplinas = []
        self.listCreditos = []


    def regras(self):
        
        # 1- Se um aluno já tiver concluído um curso que é pré-requisito para uma disciplina, então ele pode se inscrever para a disciplina.
        #   pass
        
        # 2- Se o aluno tiver interesse em uma determinada área de conhecimento, é recomendável selecionar disciplinas nessa área para ele.
        for area in self.listAreaSelecionada:
            colecao.update_many({'area_conhecimento':area}, {'$inc': {'relevancia':1}})
            colecao.update_many({'$nor': [{"area_conhecimento":area}]}, {'$inc': {'relevancia':-0.5,'dificuldade':-0.5}})
        
        # 3- Se a relevância de uma disciplina for alta para o curso que o aluno está fazendo, é recomendável que o aluno selecione essa disciplina.
        resultado = colecao.find({'relevancia': {'$gt':4}})
        for doc in resultado:
            colecao.update_many({'nome':doc['nome']}, {'$inc': {'relevancia':3}})
        
        # 4- Se houver várias opções de disciplinas disponíveis, o sistema pode sugerir as disciplinas com menor carga horária ou menor dificuldade para o aluno.
        # pass

        # 5- Se um aluno tiver concluído todas as disciplinas obrigatórias em uma área de conhecimento, então ele pode selecionar disciplinas eletivas nessa área.
        #   pass
        
        # 6- Se a disciplina for obrigatória para o curso do aluno, então ele deve selecioná-la.
        resultado = db.disciplinas.find({'nucleo': 'sim'})
        for doc in resultado:
            colecao.update_many({'nome':doc['nome']}, {'$inc': {'relevancia':3}})

        # 7- Se uma disciplina é pré-requisito de outra disciplina obrigatória para o curso do aluno, então é recomendável que o aluno selecione a disciplina
        #   pré-requisito.
        #   pass

        # 8- Se a área de conhecimento de uma disciplina for muito diferente da área de conhecimento principal do curso do aluno, é melhor evitar essa disciplina
        #   ou avaliar cuidadosamente sua relevância.
        resultado = colecao.find({})        
        for doc in resultado:
            for area in self.listAreaSelecionada:
                colecao.update_many({'area_conhecimento':area}, {'$inc': {'relevancia':1}})


    def escolhasDisciplinas(self, checkbox_vars):
        """ Recebe as escolhas do usuario de disciplinas ja cursadas e atualiza o banco. """
        for i in range(len(self.disciplinas)):
            if(checkbox_vars[i].get() == 1):
                print(f'nome => {self.disciplinas[i]}')
                update = db.disciplinas.update_one({'nome': self.disciplinas[i]},{'$set': {'cursado': True}})
                print(f"Documentos atualizados => {update.modified_count}")

    def escolhasAreaConhecimento(self, checkbox_vars):
        """ Recebe as escolhas do usuario """
        for i in range(len(self.listAreaDisponivel)):
            if(checkbox_vars[i].get() == 1):
                self.listAreaSelecionada.append(self.listAreaDisponivel[i])

        print(f'Areas selecionadas: {self.listAreaSelecionada}')

    def telaEscolhaDisciplina(self):
        root = tk.Tk()
        """ Inicializa a tela para a escolha da disciplina. """
        def exit_app():
            root.destroy()
        resultado = colecao.find({})
        for doc in resultado:
            self.disciplinas.append(doc['nome'])
        # Cria uma lista de variáveis IntVar para armazenar o estado de cada checkbox
        checkbox_vars = [tk.IntVar() for option in self.disciplinas]
        # Cria um checkbox para cada opção usando um loop for
        for i, option in enumerate(self.disciplinas):
            checkbox = tk.Checkbutton(root, text=option, variable=checkbox_vars[i])
            
            checkbox.pack()
        
        button = tk.Button(root, text="Concluir", command=exit_app)    
        button.pack()
        root.mainloop()
        self.escolhasDisciplinas(checkbox_vars)


    def telaResultadoEscolha(self):
        root = tk.Tk()
        """ Inicializa a tela que mostra as melhores disciplinas. """

        def exit_app():
            root.destroy()
        limite_creditos = 30

        # Faz a consulta na coleção 
        docs = colecao.find({'$and': [{'creditos': {'$lte': limite_creditos}},{'cursado': False}]}).sort('relevancia', pymongo.DESCENDING).limit(10)

        soma = 0
        # Imprime os nomes das disciplinas encontradas
        for doc in docs:
            
            if((soma < limite_creditos) and (soma + doc['creditos'] < limite_creditos) ):
                soma += doc['creditos']
                self.listRecomendacao.append(doc['nome'])
                self.listCreditos.append(doc['creditos'])
            print(doc['nome'])
        # Cria uma lista de variáveis IntVar para armazenar o estado de cada checkbox
        print(self.listRecomendacao)
        for i in range(len(self.listRecomendacao)):
            texto = tk.Label(text=f'{self.listRecomendacao[i]} creditos => {self.listCreditos[i]}', fg="blue", font=("Arial", 16))
            texto.pack()
        texto = tk.Label(text=f'Total de credito = {soma}', fg="blue", font=("Arial", 16))
        texto.pack()
        root.mainloop()
        colecao.update_many({},{'$set': {'cursado': False}})
        colecao.update_many({},{'$set': {'relevancia':4, 'dificuldade':4}})


    def telaEscolhaAreaConhecimento(self):
        root = tk.Tk()
        """ Inicializa a tela para a escolha de areas de conhecimento. """
        def exit_app():
            root.destroy()

        docs = colecao.find({})
        for doc in docs:
            for i in doc['area_conhecimento']:
                if not i in self.listAreaDisponivel:
                    self.listAreaDisponivel.append(i)
        print(f'Areas do conhecimento disponiveis {self.listAreaDisponivel}')
        # Cria uma lista de variáveis IntVar para armazenar o estado de cada checkbox
        checkbox_vars = [tk.IntVar() for option in self.listAreaDisponivel]
        # Cria um checkbox para cada opção usando um loop for
        for i in range(len(self.listAreaDisponivel)):
            checkbox = tk.Checkbutton(root, text=f'{self.listAreaDisponivel[i]}', variable=checkbox_vars[i])
            
            checkbox.pack()
        
        button = tk.Button(root, text="Concluir", command=exit_app)    
        button.pack()
        root.mainloop()
        self.escolhasAreaConhecimento(checkbox_vars)

if __name__ == '__main__':
    ia = PrototipoIA()
    ia.telaEscolhaDisciplina()
    ia.telaEscolhaAreaConhecimento()
    ia.regras()
    ia.telaResultadoEscolha()

# nome => ['Processamento de Imagens', 'Programação Orientada a Objetos', 'Estrutura de Dados', 'Geometria Analítica e Álgebra Linear', 'Fundamentos para Computação', 'Probabilidade e Estatística']
#         ['Processamento de Imagens', 'Programação Orientada a Objetos', 'Estrutura de Dados', 'Geometria Analítica e Álgebra Linear', 'Fundamentos para Computação', 'Probabilidade e Estatística']
#         ['Arquitetura e Organização de Computadores', 'Desafios Contemporâneos', 'Estágio Supervisionado', 'Optativa I', 'Atividades Complementares', 'Desenvolvimento Humano e Social', 'Gestão de Projetos']
