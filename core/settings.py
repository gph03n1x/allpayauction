from decouple import config

RESULTS_DIRECTORY = config("RESULTS_DIRECTORY", default="results")
IMAGES_DIRECTORY = config("IMAGES_DIRECTORY", default="images")
