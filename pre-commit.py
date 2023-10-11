import datetime


with open('pre_commit_file.txt', 'r') as file:
    paths = file.read().splitlines()

current_time = datetime.datetime.now()

for path in paths:
    with open(path, 'r') as file:
        content = file.read()

    new_content = f"# commit_time = {current_time}\n{content}"

    with open(path, 'w') as file:
        file.write(new_content)
