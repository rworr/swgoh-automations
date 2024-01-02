from dotenv import load_dotenv
from subprocess import run

# Initialize docker comlink with secrets
if __name__ == '__main__':
    load_dotenv()
    run(["./comlink-start.sh"])
    run(["./comlink-stop.sh"])
