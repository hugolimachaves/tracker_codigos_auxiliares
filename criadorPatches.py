import util as ut
a, b = ut.caminhos('/home/hugo/Documents/Mestrado/alov_dataset/alov300','videos')
#print(b)
#print('/elemento 0 0: ', b[0][0],'/elemento 1 0: ' ,b[1][0])
#print('/elemento 0 2: ',b[0][2],'/elemento 0 2: ' ,b[1][2])

for i,j in enumerate(b[1]):
    print(b[1][i],b[0][i])
    ut.gerarCaminhoAnotacao('/home/hugo/Documents/Mestrado/alov_dataset/alov300/anotacao','/home/hugo/Documents/Mestrado/alov_dataset/alov300/BB','/home/hugo/Documents/Mestrado/alov_dataset/alov300/videos',b[1][i],b[0][i]+'.ann')


