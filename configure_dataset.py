import os
import glob
import json
import argparse
import numpy as np
import shutil

fsl_path = "/home/ubuntu/workspace/datasets/fsl_datasets/classes"
images_path = "/home/ubuntu/workspace/datasets/3d-printers/*"
labels_path = "/home/ubuntu/workspace/create_train_set/data/yolo-labels/*"

images = [[os.path.basename(os.path.splitext(x)[0]), os.path.splitext(x)[1]] for x in glob.glob(images_path)]
labels = [[os.path.basename(os.path.splitext(x)[0]), os.path.splitext(x)[1]] for x in glob.glob(labels_path)]

def configure_argparser():
    parser = argparse.ArgumentParser(description='Create FSL dataset from labelled YOLO dataset')
    parser.add_argument('-j', '--json', nargs=1,
                        help='JSON file to be processed', 
                        type=argparse.FileType('r'))
    
    return parser.parse_args()


def read_json(json_file):
    print("Reading JSON file")    
    j = json.load(json_file)

    return j["images_dir"], j["labels_dir"], j["class_names"], j["class_roots"]



if __name__ == "__main__":
    arguments = configure_argparser()
    images_dir, labels_dir, classes, class_paths = read_json(arguments.json[0])
    print("Images are in: " + images_dir)
    print("Labels are in: " + labels_dir)
    print("adding classes: " + str(classes))
    print("with file paths: " + str(class_paths))

    for path in class_paths:
        if not os.path.exists(path):
            os.mkdir(path)

    images = glob.glob(images_dir+"/*")
    labels = glob.glob(labels_dir+"/*")

    for image in images:
        lookup = os.path.join(labels_dir, os.path.basename(os.path.splitext(image)[0])+".txt")
        if lookup in labels:
            print(os.path.basename(os.path.splitext(image)[0]) + " is a photo of spaghetti")
            fdst = os.path.join(class_paths[0], os.path.basename(image))
            shutil.copyfile(image, fdst)
        else:
            print(os.path.basename(os.path.splitext(image)[0]) + " is not a photo of spaghetti")
            fdst = os.path.join(class_paths[1], os.path.basename(image))
            shutil.copyfile(image, fdst)




















