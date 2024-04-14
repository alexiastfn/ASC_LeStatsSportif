import unittest
from pathlib import Path
from app import DataIngestor
from app.task_runner import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.csv_dict = DataIngestor(
            "./nutrition_activity_obesity_usa_subset.csv"
        ).dictionary_data
        self.job_id = 0

    def test_task1_in1(self):
        self.job_id += 1
        request = StatesMeanRequest(
            self.csv_dict,
            "Percent of adults aged 18 years and older who have an overweight classification",
            self.job_id,
            None,
            None,
        )
        result = dict(request.helper())

        path_to_json = Path("./tests/states_mean/output/out-1.json")
        with open(path_to_json, "r") as file:
            expected_output = dict(json.load(file))

        for state, mean_value in result.items():
            expected_value = expected_output[state]
            self.assertAlmostEqual(mean_value, expected_value, delta=0.01)

    def test_task2_in1(self):
        self.job_id += 1
        request = StateMeanRequest(
            self.csv_dict,
            "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)",
            "Guam",
            self.job_id,
            None,
            None,
        )
        result = request.helper()

        path_to_json = Path("./tests/state_mean/output/out-1.json")
        with open(path_to_json, "r") as file:
            expected_output = json.load(file)

        self.assertAlmostEqual(result, expected_output["Guam"], delta=0.01)

    def test_task3_in1(self):
        self.job_id += 1
        request = BestOrWorstRequest(
            self.csv_dict,
            "Percent of adults aged 18 years and older who have an overweight classification",
            0,
            self.job_id,
            None,
            None,
        )
        result = dict(request.helper())

        path_to_json = Path("./tests/best5/output/out-1.json")
        with open(path_to_json, "r") as file:
            expected_output = dict(json.load(file))

        for state, mean_value in result.items():
            expected_value = expected_output[state]
            self.assertAlmostEqual(mean_value, expected_value, delta=0.01)

    def test_task4_in1(self):
        # worst5_request
        self.job_id += 1
        request = BestOrWorstRequest(
            self.csv_dict,
            "Percent of adults aged 18 years and older who have an overweight classification",
            1,
            self.job_id,
            None,
            None,
        )
        result = dict(request.helper())

        path_to_json = Path("./tests/worst5/output/out-1.json")
        with open(path_to_json, "r") as file:
            expected_output = dict(json.load(file))

        for state, mean_value in result.items():
            expected_value = expected_output[state]
            self.assertAlmostEqual(mean_value, expected_value, delta=0.01)

    def test_task5_in1(self):
        # global_mean
        self.job_id += 1
        request = GlobalMeanRequest(
            self.csv_dict,
            "Percent of adults aged 18 years and older who have an overweight classification",
            self.job_id,
            None,
            None,
        )
        result = request.helper()

        path_to_json = Path("./tests/global_mean/output/out-1.json")
        with open(path_to_json, "r") as file:
            expected_output = json.load(file)

        self.assertAlmostEqual(result, expected_output["global_mean"], delta=0.01)

    def test_task6_in1(self):
        self.job_id += 1
        request = DiffFromMeanRequest(
            self.csv_dict,
            "Percent of adults aged 18 years and older who have an overweight classification",
            self.job_id,
            None,
            None,
        )
        result = dict(request.helper())

        path_to_json = Path("./tests/diff_from_mean/output/out-1.json")
        with open(path_to_json, "r") as file:
            expected_output = dict(json.load(file))

        for state, mean_value in result.items():
            expected_value = expected_output[state]
            self.assertAlmostEqual(mean_value, expected_value, delta=0.01)

    def test_task7_in1(self):
        self.job_id += 1
        request = StateDiffFromMeanRequest(
            self.csv_dict,
            "Percent of adults who report consuming vegetables less than one time daily",
            "Virgin Islands",
            self.job_id,
            None,
            None,
        )
        result = request.helper()

        path_to_json = Path("./tests/state_diff_from_mean/output/out-1.json")
        with open(path_to_json, "r") as file:
            expected_output = json.load(file)

        self.assertAlmostEqual(result, expected_output["Virgin Islands"], delta=0.01)

    def test_task8_in1(self):
        self.job_id += 1
        request = StatesMeanCategoryRequest(
            self.csv_dict,
            "Percent of adults aged 18 years and older who have an overweight classification",
            self.job_id,
            None,
            None,
        )
        result = dict(request.helper())

        path_to_json = Path("./tests/mean_by_category/output/out-1.json")
        with open(path_to_json, "r") as file:
            expected_output = dict(json.load(file))

        for state, mean_value in result.items():
            expected_value = expected_output[state]
            self.assertAlmostEqual(mean_value, expected_value, delta=0.01)

    def test_task9_in1(self):
        self.job_id += 1
        request = StateMeanCategoryRequest(
            self.csv_dict,
            "Percent of adults aged 18 years and older who have an overweight classification",
            "Oklahoma",
            self.job_id,
            None,
            None,
        )
        result = dict(request.helper())

        path_to_json = Path("./tests/state_mean_by_category/output/out-1.json")
        with open(path_to_json, "r") as file:
            all_expected_output = json.load(file)
            expected_output = all_expected_output["Oklahoma"]

        for category, expected_mean in expected_output.items():
            with self.subTest(category=category):
                result_mean = result.get(category)
                self.assertIsNotNone(
                    result_mean, f"Missing category in result: {category}"
                )
                self.assertAlmostEqual(result_mean, expected_mean, delta=0.01)


if __name__ == "__main__":
    unittest.main()
