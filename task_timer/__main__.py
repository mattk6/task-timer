import time
import click
import json

TASKS_FILE = "tasks.json"

class TaskTimer:
    def __init__(self):
        self.running_tasks = {}  # Store running tasks with start times
        self.completed_tasks = {}  # Store completed tasks with elapsed times
        self.load_tasks()

    def start_task(self, task_name):
        """Start a new task."""
        if task_name in self.running_tasks:
            click.echo(f"Task '{task_name}' is already running.")
            return
        self.running_tasks[task_name] = time.time()  # Store the start time
        click.echo(f"Started task: {task_name}")
        self.save_tasks()

    def stop_task(self, task_name):
        """Stop a running task."""
        if task_name in self.running_tasks:
            elapsed_time = time.time() - self.running_tasks.pop(task_name)
            click.echo(f"Stopped task: {task_name}. Time logged: {elapsed_time:.2f} seconds.")
            self.completed_tasks[task_name] = self.running_tasks.get(task_name, 0) + elapsed_time
            self.save_tasks()
        else:
            click.echo(f"Task '{task_name}' is not currently running.")

    def save_tasks(self):
        """Save tasks to a file."""
        with open(TASKS_FILE, "w") as file:
            json.dump({
                "running_tasks": self.running_tasks,
                "completed_tasks": self.completed_tasks
            }, file, indent=4)


    def load_tasks(self):
        """Load the running tasks from a file."""
        try:
            with open(TASKS_FILE, "r") as f:
                data = json.load(f)
                self.running_tasks = data.get("running_tasks", {})
                self.completed_tasks = data.get("completed_tasks", {})
        except FileNotFoundError:
            self.running_tasks = {}
            self.completed_tasks = {}

    def show_tasks(self):
        """Show all tasks."""
        click.echo("Running tasks:")
        for task_name, start_time in self.running_tasks.items():
            click.echo(f"{task_name}: {time.time() - start_time:.2f} seconds")
        click.echo("\nCompleted tasks:")
        for task_name, elapsed_time in self.completed_tasks.items():
            click.echo(f"{task_name}: {elapsed_time:.2f} seconds")
    
    def export_tasks_csv(self, file_directory):
        """Export tasks to a CSV file."""
        with open(file_directory + "/tasks.csv", "w") as file:
            file.write("Task Name,Elapsed Time\n")
            for task_name, elapsed_time in self.completed_tasks.items():
                file.write(f"{task_name},{elapsed_time}\n")
    
    


# Create a global instance of TaskTimer
timer = TaskTimer()

@click.group()
def cli():
    """Task Timer CLI"""
    pass


@click.command()
@click.argument("task_name")
def start(task_name):
    """Start a new task."""
    timer.start_task(task_name)

@click.command()
@click.argument("task_name")
def stop(task_name):
    """Stop a running task."""
    timer.stop_task(task_name)

@click.command()
def show():
    """Show all tasks."""
    timer.show_tasks()

@click.command()
@click.argument("file_directory", required=False, default="./")
def export(file_directory):
    """Export tasks to a file."""
    timer.export_tasks_csv(file_directory)
    click.echo("Tasks exported to 'tasks.csv'.")

cli.add_command(start)
cli.add_command(stop)
cli.add_command(show)
cli.add_command(export)

if __name__ == "__main__":
    cli()        