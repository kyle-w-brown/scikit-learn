"""
Base IO code for all datasets
"""

# Copyright (c) 2007 David Cournapeau <cournape@gmail.com>
#               2010 Fabian Pedregosa <fabian.pedregosa@inria.fr>
# License: Simplified BSD

import csv
import os

import numpy as np


class Bunch(dict):
    """ Container object for datasets: dictionnary-like object that
        exposes its keys as attributes.
    """

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self


def load_files(container_path, description=None, categories=None, shuffle=True,
               rng=42):
    """Load files with categories as subfolder names

    Individual samples are assumed to be files stored a two levels folder
    structure such as the following:

        container_folder/
            category_1_folder/
                file_1.txt
                file_2.txt
                ...
                file_42.txt
            category_2_folder/
                file_43.txt
                file_44.txt
                ...

    The folder names are used has supervised signal label names. The indivial
    file names are not important.

    This function does not try to extract features into a numpy array or
    scipy sparse matrix, nor does it try to load the files in memory.

    To use utf-8 text files in a scikit-learn classification or clustering
    algorithm you will first need to use the `scikits.learn.features.text`
    module to build a feature extraction transformer that suits your
    problem.

    Similar feature extractors should be build for other kind of unstructured
    data input such as images, audio, video, ...

    Parameters
    ----------

    container_path : string or unicode
      the path to the main folder holding one subfolder per category

    description: string or unicode
      a paragraph describing the characteristic of the dataset, its source,
      reference, ...

    categories : None or collection of string or unicode
      if None (default), load all the categories.
      if not Non, list of category names to load (other categories ignored)

    shuffle : True by default
      whether or not to shuffle the data: might be important for

    rng : a numpy random number generator or a seed integer, 42 by default
      used to shuffle the dataset

    Returns
    -------

    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'filenames', the files holding the raw to learn, 'target', the
        classification labels (integer index), 'target_names',
        the meaning of the labels, and 'DESCR', the full description of the
        dataset.

    """
    target = []
    target_names = []
    filenames = []

    folders = [f for f in sorted(os.listdir(container_path))
               if os.path.isdir(os.path.join(container_path, f))]

    if categories is not None:
        folders = [f for f in folders if f in categories]

    for label, folder in enumerate(folders):
        target_names.append(folder)
        folder_path = os.path.join(container_path, folder)
        documents = [os.path.join(folder_path, d)
                     for d in sorted(os.listdir(folder_path))]
        target.extend(len(documents) * [label])
        filenames.extend(documents)

    # convert as array for fancy indexing
    filenames = np.array(filenames)
    target = np.array(target)

    if shuffle:
        if isinstance(rng, int):
            rng = np.random.RandomState(rng)
        indices = np.arange(filenames.shape[0])
        rng.shuffle(indices)
        filenames = filenames[indices]
        target = target[indices]

    return Bunch(filenames=filenames,
                 target_names=target_names,
                 target=target,
                 DESCR=description)


################################################################################

def load_iris():
    """load the iris dataset and returns it.

    Returns
    -------
    data : Bunch
        Dictionnary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the classification labels,
        'target_names', the meaning of the labels, and 'DESCR', the
        full description of the dataset.

    Example
    -------
    Let's say you are interested in the samples 10, 25, and 50, and want to
    know their class name.

    >>> from scikits.learn.datasets import load_iris
    >>> data = load_iris()
    >>> data.target[[10, 25, 50]]
    array([0, 0, 1])
    >>> list(data.target_names)
    ['setosa', 'versicolor', 'virginica']

    """

    data_file = csv.reader(open(os.path.dirname(__file__)
                        + '/data/iris.csv'))
    fdescr = open(os.path.dirname(__file__)
                        + '/descr/iris.rst')
    temp = data_file.next()
    n_samples = int(temp[0])
    n_features = int(temp[1])
    target_names = np.array(temp[2:])
    data = np.empty((n_samples, n_features))
    target = np.empty((n_samples,), dtype=np.int)
    for i, ir in enumerate(data_file):
        data[i] = np.asanyarray(ir[:-1], dtype=np.float)
        target[i] = np.asanyarray(ir[-1], dtype=np.int)
    return Bunch(data=data, target=target, target_names=target_names,
                 DESCR=fdescr.read())


def load_digits():
    """load the digits dataset and returns it.

    Returns
    -------
    data : Bunch
        Dictionnary-like object, the interesting attributes are:
        'data', the data to learn, `images`, the images corresponding
        to each sample, 'target', the classification labels for each
        sample, 'target_names', the meaning of the labels, and 'DESCR',
        the full description of the dataset.

    Example
    -------
    To load the data and visualize the images::

        import pylab as pl
        digits = datasets.load_digits()
        pl.gray()
        # Visualize the first image:
        pl.matshow(digits.raw_data[0])

    """

    data = np.loadtxt(os.path.join(os.path.dirname(__file__)
                        + '/data/digits.csv.gz'), delimiter=',')
    fdescr = open(os.path.join(os.path.dirname(__file__)
                        + '/descr/digits.rst'))
    target = data[:, -1]
    flat_data = data[:, :-1]
    images = flat_data.view()
    images.shape = (-1, 8, 8)
    return Bunch(data=flat_data, target=target.astype(np.int),
                 target_names=np.arange(10),
                 images=images,
                 DESCR=fdescr.read())


def load_diabetes():
    base_dir = os.path.join(os.path.dirname(__file__), 'data/')
    data   = np.loadtxt(base_dir + 'diabetes_data.csv.gz')
    target = np.loadtxt(base_dir + 'diabetes_target.csv.gz')
    return Bunch (data=data, target=target)
