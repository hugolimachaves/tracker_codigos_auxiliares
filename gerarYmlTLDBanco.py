'''
comum: camino em comum do sistema
subcaminhoVideos: nome da pasta, abaixo da pasta comum, que contem todos os videos
subcaminhoAnotacoes: nome da pasta, abaixo da pasta comum, que contem todos as anotações
BBinicial: nome da pasta, dentro da pasta de anotaçoes, que contem as anotaçoes da pasta com os BB iniciais
'''

encode = "utf-8"

import os
import argparse as arg

def _getArgs():
    parser = arg.ArgumentParser(description = "Gera arquivo yml para o tracker da Helena")
    parser.add_argument("comum", help = "Caminho comum a todas a subpastas do banco de dados")
    parser.add_argument("subcaminhoVideos", help = "Subcaminho onde contem os videos")
    parser.add_argument("subcaminhoAnotacoes", help = "Subcaminho onde contem as anotacoes")
    parser.add_argument("BBinicial", help = "Nome da pasta com o BB inicial")
    return parser.parse_args()

def _main(comum, subcaminhoVideos, subcaminhoAnotacoes, BBinicial): 
    caminho = os.path.join(comum,subcaminhoVideos)
    categorias = os.listdir(caminho)
    for categoria in categorias:
        videos = os.listdir(os.path.join(caminho,categoria))
        for video in videos:
            comando = 'python ' + 'geradorYmlTLD.py ' + comum + ' ' + subcaminhoVideos + ' ' + subcaminhoAnotacoes + ' ' + categoria + ' ' + video + ' ' + BBinicial
            os.system(comando)

if __name__ == '__main__':
    args = _getArgs()
    _main(args.comum, args.subcaminhoVideos, args.subcaminhoAnotacoes, args.BBinicial)