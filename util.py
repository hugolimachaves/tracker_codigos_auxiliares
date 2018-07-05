import os 
from PIL import Image
import math
import shutil
import copy
'''
Este arquivo so possui sentido se o banco de dados esta com caminhos padronizados
(.../)  |-videos
        |   |-categorias
        |   |   |-categoria 1
        |   |    |     |-video 1
        |   |    |     |   .
        |   |    |     |   .
        |   |    |     |   .
        |   |    |     | -video N
        |   |    |  .   
        |   |    |  .
        |   |    |  .
        |   |    |-categoria N
        |
        |-BB
        |    | ... (mesmo formato de cima)
        |    .
        |    .
        |    .
        |-anotacoes
        |   | ... (mesmo formato de cima)
        |   .
        |   .
        |   .
        |

Note que há videos que nao possuem anotaçoes de BB, então há imagens  na pasta video que não tem anotação e consequentemente não possui BB
(.../) == diretorio pai
'''

#retorna o numero de pixels da image
def nPixels(arquivo):
    im = Image.open(arquivo)
    width, height = im.size
    im.close()
    return width*height

#fornece o caminho e o arquivo e eles volta no formato certo pra vc! ;)
def concatCaminho(caminho,arquivo):
    return os.path.join(caminho,arquivo)

#mostre a imagem. Especificar o caminho com o nome da imagem
def readImage(caminho):
    return Image.open(caminho)

#entra com o caminho e nome do arquivo, e retorna com cada linha sendo elemento de uma lista
def getLinhas(caminho,arquivo):
    file = open(concatCaminho(caminho,arquivo),'r')
    linhas = file.readlines()
    file.close()
    return linhas

#pega os elementos de uma linha, se cada um for separado por espaço, entao retornará com uma lista compostas deste elementos, caso tenha outro delimitador que nao seja espaço, entao vc deve informar.
def getElementos(linha,delimitador = ' '):
    Elementos = linha.split(delimitador)
    return Elementos
#entra com os 4 pontos de bounding box e retorna ela com 2 pontos extremos (esquerda superior e direita inferior) e o frame ao qual os pontos foram extraidos
#4 pontos seguidos: p1(y,x),p2(y,x),p3(y,x),p4(y,x) - convenção PDI
#2 pontos seguidos: p1'(y,x),p2(y,x)
def getBB2P(linha):
    sty = 0
    stx = 1
    frameNumber = linha[0]
    linhaInt = [] 
    for i in range(0,len(linha)-1):
        i +=1
        linhaInt.append(int(round(float(linha[i]))))
    y = []
    x = []

    for i in range(sty,len(linhaInt),2):
        y.append(linhaInt[i])
    for i in range(stx,len(linhaInt),2):
        x.append(linhaInt[i])
    pontos = [] 
    pontos.append(str(min(y))) #p1
    pontos.append(str(min(x)))
    pontos.append(str(max(y))) #p2
    pontos.append(str(max(x)))
    return pontos,frameNumber

#fornece a imagem e os pontos que delimitam o BB e retorna somente o BB pra vc! ;)
def gerarPatch(img,pontos,offset=0):
    print('offset: ',offset)
    patch = img.crop((int(pontos[0])+offset,int(pontos[1])+offset,int(pontos[2])+offset,int(pontos[3])+offset))
    return patch

#forneca o patch (subimagem, o caminho para onde voce ira salvar a imagem e nome que vc quer dar para o arquivo) e veja amágica acontecer!
def savePatch(patch,caminho,nome,extensao):
    patch.save(concatCaminho(caminho,nome)+extensao)

# a diferenca dessa funcao para a gerarPatch é que essa faz todo o processo
def criarPatch(caminhoLista,arquivoLista,caminhoImagem, nomeImagem,CaminhoPatch,nomePatch ):
    linhas = getLinhas(caminhoLista,arquivoLista)
    pontos, frameNumber = getBB2P(getElementos(linhas[0]))
    print(pontos)
    savePatch(gerarPatch(readImage(concatCaminho(caminhoImagem,nomeImagem)),pontos),CaminhoPatch,nomePatch,'.jpg')

#remove a extensao de um arquivo
def removeExtention(arquivo,ext):
    return arquivo.split(ext)[0]

# lista com todos os frame de um video
def listarFrames(pasta,categoria,video):
    return os.listdir(concatCaminho(concatCaminho(pasta,categoria),video))

