from subprocess import run

from dotenv import load_dotenv

from comlink import Comlink

# Initialize docker comlink with secrets
if __name__ == '__main__':
    load_dotenv()
    run(["./comlink-start.sh"])
    comlink = Comlink()
    run(["./comlink-stop.sh"])
