import os
import traceback
import weka.core.jvm as jvm
from weka.core.classes import Random
from weka.core.converters import Loader
from weka.core.dataset import Instances
from weka.classifiers import Classifier
from weka.filters import Filter

def main():
    data_file="data_repo/arff/UPDOWN134_6_6.arff";
    loader = Loader("weka.core.converters.ArffLoader")
    data = loader.load_file(data_file)
    data.class_is_first()
    classifier = Classifier(classname="weka.classifiers.trees.J48")

if __name__ == '__main__':
    jvm.start()
    main()
    jvm.stop()
