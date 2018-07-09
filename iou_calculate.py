#'D:/temporario/alov300_iou/01-Light/01-Light_video00001.iou'
import os


def calculatePrecision(raiz,categoria,video,threshold):
	caminho = os.path.join(raiz,categoria,video)
	caminhoCompleto = caminho + '.iou'
	threshold = 0.5
	file = open(caminhoCompleto,'r')
	linhas = file.readlines()
	file.close()
	ious = [float(elemento.replace('\n','').split()[1]) for elemento in linhas]
	correct = wrong = 0
	for i in ious:
		if i>= threshold:
			correct += 1
		else:
			wrong += 1
	precision = correct/(correct+wrong)
	print('precision: ', precision)
	arquivoASalvar = caminho + '.precision'
	file = open(arquivoASalvar,'w')
	file.writelines(str(precision))
	file.close()

calculatePrecision('D:/temporario/alov300_iou','01-Light','01-Light_video00001',0.5)