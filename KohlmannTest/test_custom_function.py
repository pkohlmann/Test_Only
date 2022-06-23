import logging
from iotfunctions.db import Database
from iotfunctions.base import BaseTransformer
from iotfunctions.ui import UIExpression, UIFunctionOutSingle
import numpy as np

PACKAGE_URL = 'git+https://github.com/pkohlmann/Test_Only.git@'

class KohlmannTestFunction2(BaseTransformer):

    def __init__(self, conditional_expression, true_expression, false_expression, output_item=None):
        super().__init__()
        self.conditional_expression = self.parse_expression(conditional_expression)
        self.true_expression = self.parse_expression(true_expression)
        self.false_expression = self.parse_expression(false_expression)
        if output_item is None:
            self.output_item = 'output_item'
        else:
            self.output_item = output_item

    def execute(self, df):
        try:
            c = self._entity_type.get_attributes_dict()
        except Exception:
            c = None
        df = df.copy()
        df[self.output_item] = np.where(eval(self.conditional_expression), eval(self.true_expression),
                                        eval(self.false_expression))
        return df

    @classmethod
    def build_ui(cls):
        # define arguments that behave as function inputs
        inputs = []
        inputs.append(UIExpression(name='conditional_expression', description="expression that returns a True/False value, \
                                                eg. if df['temp']>50 then df['temp'] else None"))
        inputs.append(UIExpression(name='true_expression', description="expression when true, eg. df['temp']"))
        inputs.append(UIExpression(name='false_expression', description='expression when false, eg. None'))
        # define arguments that behave as function outputs
        outputs = []
        outputs.append(UIFunctionOutSingle(name='output_item', datatype=bool, description='Dummy function output'))

        return (inputs, outputs)

    def get_input_items(self):
        items = self.get_expression_items([self.conditional_expression, self.true_expression, self.false_expression])
        return items


