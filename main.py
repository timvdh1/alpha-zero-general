from Coach import Coach
from wondevwoman.WonDevGame import WonDevGame as Game

#g = Game(4)
#g.getValidMoves(g.getInitBoard(), -1)
from wondevwoman.pytorch.NNet import NNetWrapper as nn
from utils import *


args = dotdict({
    'numIters': 1000,
    'numEps': 1,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 25,
    'arenaCompare': 40,
    'cpuct': 1,

    'checkpoint': './tempx/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

if __name__=="__main__":

    g = Game(6)
    nnet = nn(g)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
