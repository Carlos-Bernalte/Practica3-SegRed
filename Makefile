SHELL := /bin/bash
all: requirements certificates add-domain run 
requirements:
	@echo "Installing dependencies..."
	.venv/bin/python -m pip install --upgrade pip
	@.venv/bin/pip install -r requirements.txt
	@echo "Dependencies installed."

certificates:
	@echo "Creating certificates..."
	-mkdir cert
	-openssl req -x509 --nodes --days 365 --newkey rsa:2048 --keyout cert/myserver.local.key --out cert/myserver.local.crt -subj "/C=ES/ST=CiudadReal/L=CiudadReal/O=Dis/CN=myserver.local"
	-sudo cp cert/ssl.cert /usr/local/share/ca-certificates/myserver.local.crt
	-sudo update-ca-certificates --fresh
	@echo "Certificates created."

add-domain:
	@echo "Adding domain to hosts file..."
	@sudo sh -c "echo '127.0.0.1 myserver.local' >> /etc/hosts" 
	@echo "Domain added."

test:
	@echo "Running tests..."
	@.venv/bin/python test.py

run:
	@echo "Running server..."
	@.venv/bin/python -m src.run

clean:
	@rm -rf src/storage
	@rm src/shadow.json
	@echo "Almacenamiento limpiado."