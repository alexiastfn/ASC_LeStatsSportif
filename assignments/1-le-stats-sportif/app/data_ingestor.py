""" Data Handler Module """
import csv

class DataIngestor:
    """ Manipulation of the .csv file """
    def __init__(self, csv_path: str):
        self.data = self.read_csv(csv_path)
        # TODO: Read csv from csv_path

        self.questions_best_is_min = [
            "Percent of adults aged 18 years and older who have an overweight classification",
            "Percent of adults aged 18 years and older who have obesity",
            "Percent of adults who engage in no leisure-time physical activity",
            "Percent of adults who report consuming fruit less than one time daily",
            "Percent of adults who report consuming vegetables less than one time daily",
        ]

        self.questions_best_is_max = [
            "Percent of adults who achieve at least 150 minutes a week of moderate-intensity "
            "aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic "
            "activity (or an equivalent combination)",
            "Percent of adults who achieve at least 150 minutes a week of moderate-intensity "
            "aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic "
            "physical activity and engage in muscle-strengthening activities on 2 or more days "
            "a week",
            "Percent of adults who achieve at least 300 minutes a week of moderate-intensity "
            "aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic "
            "activity (or an equivalent combination)",
            "Percent of adults who engage in muscle-strengthening activities on 2 or more days "
            "a week",
        ]

    def read_csv(self, csv_path):
        """ Translate the file into a dictionary """
        self.dictionary_data = []
        with open(csv_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.dictionary_data.append(row)
