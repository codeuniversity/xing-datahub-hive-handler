dep:
	pip install -r requirements.txt

test:
	python model_test.py

integration:
	./integration.sh
