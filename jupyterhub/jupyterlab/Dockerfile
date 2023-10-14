FROM jupyter/scipy-notebook:python-3.11

USER root

# Install all OS dependencies for Server that starts but lacks all
# features (e.g., download as all possible file formats)
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    tmux \ 
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN usermod -aG sudo jovyan && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER 1000

ENV CPATH=$CONDA_DIR/include TZ=Asia/Bangkok

COPY requirements.txt .
## Install JupyterLab and language server
RUN pip install --no-cache-dir -U pip jupyterhub jupyterlab-lsp "python-lsp-server[all]" \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -f requirements.txt
