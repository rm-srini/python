# Import Library
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from Google import Create_serv

class AccessDrive:
	def __init__(self):
		self.g_auth = GoogleAuth()
		self.drive = GoogleDrive(self.g_auth)


	def upload_file(self, filename, replace_file=True, trg_folder_id='1-LKhI8-on-BFBLsdYzdxzxmSAGigQl3i'):
		g_file = self.drive.CreateFile({'parents': [{'id': trg_folder_id}]})
		g_file.SetContentFile(filename)
		g_file.Upload()
		os.remove(filename)

	def get_file_list(self, trg_folder_id='1-LKhI8-on-BFBLsdYzdxzxmSAGigQl3i'):
		file_list = self.drive.ListFile(
			{'q': "'{}' in parents and trashed=false".format(trg_folder_id)}).GetList()
		return file_list

	def check_files_exists(self, file_name):
		file_list = self.get_file_list()
		for file in file_list:
			if file_name == file['title']:
				return True
		return False

	def download_file(self, file_list):
		for i, file in enumerate(sorted(file_list, key=lambda x: x['title']), start=1):
			print('Downloading {} file from GDrive ({}/{})'.format(file['title'], i, len(file_list)))
			file.GetContentFile(file['title'])

a = AccessDrive()
a.upload_file(r"test.txt")
file_list = a.get_file_list()
a.download_file(file_list)
