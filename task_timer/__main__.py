import time
import click

class TaskTimer:
    def __init__(self):
        self.running_tasks = {}  # Store running tasks with start times

    def start_task(self, task_name):
        """Start a new task."""
        if task_name in self.running_tasks:
            click.echo(f"Task '{task_name}' is already running.")
            return
        self.running_tasks[task_name] = time.time()  # Store the start time
        click.echo(f"Started task: {task_name}")

    def stop_task(self, task_name):
        """Stop a running task."""
        if task_name in self.running_tasks:
            elapsed_time = time.time() - self.running_tasks.pop(task_name)
            click.echo(f"Stopped task: {task_name}. Time logged: {elapsed_time:.2f} seconds.")
        else:
            click.echo(f"Task '{task_name}' is not currently running.")


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

cli.add_command(start)
cli.add_command(stop)

if __name__ == "__main__":
    cli()        