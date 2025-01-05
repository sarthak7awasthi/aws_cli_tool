import typer
from ec2 import ec2_app
from sqs import sqs_app
from logs import logs_app




app = typer.Typer(help="AWS CLI Tool")
app.add_typer(ec2_app, name="ec2")
app.add_typer(sqs_app, name="sqs")
app.add_typer(logs_app, name="logs")

if __name__ == "__main__":
    app()






