from subprocess import call, Popen, PIPE

def get_partition_info():
	"""get a list of all partitions on the device"""

	output = Popen(["adb", "shell", "cat /proc/dumchar_info"], stdout=PIPE).communicate()[0].split('\n')
	partitions = output[1:len(output) - 6]
	partition_dict = {}
	for each_partition in partitions:
		each_partition = each_partition.split()
		partition_dict[each_partition[0]] = {'size': each_partition[1],
		'start_address': each_partition[2],
		'type': each_partition[3],
		'block_file': each_partition[4]}
	return partition_dict


def extract_image_from_device(partition_name):
	"""extract the image of a partition into the current directory"""

	info = get_partition_info()

	call(["adb", "shell", "su -c 'dd if=%s of=/sdcard/%s.img skip=%d count=%d bs=1'" % (
		info[partition_name]['block_file'],
		partition_name,
		int(info[partition_name]['start_address'], 0),
		int(info[partition_name]['size'], 0))])

	call(["adb", "pull", "/sdcard/%s.img" % (partition_name)])
	call(["adb", "shell", "rm /sdcard/%s.img" % (partition_name)])

