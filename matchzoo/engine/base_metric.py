"""Metric base class and some related utilities."""

import random
import typing
import abc

import numpy as np


class BaseMetric(abc.ABC):
    """Metric base class."""

    ALIAS = 'base_metric'

    @abc.abstractmethod
    def __call__(self, y_true: np.array, y_pred: np.array) -> float:
        """
        Call to compute the metric.

        :param y_true: An array of groud truth labels.
        :param y_pred: An array of predicted values.
        :return: Evaluation of the metric.
        """

    @abc.abstractmethod
    def __repr__(self):
        """:return: Formated string representation of the metric."""


def sort_and_couple(labels: list, scores: list) -> list:
    """Zip the `labels` with `scores` into a single list."""
    couple = list(zip(labels, scores))
    random.shuffle(couple)
    sorted_couple = sorted(couple, key=lambda x: x[1], reverse=True)
    return sorted_couple


def parse_metric(metric: typing.Union[str,
                                      typing.Type[BaseMetric],
                                      BaseMetric]):
    """
    Parse input metric in any form into a :class:`BaseMetric` instance.

    :param metric: Input metric in any form.
    :return: A :class:`BaseMetric` instance

    Examples::
        >>> from matchzoo import engine, metrics

    Use `str` as keras native metrics:
        >>> engine.parse_metric('mse')
        'mse'

    Use `str` as MatchZoo metrics:
        >>> mz_metric = engine.parse_metric('map')
        >>> type(mz_metric)
        <class 'matchzoo.metrics.MeanAveragePrecision'>

    Use :class:`matchzoo.engine.BaseMetric` subclasses as MatchZoo metrics:
        >>> type(engine.parse_metric(metrics.AveragePrecision))
        <class 'matchzoo.metrics.AveragePrecision'>

    Use :class:`matchzoo.engine.BaseMetric` instances as MatchZoo metrics:
        >>> type(engine.parse_metric(metrics.AveragePrecision()))
        <class 'matchzoo.metrics.AveragePrecision'>

    """
    if isinstance(metric, BaseMetric):
        return metric
    elif isinstance(metric, str):
        metric = metric.lower()  # ignore case
        for subclass in BaseMetric.__subclasses__():
            if metric == subclass.ALIAS or metric in subclass.ALIAS:
                return subclass()
        return metric  # keras native metrics
    elif issubclass(metric, BaseMetric):
        return metric()
