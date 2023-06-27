import argparse
import os
import shutil
from model_skeleton import Model
from dataset_maker import Dataset
from train import *
from checkpoint import *
from data_prep import *
from data_chunks import *

parser = argparse.ArgumentParser()
parser.add_argument('--max-epochs', type=int, default=5)
parser.add_argument('--batch-size', type=int, default=256)
parser.add_argument('--sequence-length', type=int, default=6)
parser.add_argument('--no-prepared-data', action='store_true')
parser.add_argument('--next-words', type=int, default=100)
parser.add_argument('--chunk-size', type=int, default=4998)
parser.add_argument('--model-checkpoint', type=str, default="savestate")
parser.add_argument('--no-create-chunks', action='store_true')
parser.add_argument('source', type=str)
parser.add_argument('text', type=str)
args = parser.parse_args()

if (args.no_prepared_data):
    if (os.path.isfile("clean_tweets")):
        os.remove("clean_tweets")
    if (os.path.isfile(args.model_checkpoint)):
        os.remove(args.model_checkpoint)

# Logic to make sure data chunks are not created in vain
# The chunk size is used as an indicatior on if the chunks are 'fresh'
if (not check_flag(args)):
    clean_data_dir()
    split_into_chunks(args)
    write_flag(args)

if (not (os.path.isfile("clean_tweets")) or args.no_prepared_data):
    directory = os.fsencode("./data/")
    for file in os.listdir(directory):
        filename =  os.path.join("./data/", os.fsdecode(file))
        tweets = persian_only(filename)
        normalize_tweets(tweets, "clean_tweets")

dataset = Dataset(args)
model = Model(dataset)

if (not (os.path.isfile(args.model_checkpoint)) or args.no_prepared_data):
    train(dataset, model, args)
    checkpoint(model, args.model_checkpoint)

resume(model, args.model_checkpoint)
print(predict(dataset, model, text=args.text, next_words=args.next_words))