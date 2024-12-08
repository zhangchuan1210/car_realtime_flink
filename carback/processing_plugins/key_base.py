from abc import abstractmethod, ABC

from pyflink.datastream import KeyedProcessFunction

from processing_plugins.base import ProcessingPlugin


class KeyProcessingPlugin(ProcessingPlugin, KeyedProcessFunction):
    pass
