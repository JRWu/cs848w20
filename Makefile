all:
	docker-compose up --build -d

shell:
	docker-compose exec cs848w20 bash

database:
	docker-compose exec cs848w20_postgres bash
