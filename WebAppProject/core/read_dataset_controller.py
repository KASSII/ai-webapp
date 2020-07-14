from . import classification

def load_data(task_type, dataset_path, start_idx, request_data_num):
    res = None
    if task_type == "classification":
        res = classification.read_dataset.load_data(dataset_path, start_idx, request_data_num)
    return res