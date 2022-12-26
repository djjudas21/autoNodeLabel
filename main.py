def mapVendor(vendor):
    if vendor == 'GenuineIntel':
        returnval = 'Intel'
    elif vendor == 'AuthenticAMD':
        returnval = 'AMD'
    else:
        returnval = vendor
    return returnval

def cleanBrand(brand):
    # Strip annoying chars
    brand = brand.replace('(R)', '')
    brand = brand.replace('(TM)', '')
    brand = brand.replace('CPU', '')

    # Drop the '@ 2.40GHz' suffix
    brand = brand.split('@')[0]

    # Drop the 'with Radeon Graphics' suffix
    brand = brand.split('with')[0]
    brand = brand.strip()

    return brand

def parseCPU(vendor, cpu):
    import re

    cpuannotations = {}
    if vendor == 'Intel':
        # Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz
        # Intel(R) Core(TM) i5-6500T CPU @ 2.50GHz
        # Intel(R) Core(TM) i5-4590T CPU @ 2.00GHz
        result = re.search(r"(i\d)-(\d)?\d{3}([A-Z])?", cpu)
        cpuannotations['cpumodel'] = result.group(0)
        cpuannotations['cpufamily'] = result.group(1)
        cpuannotations['cpugeneration'] = result.group(2)
        cpuannotations['cpuletter'] = result.group(3)
    elif vendor == 'AMD':
        pass
        # AMD Ryzen 7 5700G with Radeon Graphics
        result = re.search(r"AMD ((\w+ \d) (\d)\d+([A-Z]?))", cpu)
        cpuannotations['cpumodel'] = result.group(1)
        cpuannotations['cpufamily'] = result.group(2)
        cpuannotations['cpugeneration'] = result.group(3)
        cpuannotations['cpuletter'] = result.group(4)
    return cpuannotations

if __name__ == '__main__':
    from cpuinfo import get_cpu_info

    cpuinfo = get_cpu_info()

    annotations = {}
    annotations['vendor'] = mapVendor(cpuinfo['vendor_id_raw'])
    annotations['cpu'] = cleanBrand(cpuinfo['brand_raw'])
    annotations['speed'] = cpuinfo['hz_advertised_friendly']

    annotations.update(parseCPU(annotations['vendor'], annotations['cpu']))

    print(annotations)
