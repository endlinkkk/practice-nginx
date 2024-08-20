local-start: `uvicorn --factory main.app.application.api.main:create_app --reload`
docker-start: `docker-compose up -d`
