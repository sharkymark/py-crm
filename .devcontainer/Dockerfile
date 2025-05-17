FROM python:3.13-slim

RUN DEBIAN_FRONTEND="noninteractive" apt-get update -y && \
    apt-get install -y \
    curl \
    netcat-traditional \
    git \
    ssh \
    net-tools \
    htop \
    jq \
    procps \
    build-essential \
    wget \
    sudo

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Install GitHub CLI
RUN ARCH=$(dpkg --print-architecture) && \
    GH_VERSION=$(curl -s https://api.github.com/repos/cli/cli/releases/latest | grep tag_name | cut -d '"' -f 4 | cut -c 2-) && \
    curl -sSL "https://github.com/cli/cli/releases/latest/download/gh_${GH_VERSION}_linux_${ARCH}.deb" -o gh.deb && \
    dpkg -i gh.deb && \
    rm gh.deb

# Create a non-root user for VS Code
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
USER $USERNAME

ENV HOME=/home/$USERNAME
WORKDIR $HOME

# Install Goose CLI (non-interactive)
RUN curl -fsSL https://github.com/block/goose/releases/download/stable/download_cli.sh | CONFIGURE=false bash

# Install Aider
RUN curl -LsSf https://aider.chat/install.sh | sh