"""
Module in which there is the implementation of the thread pool, threads and tasks
"""
import threading
import os
from threading import Thread
from collections import defaultdict
import json
from queue import Queue
from app.logger import server_logger


class Task:
    """ Task Class - the parent class of every type of request """
    def __init__(self, data_dict, question, job_id, requests_map, mutex):
        self.data_dict = data_dict
        self.question = question
        self.job_id = job_id
        self.requests_map = requests_map
        self.mutex = mutex

    def acces_requests_dict(self, flag):
        """ To keep track of invalid/running/done tasks """
        if self.mutex is None and self.acces_requests_dict is False:
            return
        with self.mutex:
            self.requests_map[self.job_id] = flag


class StatesMeanRequest(Task):
    """ StatesMeanRequest - for the '/api/states_mean' requests """
    def __init__(self, data_dict, question, job_id, requests_map, mutex):
        super().__init__(data_dict, question, job_id, requests_map, mutex)

    def helper(self):
        """ The logic of the request """
        state_sums = defaultdict(float)
        state_counts = defaultdict(int)

        for row in self.data_dict:
            if row["Question"] == self.question:
                state = row["LocationDesc"]
                value = float(row["Data_Value"])
                state_sums[state] += value
                state_counts[state] += 1

        state_means = {
            state: state_sums[state] / state_counts[state] for state in state_sums
        }
        sorted_states_by_mean = sorted(state_means.items(), key=lambda item: item[1])
        return sorted_states_by_mean

    def execute(self):
        """ Writing in the necessary output file """
        sorted_states_by_mean = self.helper()

        output_path = f"results/out-{self.job_id}.json"
        with open(output_path, "w") as json_file:
            json.dump(dict(sorted_states_by_mean), json_file)
            self.acces_requests_dict(True)
            server_logger.info("[MIDDLE] /api/states_mean/%s", self.job_id)


class StateMeanRequest(Task):
    """ StateMeanRequest - for the '/api/state_mean' requests """
    def __init__(self, data_dict, question, state, job_id, requests_map, mutex):
        super().__init__(data_dict, question, job_id, requests_map, mutex)
        self.state = state

    def helper(self):
        """ The logic of the request """
        state_sum = 0.0
        state_count = 0

        for row in self.data_dict:
            if row["Question"] == self.question and row["LocationDesc"] == self.state:
                value = float(row["Data_Value"])
                state_sum += value
                state_count += 1

        state_mean = state_sum / state_count if state_count else None
        return state_mean

    def execute(self):
        """ Writing in the necessary output file """
        state_mean = self.helper()

        output_path = f"results/out-{self.job_id}.json"
        with open(output_path, "w") as json_file:
            result = {self.state: state_mean}
            json.dump(result, json_file)
            self.acces_requests_dict(True)
            server_logger.info("[MIDDLE] /api/state_mean/%s", self.job_id)


class BestOrWorstRequest(Task):
    """ BestOrWorstRequest - for the '/api/best5 or worst5' requests """
    def __init__(self, data_dict, question, max, job_id, requests_map, mutex):
        super().__init__(data_dict, question, job_id, requests_map, mutex)
        self.max = max

    def helper(self):
        """ The logic of the request """
        state_sums = defaultdict(float)
        state_counts = defaultdict(int)

        for row in self.data_dict:
            if row["Question"] == self.question:
                state = row["LocationDesc"]
                value = float(row["Data_Value"])
                state_sums[state] += value
                state_counts[state] += 1

        state_means = {
            state: state_sums[state] / state_counts[state] for state in state_sums
        }
        reverse_sort = bool(self.max)
        states = sorted(
            state_means.items(), key=lambda item: item[1], reverse=reverse_sort
        )[:5]
        return states

    def execute(self):
        """ Writing in the necessary output file """
        states = self.helper()
        output_path = f"results/out-{self.job_id}.json"
        with open(output_path, "w") as json_file:
            json.dump(dict(states), json_file)
            self.acces_requests_dict(True)
            server_logger.info("[MIDDLE] /api/best5/%s", self.job_id)


