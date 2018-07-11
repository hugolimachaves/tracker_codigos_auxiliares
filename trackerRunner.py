import os 
import util as ut
from PIL import Image

print("comeco codigo")
caminhoCodigo = '/home/hugo/Documents/Mestrado/codigoRastreador/bin/Debug/tracker' # caminho do tracker
caminhoBD = '/home/hugo/Documents/Mestrado/alov_dataset/alov300' #raiz do banco de dados, do tipo de dados antes das classes
subpasta = 'videos' # nome da pasta que contem os frames
pastaAlteracao = 'alteracao' #obsoleto

def videoGrande(caminhoBD,subpasta,categoria,video,QualOTamanhoDeUmVideoGrandeEmMB):
    items = os.listdir(os.path.join(os.path.join(os.path.join(caminhoBD,subpasta),categoria),video))
    frames = []
    for frame in items:
        if frame.endswith('.jpg'):
            frames.append(frame)
    
    nPixelsTotal = 0

    for frame in frames:
        nPixels = ut.nPixels(os.path.join(os.path.join(os.path.join(os.path.join(caminhoBD,subpasta),categoria),video),frame))
        nPixelsTotal += nPixels 

    tamanhoRGB = nPixelsTotal*3
    tamanhoEmMB = tamanhoRGB / ( pow(1024,2))
    print('O video tem ', str(tamanhoEmMB), 'MB quando carregado na memoria')
    if QualOTamanhoDeUmVideoGrandeEmMB < tamanhoEmMB:
        return True
    else:
        return False



def _main():
    print("comeco")
    categorias = os.listdir(os.path.join(caminhoBD,subpasta))
    for categoria in categorias:
        videos = os.listdir(os.path.join(os.path.join(caminhoBD,subpasta),categoria))
        for video in videos:

            print('Executando tracker para o video: ', video,', da categoria: ',categoria)
            ''' if videoGrande(caminhoBD,subpasta,categoria,video,4000): #4000MB de memoria o video ja e grande
                print('Por enquanto vamos pular esse video')
                continue
            
            else:
            '''
            caminhoVideo = os.path.join(os.path.join(os.path.join(caminhoBD,subpasta),categoria),video)
            caminhoParam = os.path.join(caminhoVideo,'parameters.yml')
            caminhoGravacaoObjMdel = os.path.join(caminhoVideo,'objectModelCoordenates.txt')
            if not (os.path.exists(os.path.join(caminhoBD,subpasta,categoria,video,pastaAlteracao))):
                os.makedirs(os.path.join(caminhoBD,subpasta,categoria,video,pastaAlteracao))
                caminhoAlteracao = os.path.join(caminhoBD,subpasta,categoria,video,pastaAlteracao)
            comando = caminhoCodigo + ' ' + caminhoParam + ' ' + caminhoGravacaoObjMdel
            os.system(comando)

if __name__ == '__main__':
    _main()