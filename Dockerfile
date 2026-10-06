FROM rclone/rclone:1.71 AS rclone

# Install necessary compile toolchains
RUN apt-get update && \
    apt-get -y install git gcc g++ && \
    apt-get -y install openssh-server smbclient cifs-utils && \
    rm -rf /var/lib/apt/lists/*

COPY --from=rclone /usr/local/bin/rclone /usr/local/bin/rclone

RUN cd /home && \
    git clone https://github.com/Tabor-Research-Group/hpclib.git

# Set the default shell to use bash and activate the conda environment
ENTRYPOINT ["smbclient"]
