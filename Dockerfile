FROM python:3

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY Makefile .
COPY requirements.txt .
COPY xtdb_chat xtdb_chat

RUN make install

ENV PYTHONPATH="xtdb_chat"
ENTRYPOINT ["sleep", "infinity"]
