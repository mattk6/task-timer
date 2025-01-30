import click
import csv
 
@click.command()
def main():
    """This is my main cli."""
 
    click.echo("Hello World")
     
if __name__ == '__main__':
    main()