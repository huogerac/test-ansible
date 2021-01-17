
## DOCKER
# Links
https://docs.docker.com/develop/develop-images/multistage-build/

# BUILD

pylint pontos/**/*.py

docker build --target production -t fi/backend:latest .


# DEPLOY
ansible-playbook -i hosts/production --tags backend playbook.yml
