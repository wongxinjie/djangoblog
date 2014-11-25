#-*- coding: utf-8 -*-
from os import environ
from django.conf import settings

debug = not environ.get("APP_NAME", "")

from django.utils.translation import ugettext as _
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
import time, os, uuid, random, unicodedata, StringIO
from django.core.files.base import ContentFile


if not debug:
	import sae
	import tempfile
	import sae.storage
	from PIL import Image  #Very import, this is how SAE load picture
else:
	import Image

class SaeAndNotSaeStorage(FileSystemStorage):
	"""
	this is a base class to storage the location and url for file
	"""
	def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
		super(SaeAndNotSaeStorage, self).__init__(location, base_url)

	def get_valid_name(self, name):
		if not debug:
			try:
				if True:
					name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
				else:
					for n in name:
						if self.is_chinese(n):
							name = "picture%s"%random.randint(0, 100)
			except Exception, e:
				name = "%s.jpg"%type(name)
		return super(SaeAndNotSaeStorage, self).get_valid_name(name)

	@property
	def maxsize(self):
		return 10*1024*1024

	@property
	def filetype(self):
		return []

	def makename(self, name):
		oldname = os.path.basename(name)
		path = os.path.dirname(name)
		if oldname.find("_mine_")==0:
			oldname = oldname.replace("_mine_", "")
			name = os.path.join(path, oldname)
			return name
		try:
			fname, hk = oldname.split(".")
		except Exception, e:
			fname, hk = oldname, ''
		if hk:
			newname = "%s_%s.%s"%(random.randint(0, 10000), fname, hk)
		else:
			newname = "%s_%s"%(random.randint(0, 10000), fname)
		name = os.path.join(path, newname)
		return name

	def _save(self, name, content):
		suffix = name.split(".")[-1]
		if self.filetypes !="*":
			if suffix.lower() not in self.filetypes:
				raise SuspiciousOperation("File not to be supproted, suports %s"% self.filetypes)

		name = self.makename(name)

		if content.size > self.maxsize:
			raise SuspiciousOperation("File to large!")
		if not debug:
			s = sae.storage.Client()
			if hasattr(content, '_get_file'):#admin enterence
				ob = sae.storage.Object(content._get_file().read())
			else:#view enterance, contetFile
				ob = sae.storage.Object(content, read())
			url = s.put('wongxinjie', name, ob)
			return name
		else:
			return super(SaeAndNotSaeStorage, self)._save(name, content)
	
	
	def delete(self, name):
		if not debug:
			s = sae.storage.Client()
			try:
				s.delete('wongxinjie', name)
			except Exception, e:
				pass
		else:
			super(SaeAndNotSaeStorage, self).delete(name)




class ImageStorage(SaeAndNotSaeStorage):
	
	@property
	def maxsize(self):
		return 10*1024*1024

	@property
	def filetypes(self):
		return ['jpg', 'jpeg', 'png', 'gif']


class FileStorage(SaeAndNotSaeStorage):

	@property
	def maxsize(self):
		return 10*1024*1024

	@property
	def filetypes(self):
		return "*"


class ThumbStorage(ImageStorage):
	
	def _save(self, name, content):
		image = Image.open(content)
		image = Image.convert('RGB')
		image.thumbnail((50, 50), Image.ANTIALIAS)
	
		output = StringIO.StringIO()
		image.save(output, 'JPEG')
		contentf = ContentFile(output.getvalue())
		output.close()

		return super(ThumbStorage, self)._save(name, contentf)



		
		
		
		

		



















