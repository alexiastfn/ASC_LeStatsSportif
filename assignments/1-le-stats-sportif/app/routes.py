""" Routes Module """
import os
from app import webserver
from flask import request, jsonify
import json
from app.task_runner import *
from app.logger import server_logger

@webserver.route("/api/get_results/<job_id>", methods=["GET"])
def get_response(job_id):
    """ Implement the get_results route """
    job_id = int(job_id)
    server_logger.info("[START] /api/get_results/%s", job_id)

    if job_id > webserver.job_counter:
        server_logger.error("[END] /api/get_results/%s", job_id)
        return jsonify({"status": "error", "reason": "Invalid job_id"})

    if job_id not in webserver.tasks_runner.requests_dict:
        server_logger.warning("[END] /api/get_results/%s", job_id)
        return jsonify({"status": "running"})

    try:
        if webserver.tasks_runner.requests_dict[job_id] is True:
            with open(f"results/out-{job_id}.json", "r") as output_file:
                content = output_file.read()
                job_data = json.loads(content)
                server_logger.info("[END] /api/get_results/%s%s", job_id, job_data)
                return jsonify({"status": "done", "data": job_data})
        else:
            server_logger.info("[END] /api/get_results/%s", job_id)
            return jsonify({"status": "running"})

    except json.JSONDecodeError:
        server_logger.exception("[END] /api/get_results/%s", job_id)
        return jsonify({"status": "running"})


@webserver.route("/api/states_mean", methods=["POST"])
def states_mean_request():
    """ Implement the states_mean route """
    server_logger.warning("[START] /api/states_mean/%s", webserver.job_counter)
    data_dict = webserver.data_ingestor.dictionary_data
    data = request.json
    question = data.get("question")
    webserver.tasks_runner.addTask(
        StatesMeanRequest(
            data_dict,
            question,
            webserver.job_counter,
            webserver.tasks_runner.requests_dict,
            webserver.tasks_runner.mutex,
        )
    )
    server_logger.warning("[END] /api/states_mean/%s", webserver.job_counter)
    webserver.job_counter += 1
    return jsonify({"status": "done", "job_id": webserver.job_counter - 1})


def save_to_text_file(self, sorted_means, file_path):
    """ Original function from file """
    with open(file_path, "w") as file:
        for state, mean in sorted_means:
            file.write(f"{state}: {mean}\n")


@webserver.route("/api/state_mean", methods=["POST"])
def state_mean_request():
    """ Implement the state_mean route """
    server_logger.warning("[START] /api/state_mean/%s", webserver.job_counter)
    data_dict = webserver.data_ingestor.dictionary_data

    data = request.json
    print(data)
    question = data.get("question")
    state = data.get("state")

    webserver.tasks_runner.addTask(
        StateMeanRequest(
            data_dict,
            question,
            state,
            webserver.job_counter,
            webserver.tasks_runner.requests_dict,
            webserver.tasks_runner.mutex,
        )
    )
    server_logger.warning("[END] /api/state_mean/%s", webserver.job_counter)
    webserver.job_counter += 1
    return jsonify({"status": "done", "job_id": webserver.job_counter - 1})


@webserver.route("/api/best5", methods=["POST"])
def best5_request():
    """ Implement the best_5 route """
    server_logger.warning("[START] /api/best5/%s", webserver.job_counter)
    data_dict = webserver.data_ingestor.dictionary_data
    data = request.json
    question = data.get("question")

    if question in webserver.data_ingestor.questions_best_is_max:
        max = 1  # cele mai bune rezultate => worst
    else:
        max = 0  # cele mai bune rezultate => best

    webserver.tasks_runner.addTask(
        BestOrWorstRequest(
            data_dict,
            question,
            max,
            webserver.job_counter,
            webserver.tasks_runner.requests_dict,
            webserver.tasks_runner.mutex,
        )
    )
    server_logger.warning("[END] /api/best5/%s", webserver.job_counter)
    webserver.job_counter += 1
    return jsonify({"status": "done", "job_id": webserver.job_counter - 1})


@webserver.route("/api/worst5", methods=["POST"])
def worst5_request():
    """ Implement the worst_5 route """
    server_logger.warning("[START] /api/worst5/%s", webserver.job_counter)
    data_dict = webserver.data_ingestor.dictionary_data
    data = request.json
    question = data.get("question")

    if question in webserver.data_ingestor.questions_best_is_max:
        max = 0  # cele mai bune rezultate => cele mai mari
    else:
        max = 1  # cele mai bune rezultate => cele mai mici

    webserver.tasks_runner.addTask(
        BestOrWorstRequest(
            data_dict,
            question,
            max,
            webserver.job_counter,
            webserver.tasks_runner.requests_dict,
            webserver.tasks_runner.mutex,
        )
    )
    server_logger.warning("[END] /api/worst5/%s", webserver.job_counter)
    webserver.job_counter += 1
    return jsonify({"status": "done", "job_id": webserver.job_counter - 1})


