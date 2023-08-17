FROM jupyter/scipy-notebook:python-3.11

USER 1000

ENV CPATH=$CONDA_DIR/include TZ=Asia/Bangkok

## Install JupyterLab and language server
RUN pip install --no-cache-dir -U pip jupyterhub jupyterlab-lsp "python-lsp-server[all]"
