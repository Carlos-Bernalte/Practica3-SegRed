SHELL := /bin/bash

install: venv requirements cert add-domain

venv:
	@echo "Creating virtual environment..."
	@python3 -m venv .venv
	@echo "Virtual environment created."
	

requirements:
	@echo "Installing dependencies..."
	.venv/bin/python -m pip install --upgrade pip
	@.venv/bin/pip install -r requirements.txt
	@echo "Dependencies installed."

cert:
	@echo "Creating certificates..."
	-mkdir cert
	-openssl req -x509 --newkey rsa:4096 --out cert/cert.pem --keyout cert/key.pem --days 365
	-sudo cp cert/cert.pem /usr/local/share/ca-certificates/cert.crt
	-sudo update-ca-certificates
	@echo "Certificates created."
env:
	@echo "Creating .env file..."
	@echo "SECRET_KEY='secret'" > .env

add-domain:
	@echo "Adding domain to hosts file..."
	@sudo sh -c "echo '127.0.0.1 myserver.local' >> /etc/hosts" 
	@echo "Domain added."

test:
	@echo "Running tests..."
	@.venv/bin/python test_db.py

run:
	@echo "Running server..."
	@.venv/bin/python -m src.run

clean:
	@rm -rf storage
	@echo "Almacenamiento limpiado."