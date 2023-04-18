#!/usr/bin/env python3
from pymongo import MongoClient
import pymongo
import tkinter as tk
import pprint


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
        """ Regras para a selecao de disciplinas. """
        # 1- Se o aluno tiver interesse em uma determinada área de conhecimento, é recomendável selecionar disciplinas nessa área para ele.
        for area in self.listAreaSelecionada:
            colecao.update_many({'area_conhecimento':area}, {'$inc': {'relevancia':1}})
            colecao.update_many({'$nor': [{"area_conhecimento":area}]}, {'$inc': {'relevancia':-0.5,'dificuldade':-0.5}})
        
        # 2- Se a relevância de uma disciplina for alta para o curso que o aluno está fazendo, é recomendável que o aluno selecione essa disciplina.
        resultado = colecao.find({'relevancia': {'$gt':4}})
        for doc in resultado:
            colecao.update_many({'nome':doc['nome']}, {'$inc': {'relevancia':3}})
        
        # 3- Se a disciplina for obrigatória para o curso do aluno, então ele deve selecioná-la.
        resultado = db.disciplinas.find({'nucleo': 'sim'})
        for doc in resultado:
            colecao.update_many({'nome':doc['nome']}, {'$inc': {'relevancia':3}})

        # 4- Se a área de conhecimento de uma disciplina for muito diferente da área de conhecimento principal do curso do aluno, é melhor evitar essa disciplina
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
                db.disciplinas.update_one({'nome': self.disciplinas[i]},{'$set': {'cursado': True}})
                

    def escolhasAreaConhecimento(self, checkbox_vars):
        """ Recebe as escolhas do usuario """


        for i in range(len(self.listAreaDisponivel)):
            if(checkbox_vars[i].get() == 1):
                self.listAreaSelecionada.append(self.listAreaDisponivel[i])
        print(f'Areas selecionadas:')
        pprint.pprint(self.listAreaSelecionada)


    def telaEscolhaDisciplina(self):
        """ Inicializa a tela para a escolha da disciplina. """


        def exit_app():
            root.destroy()

        root = tk.Tk()
        
        texto = tk.Label(text=f'Selecione as disciplinas que voce ja cursou:', fg="blue", font=("Arial", 16))
        texto.pack()
        
        resultado = colecao.find({})
        for doc in resultado:
            self.disciplinas.append(doc['nome'])
        
        checkbox_vars = [tk.IntVar() for option in self.disciplinas]
        for i, option in enumerate(self.disciplinas):
            checkbox = tk.Checkbutton(root, text=option, variable=checkbox_vars[i])
            checkbox.pack()
        
        button = tk.Button(root, text="Concluir", command=exit_app)    
        button.pack()
        
        root.mainloop()
        
        self.escolhasDisciplinas(checkbox_vars)


    def telaResultadoEscolha(self):
        """ Incializa a tela para exibir o resultado. """
        

        limite_creditos = 30
        soma = 0

        def exit_app():
            root.destroy()

        root = tk.Tk()

        texto = tk.Label(text=f'Voce pode escolher essas disciplinas:', fg="blue", font=("Arial", 16))
        texto.pack()
        
        docs = colecao.find({'$and': [{'creditos': {'$lte': limite_creditos}},{'cursado': False}]}).sort('relevancia', pymongo.DESCENDING).limit(10)
        for doc in docs:
            if((soma < limite_creditos) and (soma + doc['creditos'] < limite_creditos) ):
                soma += doc['creditos']
                self.listRecomendacao.append(doc['nome'])
                self.listCreditos.append(doc['creditos'])
        print('Lista de recomendacao: ')
        pprint.pprint(self.listRecomendacao)
        
        for i in range(len(self.listRecomendacao)):
            texto = tk.Label(text=f'{self.listRecomendacao[i]} creditos => {self.listCreditos[i]}', fg="black", font=("Arial", 16))
            texto.pack()
        
        texto = tk.Label(text=f'Total de credito = {soma}', fg="blue", font=("Arial", 16))
        texto.pack()
        
        button = tk.Button(root, text="Concluir", command=exit_app)    
        button.pack()
        
        root.mainloop()
        
        colecao.update_many({},{'$set': {'cursado': False}})
        colecao.update_many({},{'$set': {'relevancia':4, 'dificuldade':4}})


    def telaEscolhaAreaConhecimento(self):
        """ Inicializa a tela para a escolha de areas de conhecimento. """


        def exit_app():
            root.destroy()

        root = tk.Tk()

        texto = tk.Label(text=f'Escolhas as areas que voce gosta', fg="blue", font=("Arial", 16))
        texto.pack()

        docs = colecao.find({})
        for doc in docs:
            for i in doc['area_conhecimento']:
                if not i in self.listAreaDisponivel:
                    self.listAreaDisponivel.append(i)
        print("Areas do conhecimento disponiveis: ")
        pprint.pprint(self.listAreaDisponivel)
        checkbox_vars = [tk.IntVar() for option in self.listAreaDisponivel]
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