@webserver.route("/api/global_mean", methods=["POST"])
def global_mean_request():
    """ Implement the global_mean route """
    server_logger.warning("[START] /api/global_mean/%s", webserver.job_counter)
    data_dict = webserver.data_ingestor.dictionary_data
    data = request.json
    question = data.get("question")
    webserver.tasks_runner.addTask(
        GlobalMeanRequest(
            data_dict,
            question,
            webserver.job_counter,
            webserver.tasks_runner.requests_dict,
            webserver.tasks_runner.mutex,
        )
    )
    server_logger.warning("[END] /api/global_mean/%s", webserver.job_counter)
    webserver.job_counter += 1
    return jsonify({"status": "done", "job_id": webserver.job_counter - 1})


@webserver.route("/api/diff_from_mean", methods=["POST"])
def diff_from_mean_request():
    """ Implement the diff_from_mean route """
    server_logger.warning("[START] /api/diff_from_mean/%s", webserver.job_counter)
    data_dict = webserver.data_ingestor.dictionary_data
    data = request.json
    question = data.get("question")
    webserver.tasks_runner.addTask(
        DiffFromMeanRequest(
            data_dict,
            question,
            webserver.job_counter,
            webserver.tasks_runner.requests_dict,
            webserver.tasks_runner.mutex,
        )
    )
    server_logger.warning("[START] /api/diff_from_mean/%s", webserver.job_counter)
    webserver.job_counter += 1
    return jsonify({"status": "done", "job_id": webserver.job_counter - 1})


@webserver.route("/api/state_diff_from_mean", methods=["POST"])
def state_diff_from_mean_request():
    """ Implement the state_diff_from_mean route """
    server_logger.warning("[START] /api/state_diff_from_mean/%s", webserver.job_counter)
    data_dict = webserver.data_ingestor.dictionary_data

    data = request.json
    print(data)
    question = data.get("question")
    state = data.get("state")

    webserver.tasks_runner.addTask(
        StateDiffFromMeanRequest(
            data_dict,
            question,
            state,
            webserver.job_counter,
            webserver.tasks_runner.requests_dict,
            webserver.tasks_runner.mutex,
        )
    )
    server_logger.warning("[END] /api/state_diff_from_mean/%s", webserver.job_counter)
    webserver.job_counter += 1
    return jsonify({"status": "done", "job_id": webserver.job_counter - 1})


@webserver.route("/api/mean_by_category", methods=["POST"])
def mean_by_category_request():
    """ Implement the mean_by_category route """
    server_logger.warning("[START] /api/mean_by_category/%s", webserver.job_counter)
    data_dict = webserver.data_ingestor.dictionary_data
    data = request.json
    question = data.get("question")
    webserver.tasks_runner.addTask(
        StatesMeanCategoryRequest(
            data_dict,
            question,
            webserver.job_counter,
            webserver.tasks_runner.requests_dict,
            webserver.tasks_runner.mutex,
        )
    )
    server_logger.warning("[END] /api/mean_by_category/%s", webserver.job_counter)
    webserver.job_counter += 1
    return jsonify({"status": "done", "job_id": webserver.job_counter - 1})


@webserver.route("/api/state_mean_by_category", methods=["POST"])
def state_mean_by_category_request():
    """ Implement the state_mean_by_category route """
    server_logger.warning("[START] /api/state_mean_by_category/%s", webserver.job_counter)
    data_dict = webserver.data_ingestor.dictionary_data

    data = request.json
    print(data)
    question = data.get("question")
    state = data.get("state")

    webserver.tasks_runner.addTask(
        StateMeanCategoryRequest(
            data_dict,
            question,
            state,
            webserver.job_counter,
            webserver.tasks_runner.requests_dict,
            webserver.tasks_runner.mutex,
        )
    )
    server_logger.warning("[END] /api/state_mean_by_category/%s", webserver.job_counter)
    webserver.job_counter += 1
    return jsonify({"status": "done", "job_id": webserver.job_counter - 1})


@webserver.route("/api/graceful_shutdown", methods=["GET"])
def graceful_shutdown():
    """ Implement the shutdown route """
    server_logger.warning("[START] /api/graceful_shutdown/")
    webserver.tasks_runner.stop()
    server_logger.warning("[END] /api/graceful_shutdown/")
    return jsonify({"status": "done"})


@webserver.route("/api/num_jobs", methods=["GET"])
def num_jobs():
    """ Implement the num_jobs route """
    server_logger.info("[START] /api/num_jobs/")
    output_files = os.listdir("results/")
    done_jobs = len(output_files)
    result = webserver.job_counter - done_jobs
    server_logger.warning("[END] /api/num_jobs/%s", result)

    return jsonify({"num jobs": result})


@webserver.route("/api/jobs", methods=["GET"])
def api_jobs():
    """ Implement the jobs route """
    server_logger.info("[START] /api/jobs/")
    job_statuses = []
    for job_id, is_completed in webserver.tasks_runner.requests_dict.items():
        status = "done" if is_completed else "running"
        job_statuses.append({f"job_id_{job_id}": status})

    result = {"status": "done", "data": job_statuses}
    server_logger.warning("[END] /api/jobs/%s", result)
    return jsonify(result)


# You can check localhost in your browser to see what this displays
@webserver.route("/")
@webserver.route("/index")
def index():
    """ Original function from file """
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg


def get_defined_routes():
    """ Original function from file """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ", ".join(rule.methods)
        routes.append(f'Endpoint: "{rule}" Methods: "{methods}"')
    return routes
