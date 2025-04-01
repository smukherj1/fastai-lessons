from duckduckgo_search import DDGS
import fastcore.all as fc
import fastai.vision.all as fv
import time
import json
from fastdownload import download_url
import matplotlib.pyplot as plt


def search_images(keywords, max_images=200): return fc.L(
    DDGS().images(keywords, max_results=max_images)).itemgot('image')


def download_training_data():
  searches = 'cake', 'pizza'
  path = fc.Path('data')

  for o in searches:
    dest = (path/o)
    dest.mkdir(exist_ok=True, parents=True)
    fv.download_images(dest, urls=search_images(f'{o} photo'))
    fv.resize_images(path/o, max_size=400, dest=path/o)
  n = len(fv.get_image_files(path))
  print("Download {} images.".format(n))
  failed = fv.verify_images(fv.get_image_files(path))
  failed.map(fc.Path.unlink)
  print("Removed {} images that failed to verify.".format(failed))

if __name__ == "__main__":
  # download_training_data()
  dls = fv.DataBlock(
    blocks=(fv.ImageBlock, fv.CategoryBlock), 
    get_items=fv.get_image_files, 
    splitter=fv.RandomSplitter(valid_pct=0.2, seed=42),
    get_y=fv.parent_label,
    item_tfms=[fv.Resize(192, method='squish')]
  ).dataloaders(fc.Path('data'), bs=32)

  learn = fv.vision_learner(dls, fv.resnet18, metrics=fv.error_rate)
  learn.fine_tune(3)
  a, b, c = learn.predict(fv.PILImage.create('cake.jpeg'))
  print("Predict cake", a, b, c)
  a, b, c = learn.predict(fv.PILImage.create('score_pizza.jpg'))
  print("Predict score_pizza", a, b, c)
