"""
LensKit algorithms.

The `lenskit.algorithms` package contains several example algorithms for carrying out recommender
experiments.  These algorithm implementations are designed to mimic the characteristics of the
implementations provided by the original LensKit Java package.  It also provides abstract base
classes (:py:mod:`abc`) representing different algorithm capabilities.
"""

from abc import ABCMeta, abstractmethod
import pickle


class Predictor(metaclass=ABCMeta):
    """
    Predicts user ratings of items.  Predictions are really estimates of the user's like or
    dislike, and the ``Predictor`` interface makes no guarantees about their scale or
    granularity.
    """

    @abstractmethod
    def predict(self, model, user, items, ratings=None):
        """
        Compute predictions for a user and items.

        Args:
            model:
                the trained model to use.  Either ``None`` or the ratings matrix if the
                algorithm has no concept of training.
            user: the user ID
            items (array-like): the items to predict
            ratings (pandas.Series):
                the user's ratings (indexed by item id); if provided, they may be used to
                override or augment the model's notion of a user's preferences.

        Returns:
            pandas.Series: scores for the items, indexed by item id.
        """
        raise NotImplemented()


class Trainable(metaclass=ABCMeta):
    """
    Models that can be trained and have their models saved.
    """

    @abstractmethod
    def train(self, ratings):
        """
        Train the model on rating/consumption data.  Training methods that require additional
        data may accept it as additional parameters or via class members.

        Args:
            ratings(pandas.DataFrame):
                rating data, as a matrix with columns ‘user’, ‘item’, and ‘rating’. The
                user and item identifiers may be of any type.

        Returns:
            the trained model (of an implementation-defined type).
        """
        raise NotImplemented()

    def save_model(self, model, file):
        """
        Save a trained model to a file.  The default implementation pickles the model.

        Algorithms are allowed to use any format for saving their models, including
        directories.

        Args:
            model: the trained model.
            file(string):
                the file in which to save the model.
        """

        with open(file, 'wb') as f:
            pickle.dump(model, f)

    def load_model(self, file):
        """
        Save a trained model to a file.

        Args:
            file(string): the path to file from which to load the model.

        Returns:
            the trained model (of an implementation-defined type).
        """
        with open(file, 'rb') as f:
            return pickle.load(f)
