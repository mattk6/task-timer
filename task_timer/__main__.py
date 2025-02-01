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
        """Start a new task. Enter task name as one word """
        if task_name in self.running_tasks:
            click.echo(f"Task '{task_name}' is already running.")
            return
        self.running_tasks[task_name] = time.time()  # Store the start time
        click.echo(f"Started task: {task_name}")
        self.save_tasks()

    def stop_task(self, task_name):
        """Stop a running task. Enter name of already running task """
        if task_name in self.running_tasks:
            elapsed_time = time.time() - self.running_tasks.pop(task_name)
            click.echo(f"Stopped task: {task_name}. Time logged: {elapsed_time:.2f} seconds.")
            self.completed_tasks[task_name] = self.running_tasks.get(task_name, 0) + elapsed_time
            self.save_tasks()
        else:
            click.echo(f"Task '{task_name}' is not currently running.")

    def save_tasks(self):
        """Save tasks to a file. """
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
    
    def delete_task(self, task_name):
        """Delete a task."""
        found = False
        if task_name in self.running_tasks:
            found = True
            self.running_tasks.pop(task_name)
            click.echo(f"Task '{task_name}' deleted.")
        if task_name in self.completed_tasks:
            found = True
            self.completed_tasks.pop(task_name)
            click.echo(f"Task '{task_name}' deleted.")
        if not found:
            click.echo(f"Task '{task_name}' not found.")
        self.save_tasks()
    
    def rename_task(self, old_task_name, new_task_name):
        """Rename a task."""
        
        found = False
        
        if new_task_name in self.running_tasks or new_task_name in self.completed_tasks:
            click.echo(f"Task '{new_task_name}' already exists.")
            return
        
        if old_task_name in self.running_tasks:
            found = True
            self.running_tasks[new_task_name] = self.running_tasks.pop(old_task_name)
            click.echo(f"Task '{old_task_name}' renamed to '{new_task_name}'.")
        if old_task_name in self.completed_tasks:
            found = True
            self.completed_tasks[new_task_name] = self.completed_tasks.pop(old_task_name)
            click.echo(f"Task '{old_task_name}' renamed to '{new_task_name}'.")
        if not found:
            click.echo(f"Task '{old_task_name}' not found.")
        self.save_tasks()
    


# Create a global instance of TaskTimer
timer = TaskTimer()

@click.group(help="Task Timer CLI Tool")
def cli():
    """Task Timer CLI"""
    pass

@click.command(help="Start a new task. Enter task name as one word.")
@click.argument("task_name", required=True)
def start(task_name):
    """Start a new task."""
    timer.start_task(task_name)

@click.command(help="Stop a running task. Enter name of already running task.")
@click.argument("task_name", required=True)
def stop(task_name):
    """Stop a running task."""
    timer.stop_task(task_name)

@click.command(help="Show all tasks.")
def show():
    """Show all tasks."""
    timer.show_tasks()

@click.command(help="Export tasks to a file. Enter optional file directory without trailing slash, default is current directory.")
@click.argument("file_directory", required=False, default="./")
def export(file_directory):
    """Export tasks to a file."""
    timer.export_tasks_csv(file_directory)
    click.echo("Tasks exported to 'tasks.csv'.")


@click.command(help="Delete a task. Enter name of task to delete.")
@click.argument("task_name", required=True)
def delete(task_name):
    """Delete a task."""
    timer.delete_task(task_name)
    
@click.command(help="Rename a task. Enter old task name and new task name.")
@click.argument("old_task_name", required=True)
@click.argument("new_task_name", required=True)
def rename(old_task_name, new_task_name):
    """Rename a task."""
    timer.rename_task(old_task_name, new_task_name)



cli.add_command(start)
cli.add_command(stop)
cli.add_command(show)
cli.add_command(export)
cli.add_command(delete)
cli.add_command(rename)

if __name__ == "__main__":
    cli()