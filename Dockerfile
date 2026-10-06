FROM rclone/rclone:1.71 AS rclone

FROM debian:bookworm-slim
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
      ca-certificates smbclient cifs-utils krb5-user openssh-client && \
    rm -rf /var/lib/apt/lists/*
COPY --from=rclone /usr/local/bin/rclone /usr/local/bin/rclone
ENTRYPOINT ["smbclient"]
