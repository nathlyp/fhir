.PHONY: run json

run:
#	python final/admissions.py
	python final/patient.py

json:
	python final/patient.py > 01-patient.fhir.json
	python final/admissions.py > 02-encounter.fhir.json
	python final/procedures.py > 03-procedure.fhir.json
	python final/service_request.py > 04-ServiceRequest.fhir.json

hapi:
	docker-compose up

clean:
	docker-compose down

#	docker run -p 8080:8080 hapiproject/hapi:latest
