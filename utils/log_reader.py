def read_log_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        logs = file.readlines()
    return logs
