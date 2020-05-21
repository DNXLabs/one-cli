from docker import Client


base_url = 'unix://var/run/docker.sock'
client = Client(base_url=base_url)
