import gbdxtools
import time
import boto3

PROTOCOL = 'gbdx://'

class Task():
	def __init__(self, gbdx_interface, task_name, params):
		self.gbdx_interface = gbdx_interface
		params = self.unpack_param_urls(params)
		self.task = self.gbdx_interface.Task(task_name, **params)
		self.persist_all_outputs()

	def execute(self):
		self.wf = self.gbdx_interface.Workflow([self.task])
		self.wf.execute()
		self.wait_until_done()
		port_outputs = self.get_output_locations()
		return port_outputs

	def unpack_param_urls(self, params):
		newparams = {}
		for name, value in params.iteritems():
			if type(value) is RemoteFile:
				value = value.data2s3(value.location)

			newparams[name] = value

		return newparams

	def wait_until_done(self):
		while not self.wf.complete:
			print '.'
			time.sleep(20)

	def get_output_locations(self):
		# loop through output ports and get the auto-persist locations
		# for now just output the big dict of status
		info = self.gbdx_interface.workflow.get(self.wf.id)
		output_dict = {}
		for port in info['tasks'][0]['outputs']:
			if 'persistLocation' in port:
				output_dict[port['name']] = RemoteFile(self.gbdx_interface, "s3://gbd-customer-data/" + port['persistLocation'])

		return output_dict

	def persist_all_outputs(self):
		for portname in self.task.outputs._portnames:
			self.task.outputs.__getattribute__(portname).persist = True


class RemoteFile(object):
	def __init__(self, gbdx_interface, location):
		self.gbdx_interface = gbdx_interface
		self.location = location

	def putFile(self, local_path):
		# put the file in s3 with boto
		s3path = self.data2s3(self.location).strip('/')
		info = self.gbdx_interface.s3.info
		client = boto3.client(
			's3',
			aws_access_key_id=info['S3_access_key'],
			aws_secret_access_key=info['S3_secret_key'],
			aws_session_token=info['S3_session_token'],
		)
		bucket = s3path.split('/')[2]
		prefix = '/'.join( s3path.split('/')[3:] )
		with open(local_path, 'rb') as data:
			client.upload_fileobj(data, bucket, prefix)


	def getFile(self, local_path):
		# get the file from s3 with boto
		s3path = self.data2s3(self.location).strip('/')
		info = self.gbdx_interface.s3.info
		client = boto3.client(
			's3',
			aws_access_key_id=info['S3_access_key'],
			aws_secret_access_key=info['S3_secret_key'],
			aws_session_token=info['S3_session_token'],
		)
		bucket = s3path.split('/')[2]
		prefix = '/'.join( s3path.split('/')[3:] )
		with open(local_path, 'wb') as data:
			client.download_fileobj(bucket, prefix, data)

	def data2s3(self, data_url):
		# convert a url that looks like data://{{userdata}}/path/to/stuff to
		# s3://gbd_customer_data/<account_id>/path/to/stuff
		info = self.gbdx_interface.s3.info
		bucket = info['bucket']
		prefix = info['prefix']

		return data_url.replace(PROTOCOL,'s3://'+ bucket + '/' + prefix + '/')

	def s32data(self, s3_url):
		if PROTOCOL in s3_url:
			return s3_url
		bucket = s3_url.split('/')[2]
		account_id = s3_url.split('/')[3]
		data_url = s3_url.replace('s3://' + bucket + '/' + account_id + '/', PROTOCOL)
		return data_url

	@property
	def location(self):
		return self._location

	@location.setter
	def location(self, value):
		# convert to "data://" format upon GET
		self._location = self.s32data(value)

	def list(self):
		s3path = self.data2s3(self.location).strip('/')
		info = self.gbdx_interface.s3.info
		client = boto3.client(
			's3',
			aws_access_key_id=info['S3_access_key'],
			aws_secret_access_key=info['S3_secret_key'],
			aws_session_token=info['S3_session_token'],
		)
		bucket = s3path.split('/')[2]
		prefix = '/'.join( s3path.split('/')[3:] )
		response = client.list_objects_v2(
			Bucket=bucket,
			#Delimiter='/',
			EncodingType='url',
			MaxKeys=123,
			Prefix=prefix + '/',
		)
		if not 'Contents' in response: return []

		return [self.s32data('s3://' + bucket + '/' + k['Key']) for k in response['Contents']]

class lets_go_insane():

	def __init__(self):
		self.gbdx_interface = gbdxtools.Interface()

	def remote_file(self, location):
		return RemoteFile(self.gbdx_interface, location)

	def Task(self, task_name, params):
		return Task(self.gbdx_interface, task_name, params)

	

	

	


