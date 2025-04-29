FROM ubuntu:latest

COPY agent.py .

RUN apt update && apt install -y python3 python3-pip
RUN pip install --break-system-packages requests uagents

ENTRYPOINT ["python3", "agent.py"]
