def mapVendor(vendor):
    """
    Rewrite vendor name
    """
    if vendor == 'GenuineIntel':
        returnval = 'Intel'
    elif vendor == 'AuthenticAMD':
        returnval = 'AMD'
    else:
        returnval = vendor
    return returnval

def cleanCpuString(brand):
    """
    Rewrite CPU string more neatly.
    
    This:
        Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz
    Becomes:
        Intel Core i5-6300U
    """
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
    """
    Parse the CPU string to figure out some attributes
    """
    import re

    cpulabels = {}
    if vendor == 'Intel':
        # Intel(R) Core(TM) i5-6300U CPU @ 2.40GHz
        # Intel(R) Core(TM) i5-6500T CPU @ 2.50GHz
        # Intel(R) Core(TM) i5-4590T CPU @ 2.00GHz
        result = re.search(r"(i\d)-(\d)?\d{3}([A-Z])?", cpu)
        cpulabels['cpuModel'] = result.group(0)
        cpulabels['cpuFamily'] = result.group(1)
        cpulabels['cpuGeneration'] = result.group(2)
        cpulabels['cpuLetter'] = result.group(3)
    elif vendor == 'AMD':
        pass
        # AMD Ryzen 7 5700G with Radeon Graphics
        result = re.search(r"AMD ((\w+ \d) (\d)\d+([A-Z]?))", cpu)
        cpulabels['cpuModel'] = result.group(1)
        cpulabels['cpuFamily'] = result.group(2)
        cpulabels['cpuGeneration'] = result.group(3)
        cpulabels['cpuLetter'] = result.group(4)
    return cpulabels


def drop_nones_inplace(d: dict) -> dict:
    """Recursively drop Nones in dict d in-place and return original dict"""
    dd = drop_nones(d)
    d.clear()
    d.update(dd)
    return d


def drop_nones(d: dict) -> dict:
    """Recursively drop Nones in dict d and return a new dict"""
    dd = {}
    for k, v in d.items():
        if isinstance(v, dict):
            dd[k] = drop_nones(v)
        elif isinstance(v, (list, set, tuple)):
            # note: Nones in lists are not dropped
            # simply add "if vv is not None" at the end if required
            dd[k] = type(v)(drop_nones(vv) if isinstance(vv, dict) else vv
                            for vv in v)
        elif v is not None:
            dd[k] = v
    return dd


if __name__ == '__main__':
    from cpuinfo import get_cpu_info

    cpuinfo = get_cpu_info()

    labels = {}
    labels['cpuVendor'] = mapVendor(cpuinfo['vendor_id_raw'])
    labels['cpuString'] = cleanCpuString(cpuinfo['brand_raw'])

    labels.update(parseCPU(labels['cpuVendor'], labels['cpuString']))

    # Drop None elements
    labels = (drop_nones_inplace(labels))

    # Generate fully qualified labels
    prefix = 'autolabels.example.com'
    for key, value in labels.items():
        print(f"{prefix}/{key}: {value}")
