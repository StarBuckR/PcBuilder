from build_pc import build_pc, BuildType, GpuBrand, CpuBrand, StorageType, get_benchmark_text
from percentage import Percentage

def builder(price, percentages, build_type = BuildType.Gaming.value, gpu_brand = GpuBrand.Both.value, cpu_brand = CpuBrand.Both.value, storage_type = StorageType.Both.value):
    pcs = []
    # pc desired by user specifications
    pcs.append(build_pc(price, percentages, "Desired", build_type, gpu_brand, cpu_brand, storage_type))

    # if user changed any default setting, we also show our algorithms default version, so user can decide which to choose
    if gpu_brand != GpuBrand.Both.value or cpu_brand != CpuBrand.Both.value or storage_type != StorageType.Both.value:
        pc = build_pc(price, percentages, "Recommended By Algorithm", build_type, GpuBrand.Both.value, CpuBrand.Both.value, StorageType.Both.value)
        if pc["GPU"] != pcs[0]["GPU"] or pc["CPU"] != pcs[0]["CPU"] or storage_type != StorageType.Both.value:
            pcs.append(pc)
    
    # if algorithm finds a system that doesn't change performance significantly and its price is 10% lower than expected,
    #  we also show that system, so user can decide whether or not to go for lower price one
    pc = build_pc(price * 0.9, percentages, "A bit cheaper but almost same performance version", build_type, gpu_brand, cpu_brand, storage_type)
    if (pc["GPU"] != pcs[0]["GPU"] and pc["CPU"] != pcs[0]["CPU"]) \
        and (pc["GPU"][get_benchmark_text(build_type)] >= pcs[0]["GPU"][get_benchmark_text(build_type)]*0.9 \
        and pc["CPU"][get_benchmark_text(build_type)] >= pcs[0]["CPU"][get_benchmark_text(build_type)]*0.9):
            pcs.append(pc)

    # if algorithm finds a system that change performance significantly and its price is 10% higher than expected, we also show that system,
    # so user can decide whether or not to higher price
    pc = build_pc(price * 1.1, percentages, "A bit more expensive but more performent version", build_type, gpu_brand, cpu_brand, storage_type)
    if (pc["GPU"] != pcs[0]["GPU"] and pc["CPU"] != pcs[0]["CPU"])\
        and (pc["GPU"][get_benchmark_text(build_type)] >= pcs[0]["GPU"][get_benchmark_text(build_type)]*1.1 \
        and pc["CPU"][get_benchmark_text(build_type)] >= pcs[0]["CPU"][get_benchmark_text(build_type)]*1.1):
            pcs.append(pc)
    
    return pcs

#builder(1000, None)
