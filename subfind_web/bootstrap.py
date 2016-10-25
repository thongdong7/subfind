from tb_ioc import IOC

container = IOC()
container.load_resource('@subfind_web')

# subfind = container.get('SubFinder')
# print(subfind)
