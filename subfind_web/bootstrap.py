from tb_ioc import IOC

container = IOC()
container.load_resource('@subfind_web')
container.load_resource('@subfind_web/conf/api.yml')

# subfind = container.get('SubFinder')
# print(subfind)
