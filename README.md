# dvc-s3-repo
[![Deploy deb/rpm to s3 repo](https://github.com/treeverse/dvc-s3-repo/actions/workflows/deploy.yaml/badge.svg)](https://github.com/treeverse/dvc-s3-repo/actions/workflows/deploy.yaml)

Maintain deb and rpm repositories on s3

## Ubuntu, Debian
Install dvc from dep repository:
```bash
sudo apt install wget gpg
sudo mkdir -p /etc/apt/keyrings
wget -qO - https://dvc.org/deb/iterative.asc | sudo gpg --dearmor -o /etc/apt/keyrings/packages.iterative.gpg
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.iterative.gpg] https://dvc.org/deb/ stable main" | sudo tee /etc/apt/sources.list.d/dvc.list
sudo chmod 644 /etc/apt/keyrings/packages.iterative.gpg /etc/apt/sources.list.d/dvc.list
sudo apt update
sudo apt install dvc
```

## Fedora, Centos, RHEL
Install dvc from rpm repository:
```bash
sudo wget \
       https://dvc.org/rpm/dvc.repo \
       -O /etc/yum.repos.d/dvc.repo
sudo rpm --import https://dvc.org/rpm/iterative.asc
sudo yum update
sudo yum install dvc
```
