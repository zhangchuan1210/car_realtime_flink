# processing_plugins/double_value_plugin.py

from processing_plugins.base import ProcessingPlugin


class DoubleValuePlugin(ProcessingPlugin):
    def process(self, data):
        result_key = data.get('user_id')
        result_value = data.get('oil_avg') * 2
        return (result_key, result_value)
