import os 
import argparse as arg

encode = "utf-8"

#caminho: caminho ate o banco de dados
#subcaminho: nome da pasta, i.e., BB, anotacoes ou videos
#categoria: nome da pasta com a categoria
#video: nome da pasta com o video
#BBinicial: nome da pasta com o BB inicial

def _getArgs():
    parser = arg.ArgumentParser(description = "Gera arquivo yml para o tracker da Helena")
    parser.add_argument("caminho", help = "Caminho comum a todas a subpastas do banco de dados")
    parser.add_argument("subcaminhoVideos", help = "Subcaminho onde contem os videos")
    parser.add_argument("subcaminhoAnotacoes", help = "Subcaminho onde contem as anotacoes")
    parser.add_argument("categoria", help = "Nome da pasta da categoria")
    parser.add_argument("video", help = "Nome da pasta que contem o video")
    parser.add_argument("BBinicial", help = "Nome da pasta com o BB inicial")
    return parser.parse_args()

def escreverYml(caminho,subcaminhoVideos,subcaminhoAnotacoes,categoria,video,BBinicial):
    video_type = '2'
    filter = '6'
    window_size = '15'
    bb_path =  os.path.join(os.path.join(os.path.join(os.path.join(caminho,subcaminhoVideos),categoria),video),'bb.txt') # saida do tracker
    video_path = os.path.join(os.path.join(os.path.join(os.path.join(caminho,subcaminhoVideos),categoria),video),'lista.list')
    init_path = os.path.join(os.path.join(os.path.join(os.path.join(caminho,subcaminhoAnotacoes),categoria),BBinicial), video + '.ann.txt')
    gt_path = os.path.join(os.path.join(os.path.join(caminho,subcaminhoAnotacoes),categoria), video + '.ann')
    detect = '1'
    track = '1'
    detect_failure = '1'
    show = '0'
    repeat_video = '0'
    print_status = '1'
    valid = '0'
    conf =  '0'

    file = open(os.path.join (os.path.join( os.path.join(os.path.join(caminho,subcaminhoVideos),categoria),video) ,"parameters.yml"),"w")
    file.write("%YAML:1.0\n")
    file.write("video_type: " + video_type + "\n") 
    file.write("filter: " + filter + "\n")
    file.write("window_size: " + window_size + "\n")
    file.write("bb_path: " + bb_path + "\n")
    file.write("video_path: " + video_path + "\n")
    file.write("init_path: " + init_path + "\n")
    file.write("gt_path: " + gt_path + "\n")
    file.write("detect: " + detect + "\n")
    file.write("track: " + track + "\n")
    file.write("detect_failure: " + detect_failure + "\n")
    file.write("show: " + show + "\n")
    file.write("repeat_video: " + repeat_video + "\n")
    file.write("print_status: " + print_status + "\n")
    file.write("valid: " + valid + "\n")
    file.write("conf: " + conf + "\n")
    file.close()

if __name__ == "__main__":
    args = _getArgs()
    escreverYml(args.caminho, args.subcaminhoVideos, args.subcaminhoAnotacoes, args.categoria, args.video, args.BBinicial)
    