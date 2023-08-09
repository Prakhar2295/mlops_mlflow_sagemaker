import yaml

def read_config(config_path):
	with open(config_path,'r') as config_file:
		content = yaml.safe_load(config_file)
	return content

