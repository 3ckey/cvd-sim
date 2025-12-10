FROM python:3.14-slim

# rootでパッケージインストール等必要ならここで行う

# 非rootユーザー作成
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

# グループ&ユーザー作成
RUN if getent group "${USER_GID}" > /dev/null 2>&1; then \
        echo "Group with GID ${USER_GID} already exists. Skipping groupadd."; \
    else \
        groupadd --gid "${USER_GID}" "${USERNAME}"; \
    fi \
    && useradd --uid "${USER_UID}" --gid "${USER_GID}" -m "${USERNAME}" -s /bin/bash

# ワークスペース用ディレクトリ
WORKDIR /workspaces/cvd-sim

# 以降は非rootユーザーで実行
USER ${USERNAME}
