# processing_plugins/base.py

from abc import ABC, abstractmethod


class ProcessingPlugin(ABC):
    @abstractmethod
    def process(self, data):
        """处理数据的抽象方法"""
        pass
