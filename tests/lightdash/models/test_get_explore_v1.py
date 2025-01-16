# Copyright 2025 yu-iskw
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unittest

from lightdash_ai_tools.lightdash.models.get_explore_v1 import Dimension, Metric


class TestDimension(unittest.TestCase):
    def test_reference(self):
        dimension = Dimension(table="orders", name="order_id")
        self.assertEqual(dimension.reference, "orders_order_id")

    def test_model_dump(self):
        dimension = Dimension(table="orders", name="order_id")
        result = dimension.model_dump(exclude_unset=True)
        expected = {
            "table": "orders",
            "name": "order_id",
            "reference": "orders_order_id",
        }
        self.assertDictEqual(result, expected)

class TestMetric(unittest.TestCase):
    def test_reference(self):
        metric = Metric(table="orders", name="num_unique_order_ids")
        self.assertEqual(metric.reference, "orders_num_unique_order_ids")

    def test_model_dump(self):
        metric = Metric(table="orders", name="num_unique_order_ids")
        result = metric.model_dump(exclude_unset=True)
        expected = {
            "table": "orders",
            "name": "num_unique_order_ids",
            "reference": "orders_num_unique_order_ids",
        }
        self.assertDictEqual(result, expected)
