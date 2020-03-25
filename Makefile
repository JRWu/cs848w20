all:
	docker-compose up --build -d

magellan: force
	docker-compose exec cs848w20_magellan bash

jedai: force
	docker-compose exec cs848w20_jedai sh

pydedupe: force
	docker-compose exec cs848w20_pydedupe bash

dedupe: force
	docker-compose exec cs848w20_dedupe bash

# Force exec into shell for magellan
force:
	