generate:  # make generate NAME=Test
	alembic revision --m="$(NAME)" --autogenerate

migrate:  # make migrate
	alembic upgrade head
