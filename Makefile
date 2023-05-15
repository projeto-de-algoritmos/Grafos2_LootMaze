install:
	python -m pip install -r requirements.txt

run: 
	python -m src.game.main --map_file=<path_to_map_file>