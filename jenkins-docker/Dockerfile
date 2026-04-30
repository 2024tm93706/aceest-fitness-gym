FROM jenkins/jenkins:lts

USER root

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    docker.io \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

# Give Jenkins access to Docker socket
RUN usermod -aG docker jenkins

# 🔥 IMPORTANT: fix docker permissions
RUN chmod 666 /var/run/docker.sock || true

USER jenkins