#gerar uma BB de acordo com o caminho especificado
def gerarCaminhoAnotacao(pastaAnotacao,pastaBB,pastaVideo,categoria,videoFull): # videofull: os frames com a extensao
    video = videoFull.split('.')[0]
    listaDeFrames = listarFrames(pastaVideo,categoria,video) # lista com os caminhos dos frames
    listaDeFrames.sort()

    #frames que o patch tem label 
    linhas = getLinhas(concatCaminho(pastaAnotacao,categoria),videoFull) # frames com os respectivos bounding box
    pasta = concatCaminho(concatCaminho(pastaBB,categoria),video)
    os.makedirs(pasta)
    
    for i in linhas:
        pontos,frameNumberstr = getBB2P(getElementos(i))
        frameNumber = int(frameNumberstr)
        fselecionado = listaDeFrames[frameNumber-1] #caminho para um frame que tem label, incluindo o seu nome
        pasta = concatCaminho(concatCaminho(pastaBB,categoria),video)
        savePatch(gerarPatch(readImage(concatCaminho(concatCaminho(concatCaminho(pastaVideo,categoria),video),fselecionado)),pontos,1),concatCaminho(concatCaminho(pastaBB,categoria),video), str(frameNumber),'.jpg')
        frameNumber += 1

#gera todos os sufixos (.../cat/vid) para todas a categorias e seus videos, reto
#input: Caminho comum as pasta de: video,BB e anotacao; pasta desejada (video, BB, anotacao)
def caminhos(caminhoRef,tipoDir):
    diretorio = concatCaminho(caminhoRef,tipoDir) # caminho em comum + video/BB/anotação
    sufixoCat = []
    sufixoTot = []
    sufixoTotSep = [[],[]]
    categorias = os.listdir(diretorio) # lista todas a categorias
    for i in categorias:
        sufixoCat.append(i)
    sufixoCat.sort()
    for j in sufixoCat: # categoria
        sufixoVid = [] # lista de videos em cada uma das categorias
        sufixoVid.append(os.listdir(concatCaminho(diretorio,j))) # lista com todos o sufixos do caminho categoria + videos
        for k in sufixoVid[0]: # video
            sufixoTot.append(concatCaminho(j,k)) # lista de sufixo: categoria + video
            sufixoTotSep[0].append(k) # lista com nome dos videos 
            sufixoTotSep[1].append(j) # lista com nome das categorias, essa linha e a de cima, e individual para cada video do data set
    return sufixoTot,sufixoTotSep

#passa uma string, com x1,y1,x2,y2 e retorna uma lista de float x1,y1,x2,y2
def getPontosFromString(string):
    pontos = string.split(',')
    for cont, ponto in enumerate(pontos):
        pontos[cont] = float(ponto)
    return pontos

#passa um string do arquivo de anotacao uma linha bb.txt com 4 pontos
#retorna: o indice do frame, 2 pontos no formato da Helena 
def getIndiceEPontosAnotacao(string):
    #convencao cartesiana
    if string.endswith('\n'):
        string = string[:-1]
    pontos = string.split(' ')
    for cont, ponto in enumerate(pontos):
        pontos[cont] = float(ponto)
    indice = pontos.pop(0)
    pontosX = list(pontos)
    pontosY = list(pontos)
    contX =  0
    contY =  0
    for indice in range(len(pontos)):
     
        if(indice%2):
            
            pontosX.pop(indice + contX)
            contX += -1
        else:
            pontosY.pop(indice + contY)
            contY += -1
    
    #convencao cartesiana
    novosPontos = [] 
    novosPontos.append(min(pontosX)) #p1
    novosPontos.append(min(pontosY))
    novosPontos.append(max(pontosX)) #p2
    novosPontos.append(max(pontosY))
    return indice, novosPontos

#determinar a interseccao da unicao para todo o video, retorna uma lista de IoU
def detInterseccaoDaUniaoVideo(caminhoAnotacao, arquivoAnotacao, caminhoSaida, arquivoSaida):
   
  
  
    anotacoes = getLinhas(caminhoAnotacao, arquivoAnotacao)
 
    saidas = getLinhas(caminhoSaida, arquivoSaida)
    anotacoesNum =[] #guarda os elementos de anotacoes em float
    saidaNum = [] #guarda os elementos de saida em float
    iou = []
    #saida do rastreados, no caso da Helena, o BB começa com indice 0
    for saida in saidas:
        saidaNum.append(getPontosFromString(saida))
 
   
    for anotacao in anotacoes:
        indice, pontos = getIndiceEPontosAnotacao(anotacao) #saida do GT, comeca com indice 1
        pontos = converterPontosParaReferencia(pontos,0) # estou convertendo para a referencia da helena

        iou.append(interseccaoDaUniao(saidaNum[indice-1], pontos))
    return iou


