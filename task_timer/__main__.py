import time
import click
import csv
 
class TaskTimer:
    def __init__(self):
        self.tasks = {}
        self.completed_tasks = {}
        # Load current running tasks from file
    
    

    def start_task(self, task_name):
        if task_name in self.tasks:
            print("Task already exists")
            return
        self.tasks[task_name] = time.time()
        print(f"Task {task_name} started")
    
    def stop_task(self, task_name):
        if task_name not in self.tasks:
            print("Task does not exist")
            return
        elapsed_time = time.time() - self.tasks[task_name]
        self.completed_tasks[task_name] = self.tasks.get(task_name, 0) + elapsed_time
        del self.tasks[task_name]
        print(f"Task {task_name} took {elapsed_time} seconds")
 
    def list_tasks(self):
        for task in self.tasks:
            print(task)
 
    def save_tasks(self):
        with open('tasks.csv', 'w') as csvfile:
            task_writer = csv.writer(csvfile)
            for task in self.tasks:
                task_writer.writerow([task])
 
    def load_tasks(self):
        with open('tasks.csv', 'r') as csvfile:
            task_reader = csv.reader(csvfile)
            for row in task_reader:
                self.tasks.append(row[0])



@click.command()
def main():


    timer = TaskTimer()

    while True:
        command = input("Enter command: ")
        if command == "start":
            task_name = input("Enter task name: ")
            timer.start_task(task_name)
        elif command == "stop":
            task_name = input("Enter task name: ")
            timer.stop_task(task_name)
        elif command == "list":
            timer.list_tasks()
        elif command == "save":
            timer.save_tasks()
        elif command == "load":
            timer.load_tasks()
        elif command == "exit":
            break
        else:
            print("Invalid command")

     


if __name__ == '__main__':
    main()