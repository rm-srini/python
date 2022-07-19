import finance.config as config
import glob


print(config.file_path + '\\' + config.file_name)
print(glob.glob(config.file_path + '/' + config.file_name))