#calcula i IoU para os potnos dados, pontos formato (convencao cartesiado): x1,y1,x2,y2
def interseccaoDaUniao(boxA,boxB):
    
    if ( True in [ i or j for i,j in zip([math.isnan(i) for i in boxA],[math.isnan(i) for i in boxA])]):

        iou = 0
    else:
        # determine the (x, y)-coordinates of the intersection rectangle
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        # compute the area of intersection rectangleyA
        interArea = (xB - xA + 1) * (yB - yA + 1)
        # compute the area of both the prediction and ground-truth
        # rectangles
        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = interArea / float(boxAArea + boxBArea - interArea)
        if iou <= 0:
            iou = 0
        # return the intersection over union value
    return iou

#Essa função foi criada pelo fato de algumas anotações ou saida terem como origem ou o ponto 0,0 ou o ponto 1,1
#Assim, essa função da um offset nesses pontos de acordo com a referencia
def converterPontosParaReferencia(listaDePontos,referencia):
    for cont, ponto in enumerate(listaDePontos):
        if(referencia):
            listaDePontos[cont] = ponto + 1
        else:
            listaDePontos[cont] = ponto - 1
    return listaDePontos

#existe esse arquivo?
def isThereThisFile(caminho,arquivo):
    return arquivo in os.listdir(caminho)
    '''
    TESTE:
    lista1,lista2 = util.caminhos('/home/hugo/Documents/Mestrado/alov_dataset/alov300','videos')
    '''

def whereAreTheTrackersOutput():
    caminhoComum = '/home/hugo/Documents/Mestrado/alov_dataset/alov300'
    subcaminho = 'videos'
    subcaminhoAn = 'anotacao'
    nomeDoArquivo = 'bb.txt'
    prefixo = os.path.join(caminhoComum,subcaminho)
    listaSufixo, listaSufixoDepricated = caminhos(caminhoComum,subcaminho)
    listaDebb = [[],[],[],[]]
    for cont, sufixo in enumerate(listaSufixo):
        caminhoDoArquivo = os.path.join(prefixo,sufixo)
        if(isThereThisFile(caminhoDoArquivo,nomeDoArquivo)):
            listaDebb[0].append(os.path.join(os.path.join(os.path.join(caminhoComum,subcaminhoAn),listaSufixoDepricated[1][cont]))) #caminho do arquivos de anotacao
            listaDebb[1].append(listaSufixoDepricated[0][cont] + '.ann')
            listaDebb[2].append(caminhoDoArquivo)# caminho do arquivo bb.txt
            listaDebb[3].append(nomeDoArquivo)
    return listaDebb

def list2path(list):
    cadeia = ''
    for i in list:
        cadeia = os.path.join(cadeia,i)
    return cadeia

#primeiro parametro é de onde começa a iteracao o caminho comum, depois sao dos diferentes niveis a iterar...
#numero maximo de niveis a iterar, 0: só a raiz.
# raiz = lista contendo os diretorios e.g.: ['D:','pasta','subpasta']
# visita = funcao a ser chamada do percurso das pastas
# argsVisita = lista com os de argumentos da funcao visita
# nivel = passa o valor '-1' para a raiz ser nivel 0
# a funcao visita tem: argumentos proprios, definido por argsVisita; um segundo argumento que contem um lista que indica a pasta que esta sendo executada no momento ;um terceiro argumento que contem o nivel atual 
# Um modelo de funcao que pode ser utilizada e a funcao printar, especificada nesse arquivo

def percorrer(nivel,raiz,visita,argsVisita):
    level = nivel + 1
    
    print('variavel raiz pre: ',raiz)
    visita(level,raiz,argsVisita)
    print('variavel raiz pos: ',raiz)
    print('nivel: ', level)
    print('percorrendo...')
    diretorios = [i for i in os.listdir(list2path(raiz)) if ((os.path.isdir(os.path.join(list2path(raiz),i))) and (not i.startswith('.'))) ]
    diretorios.sort()
    for i in diretorios:
        raiz.append(i)
        
        percorrer(level,raiz,visita,argsVisita)
        raiz.pop()
    level -=1

   
