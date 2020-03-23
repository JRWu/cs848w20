all:
	docker-compose up --build -d

magellan: force
	docker-compose exec cs848w20_magellan bash

# Force exec into shell for magellan
force:
	