class GlobalMeanRequest(Task):
    """ GlobalMeanRequest - for the '/api/global_mean' requests """
    def __init__(self, data_dict, question, job_id, requests_map, mutex):
        super().__init__(data_dict, question, job_id, requests_map, mutex)

    def helper(self):
        """ The logic of the request """
        total_sum = 0.0
        count = 0

        for row in self.data_dict:
            if row["Question"] == self.question:
                value = float(row["Data_Value"])
                total_sum += value
                count += 1

        mean_value = total_sum / count if count > 0 else None
        return mean_value

    def execute(self):
        """ Writing in the necessary output file """
        mean_value = self.helper()
        output_path = f"results/out-{self.job_id}.json"
        with open(output_path, "w") as json_file:
            result = {"global_mean": mean_value}
            json.dump(result, json_file)
            self.acces_requests_dict(True)
            server_logger.info("[MIDDLE] /api/global_mean/%s", self.job_id)


class DiffFromMeanRequest(Task):
    """ DiffFromMeanRequest - for the '/api/diff_from_mean' requests """
    def __init__(self, data_dict, question, job_id, requests_map, mutex):
        super().__init__(data_dict, question, job_id, requests_map, mutex)

    def helper(self):
        """ The logic of the request """
        states_mean_req = StatesMeanRequest(
            self.data_dict, self.question, self.job_id, self.requests_map, self.mutex
        )
        states_mean_dict = states_mean_req.helper()

        global_mean_req = GlobalMeanRequest(
            self.data_dict, self.question, self.job_id, self.requests_map, self.mutex
        )
        global_mean = global_mean_req.helper()
        dif_dict = {state: global_mean - mean for state, mean in states_mean_dict}
        return dif_dict

    def execute(self):
        """ Writing in the necessary output file """
        dif_dict = self.helper()
        output_path = f"results/out-{self.job_id}.json"
        with open(output_path, "w") as json_file:
            json.dump(dict(dif_dict), json_file)
            self.acces_requests_dict(True)
            server_logger.info("[MIDDLE] /api/diff_from_mean/%s", self.job_id)


class StateDiffFromMeanRequest(Task):
    """ StateDiffFromMeanRequest - for the '/api/state_diff_from_mean' requests """
    def __init__(self, data_dict, question, state, job_id, requests_map, mutex):
        super().__init__(data_dict, question, job_id, requests_map, mutex)
        self.state = state

    def helper(self):
        """ The logic of the request """
        state_mean_req = StateMeanRequest(
            self.data_dict,
            self.question,
            self.state,
            self.job_id,
            self.requests_map,
            self.mutex,
        )
        state_mean = state_mean_req.helper()

        global_mean_req = GlobalMeanRequest(
            self.data_dict, self.question, self.job_id, self.requests_map, self.mutex
        )
        global_mean = global_mean_req.helper()
        state_diff_from_mean = global_mean - state_mean
        return state_diff_from_mean

    def execute(self):
        """ Writing in the necessary output file """
        state_diff_from_mean = self.helper()
        output_path = f"results/out-{self.job_id}.json"
        with open(output_path, "w") as json_file:
            result = {self.state: state_diff_from_mean}
            json.dump(result, json_file)
            self.acces_requests_dict(True)
            server_logger.info("[MIDDLE] /api/state_diff_from_mean/%s", self.job_id)