#Copia a estrutura de diretorios, sem adicinar arquivo. Deve ser usado em conjunto com 'percorrer'
def copiaDiretoriosVazio(nivel,raiz,argsVisita):
    '''
    para usar a função, passe os seguintes argumentos para a funçao percorrer:
    percorrer( nivel inicial(inteirio), raiz da pasta de origem (string dentro de uma lista), o nome dessa funao, raiz da pasta de destino , (string dentro de uma lista de uma lista - e.g.: [['destino']]) )
    ut.percorrer(0,['D:\siameseFC_tracker\\alov300_saida'],ut.copiaDiretoriosVazio,[['D:\siameseFC_tracker\labTeste\destino']])
    '''
    '''
    exemplo:
    import util as ut
    ut.percorrer(0,['D:\siameseFC_tracker\\alov300_annotation'],ut.copiaDiretoriosVazio,[['D:\siameseFC_tracker\labTeste\destino']])
    '''
    '''
    Essa funçao esta mal programada? esta... mas nao me julgue pois ela funciona e eu estava com pressa
    '''  
    destino = argsVisita.copy()
    raizOrigemMaisSufixos = raiz.copy()
    raiz = raizOrigemMaisSufixos[0]  
    if raizOrigemMaisSufixos != []:
        if len (raizOrigemMaisSufixos) == 1:
            pass
        else:
            destino.append(raizOrigemMaisSufixos[1:])
    destinoPrefixo = ''
    destinoSufixo = ''
    for i in destino[0]:
        destinoPrefixo = os.path.join(destinoPrefixo,i)
    print('raizOrigemMaisSufixos[0]: ', raizOrigemMaisSufixos[0])
    if len(destino)>1:
        for i in destino[1]:
            destinoSufixo = os.path.join(destinoSufixo,i)
    
    destinoCompleto = os.path.join(destinoPrefixo,destinoSufixo)
    try:
        os.makedirs(destinoCompleto)
    except:
        print('Nao foi possivel criar: ',destinoCompleto)


#Copiar arquivo de um estrutura de arquivos para outro estrutura, antes deve-se chamar a funçao 'copiaDiretoriosVazio'
def copiaArquivosNaEstrutura(nivel,raiz,argsVisita): #nivel da iteração, raiz da pasta de origem, argsVisita e o destino dentro de uma lista ['destino']
    destino = argsVisita.copy()
    raizOrigemMaisSufixos = raiz.copy()
    raiz = raizOrigemMaisSufixos[0]  
    if raizOrigemMaisSufixos != []:
        if len (raizOrigemMaisSufixos) == 1:
            pass
        else:
            destino.append(raizOrigemMaisSufixos[1:])
    destinoPrefixo = ''
    destinoSufixo = ''
    for i in destino[0]:
        destinoPrefixo = os.path.join(destinoPrefixo,i)
    if len(destino)>1:
        for i in destino[1]:
            destinoSufixo = os.path.join(destinoSufixo,i)
    destinoCompleto = os.path.join(destinoPrefixo,destinoSufixo)
    try:
        shutil.copy(os.path.join(raiz,destinoSufixo,'saidaSiameseFC.txt'), destinoCompleto)
    except:
        print('Nao foi possivel copiar o tipo de arquivo para: ',destinoCompleto)
  
#Converte arquivos em uma estrutura para outra, convertendo-os para a saida padrao de processamento 
def converterArquivosdeSiameseFCParaAlov(nivel,raiz,argsVisita): # função conjunta com ut.percorrer
    #exemplo de chamda
    '''ut.percorrer(0,['D:/siameseFC_tracker/alov300_saida'],ut.converterArquivosdeSiameseFCParaAlov,[['D:/siameseFC_tracker/labTeste/destino']])'''
    destino = argsVisita.copy()
    raizOrigemMaisSufixos = raiz.copy()
    raiz = raizOrigemMaisSufixos[0]  
    if raizOrigemMaisSufixos != []:
        if len (raizOrigemMaisSufixos) == 1:
            pass
        else:
            destino.append(raizOrigemMaisSufixos[1:])
    destinoPrefixo = ''
    destinoSufixo = ''
    for i in destino[0]:
        destinoPrefixo = os.path.join(destinoPrefixo,i)
    if len(destino)>1:
        for i in destino[1]:
            destinoSufixo = os.path.join(destinoSufixo,i)
    destinoSufixo = destinoSufixo.replace('\\','/')
    destinoCompleto = os.path.join(destinoPrefixo,destinoSufixo)
    destinoCompleto = destinoCompleto.replace('\\','/')
    try:
        numero_frame = getNumeroPrimeiroFrame(os.path.join('D:/siameseFC_tracker/alov300_annotation',destinoSufixo + '.ann'))
        arquivo_entrada = os.path.join(raiz,destinoSufixo,'saidaSiameseFC.txt')
        arquivo_entrada = arquivo_entrada.replace('\\','/')
        arquivo_saida = destinoCompleto
     
        conversor_siameseFC_alov300(numero_frame,arquivo_entrada,arquivo_saida,'convertido')
    except:
        print('Nao foi possivel converter para: ',destinoCompleto)





