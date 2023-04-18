#!/usr/bin/env python3
from pymongo import MongoClient
import tkinter as tk


client = MongoClient('mongodb://localhost:27017/')
db = client['local']
colecao = db['disciplinas']

root = tk.Tk()

class PrototipoIA():
    """
        Prototipo de sistema inteligente para escolha de disciplina.
    """

    def __init__(self) -> None:
        self.listArea = []
        self.listRecomendacao = []
        self.disciplinas = []


    def regras(self):
        
        # 1- Se um aluno já tiver concluído um curso que é pré-requisito para uma disciplina, então ele pode se inscrever para a disciplina.
        #   pass
        
        # 2- Se o aluno tiver interesse em uma determinada área de conhecimento, é recomendável selecionar disciplinas nessa área para ele.
        for area in self.listArea():
            colecao.update_many({'area_conhecimento':area}, {'$inc': {'relevancia':1}})
            colecao.update_many({'$nor': [{"area_conhecimento":area}]}, {'$inc': {'relevancia':-0.5,'dificuldade':-0.5}})
        
        # 3- Se a relevância de uma disciplina for alta para o curso que o aluno está fazendo, é recomendável que o aluno selecione essa disciplina.
        resultado = colecao.find({'relevancia': {'$gt':4}})
        for doc in resultado:
            self.recomendacao.append(doc['nome'])
        
        # 4- Se houver várias opções de disciplinas disponíveis, o sistema pode sugerir as disciplinas com menor carga horária ou menor dificuldade para o aluno.
        for i in self.recomendacao:
            colecao.find({'nome':i})

        # 5- Se um aluno tiver concluído todas as disciplinas obrigatórias em uma área de conhecimento, então ele pode selecionar disciplinas eletivas nessa área.
        #   pass
        
        # 6- Se a disciplina for obrigatória para o curso do aluno, então ele deve selecioná-la.
        resultado = db.disciplinas.find({'nucleo': 'sim'})
        for doc in resultado:
            self.recomendacao.append(doc['nome'])

        # 7- Se uma disciplina é pré-requisito de outra disciplina obrigatória para o curso do aluno, então é recomendável que o aluno selecione a disciplina
        #   pré-requisito.
        #   pass

        # 8- Se a área de conhecimento de uma disciplina for muito diferente da área de conhecimento principal do curso do aluno, é melhor evitar essa disciplina
        #   ou avaliar cuidadosamente sua relevância.
        resultado = db.disciplinas.find({'area_conhecimento': 'desenvolvimento'})        
        for doc in resultado:
            for area in self.listArea():
                colecao.update_many({'area_conhecimento':area}, {'$inc': {'relevancia':1}})


    def escolhas(self, checkbox_vars):
        """ Recebe as escolhas do usuario de disciplinas ja cursadas e atualiza o banco. """
        #for nome in checkbox_vars:
        #    db.disciplinas.update_many({'area_conhecimento': nome},{'$set': {'cursado': True}})
        for i in range(len(self.disciplinas)):
            #print(f'i = {i}')
            
            if(checkbox_vars[i].get() == 1):
                #print(f'checkbox_vars[i].get() => {checkbox_vars[i].get()}')
                print(f'nome => {self.disciplinas[i]}')
                update = db.disciplinas.update_one({'nome': self.disciplinas[i]},{'$set': {'cursado': True}})
                print(f"Documentos atualizados => {update.modified_count}")



    def telas(self):
        """ Inicializa a tela para a escolha da disciplina. """
        def exit_app():
            root.destroy()
        resultado = db.disciplinas.find({})
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
        self.escolhas(checkbox_vars)

    

if __name__ == '__main__':
    ia = PrototipoIA()
    ia.telas()

The easiest way:

$ mkdir build
$ cd build
$ cmake ../
$ make
$ make install