class StatesMeanCategoryRequest(Task):
    """ StatesMeanCategoryRequest - for the '/api/mean_by_category' requests """
    def __init__(self, data_dict, question, job_id, requests_map, mutex):
        super().__init__(data_dict, question, job_id, requests_map, mutex)

    def helper(self):
        """ The logic of the request """
        sum_dict = defaultdict(float)
        count_dict = defaultdict(int)

        for row in self.data_dict:
            if row["Question"] == self.question:
                if row["StratificationCategory1"] and row["Stratification1"]:
                    loc_desc = row["LocationDesc"]
                    strat_cat = row["StratificationCategory1"]
                    strat = row["Stratification1"]
                    key = f"('{loc_desc}', '{strat_cat}', '{strat}')"
                    sum_dict[key] += float(row["Data_Value"])
                    count_dict[key] += 1

        mean_values = {
            key: round(sum_dict[key] / count_dict[key], 2) for key in sum_dict
        }

        mean_values_sorted = {key: mean_values[key] for key in sorted(mean_values)}

        return mean_values_sorted

    def execute(self):
        """ Writing in the necessary output file """
        state_mean_category_dict = self.helper()

        output_path = f"results/out-{self.job_id}.json"
        with open(output_path, "w") as json_file:
            json.dump(dict(state_mean_category_dict), json_file)
            self.acces_requests_dict(True)
            server_logger.info("[MIDDLE] /api/mean_by_category/%s", self.job_id)


class StateMeanCategoryRequest(Task):
    """ StateMeanCategoryRequest - for the '/api/state_mean_by_category' requests """
    def __init__(self, data_dict, question, state, job_id, requests_map, mutex):
        super().__init__(data_dict, question, job_id, requests_map, mutex)
        self.state = state

    def helper(self):
        """ The logic of the request """
        sum_dict = defaultdict(float)
        count_dict = defaultdict(int)

        for row in self.data_dict:
            if row["Question"] == self.question and row["LocationDesc"] == self.state:
                key = (
                    f"('{row['StratificationCategory1']}', '{row['Stratification1']}')"
                )
                sum_dict[key] += float(row["Data_Value"])
                count_dict[key] += 1

        mean_values = {
            key: round(sum_dict[key] / count_dict[key], 2) for key in sum_dict
        }
        mean_values_sorted = {key: mean_values[key] for key in sorted(mean_values)}

        return mean_values_sorted

    def execute(self):
        """ Writing in the necessary output file """

        state_mean_category_dict = self.helper()
        answer = {self.state: state_mean_category_dict}

        output_path = f"results/out-{self.job_id}.json"
        with open(output_path, "w") as json_file:
            json.dump(answer, json_file)
            self.acces_requests_dict(True)
            server_logger.info("[MIDDLE] /api/state_mean_by_category/%s", self.job_id)


class StopRequest(Task):
    """ StopRequest - when the thread pool needs to shutdown """
    def __init__(self):
        super().__init__(None, None, 0, None, None)


class TaskRunner(Thread):
    """ TaskRunner - Thread's blue print """
    def __init__(self, queue):
        super().__init__()
        self.q = queue

    def run(self):
        """ Thread's implementation """
        while True:
            temp_task = self.q.get()
            if isinstance(temp_task, StopRequest):
                return
            temp_task.execute()

            self.q.task_done()


class ThreadPool:
    """ ThreadPool - the ThreadPool class """
    def __init__(self):
        self.queue = Queue()
        self.stop = False
        self.requests_dict = {}
        self.mutex = threading.Lock()
        self.no_threads = self.get_no_threads()
        self.threads = []

    def get_no_threads(self):
        """ getNoThreads - number of threads """
        num_threads = os.environ.get("TP_NUM_OF_THREADS")
        if num_threads is not None:
            return int(num_threads)
        else:
            return os.cpu_count()

    def start(self):
        """ start - activate the threads """
        for i in range(self.no_threads):
            t = TaskRunner(self.queue)
            self.threads.append(t)
            t.start()

    def stop(self):
        """ end - kill the threads """
        for i in range(self.no_threads):
            self.queue.put(StopRequest())

        for i in range(self.no_threads):
            self.threads[i].join()

    def addTask(self, task):
        """ addTask - add request in threadpool's queue """
        self.queue.put(task)