def conversor_siameseFC_alov300(frame,input,path_output,namefile):
    '''
    funçao para converter a saida do siameseFC para analise padrao do alov300
    argumentos:

    um inteiro
    um caminho para ler um arquivo txt, txt_in
    um caminho para gravar um arquivo txt_out
    uma nome para gravar o arquivo txt_out, que ja sera .txt, entao nao passe a extensao 

    ex.:  def func(int, caminho_in, , nome)

    A funcao deve ler o arquivo txt_in em camino_in.
    Para cada cada linha de txt_in deve ser incrementado de int

    ie.:

    int premeiraLinha_txt_in
    int+1 segundaLinha_txt_in
    .
    .
    .
    int+n ultimaLinha_txt_in


    para cada linha de txt_in, há 4 elementos.
    criar uma linha equivalente no seguinte formato:

    int 1_txt_in 2txt_in 1_txt_in+3_txt_in 2txt_in+4_xt_in 

    totalizando 5 elementos por linha, onde:
    1_txt_in, significa 1º elemento de uma determinada linha no arquivo txt_in
    2_txt_in, significa 2º elemento de uma determinada linha no arquivo txt_in
    .
    .
    .
    '''
    input = input.replace('\\\\','/')
    input = input.replace('\\','/')
    path_output =  path_output.replace('\\\\','/')
    path_output =  path_output.replace('\\','/')
    output = os.path.join(path_output,namefile + ".txt")
    with open (input) as i, open (output, "wt") as o:
        for line in i:
            line = line.replace("\n", "")
            coord = line.split()		
            o.write("%d " %frame + "%f " %float(coord[0]) + "%f " %float(coord[1]) + "%f " %(float(coord[0]) + float(coord[2])) + "%f\n" %(float(coord[1]) + float(coord[3])))
            frame+=1


def getNumeroPrimeiroFrame(caminho):
    file = open(caminho,'r')
    linha = file.readline()
    file.close()
    valoresLinha = linha.split()
    frame =  int(valoresLinha[0])
    return frame



def printar(listaArgs,raiz,nivel):
    print('teste novo')
    if nivel == 2:
        print(raiz)
        fullCaminho = ''
        for i  in raiz:
            fullCaminho = os.path.join(fullCaminho,i)

        print(os.listdir(os.path.join(fullCaminho)))
    print(nivel)


#teste 2
def soma(a,b):
    return a + b


    

#argumentos rapidos para o prompt

#teste 1
'''
import os
import util as ut
raiz = []
argumento = []
arquivos = []
arquivos.append('bb.txt')
arquivos.append('lista.list')
raiz.append('/home/hugo/Documents/Mestrado/alov_dataset/alov300/videos')
argumento.append('/home/hugo/Documents/Mestrado/saidas')
argumento.append(raiz)
argumento.append('alteracao')
argumento.append(arquivos)
ut.percorrer(raiz,ut.copiarPasta,argumento,-1)

'''
#teste 2 - iou medio
'''
lista = whereAreTheTrackersOutput()
accLenLista = 0
accTotal = 0

for video in range(len(lista[0])):
    vid = video
    #print(lista[0][video], lista[1][video], lista[2][video], lista[3][video])
    listaTodos = detInterseccaoDaUniaoVideo(lista[0][video], lista[1][video], lista[2][video], lista[3][video])
    print(listaTodos)
    accLenLista += len(listaTodos)
    for i in listaTodos:
        accTotal +=i

iouMedio = accTotal/accLenLista
print(iouMedio)
print('teste')
'''











'''
TODO: DEBUGAR PQ ioiMedio é nan
     hipotese:
     listaTodos esta retornando nan, verificar o que leva a isso
TODO: o bb inicial gerado é diferente do bb inicial da marcação, consertar

'''


'''
TESTE:
modelo = [200,200,300,300]
offset = 50
print('entrou')
for i in range (-1,2):
    print('i: ',i)
    for j in range(-1,2):
        print('j: ',j)	
        temp = list(modelo)
        temp[0] = temp[0] + i*offset
        temp[1] = temp[1] + j*offset
        temp[2] = temp[2] + i*offset
        temp[3] = temp[3] + j*offset
        print('modelo: ',modelo )
        print('temp: ',temp )
        
        if interseccaoDaUniao(modelo,temp) > 0:
            print(interseccaoDaUniao(modelo,temp))
            print('passou')
        else:
            print('reprovado')
        
        if( not (interseccaoDaUniao(modelo,temp) == interseccaoDaUniao(temp,modelo)) ):
            print('Erro de simetria')
'''