from build_pc import build_pc, BuildType, GpuBrand, CpuBrand, StorageType, get_benchmark_text

pcs = []
def builder(price, percentages, build_type = BuildType.Gaming.name, gpu_brand = [GpuBrand.Nvidia.name, GpuBrand.AMD.name], cpu_brand = [CpuBrand.Intel.name, CpuBrand.AMD.name], storage_type = StorageType.Both.name):
    # quick hacky fix for $in in mongodb "Nvidia" to ["Nvidia"]
    if not isinstance(gpu_brand, list): 
        gpu_brand = [gpu_brand]
    if not isinstance(cpu_brand, list): 
        cpu_brand = [cpu_brand]
    
    # pc desired by user spesifications
    pcs.append(build_pc(price, percentages, "Desired", build_type, gpu_brand, cpu_brand, storage_type))

    # if user changed any default setting, we also show our algorithms default version, so user can decide which to choose
    if gpu_brand != [GpuBrand.Nvidia.name, GpuBrand.AMD.name] or cpu_brand != [CpuBrand.Intel.name, CpuBrand.AMD.name] or storage_type != StorageType.Both.name:
        pc = build_pc(price, percentages, "Recommended By Algorithm", build_type, [GpuBrand.Nvidia.name, GpuBrand.AMD.name], [CpuBrand.Intel.name, CpuBrand.AMD.name], StorageType.Both.name)
        if pc["GPU"] != pcs[0]["GPU"] or pc["CPU"] != pcs[0]["GPU"] or storage_type != StorageType.Both.name:
            pcs.append(pc)
    
    # if algorithm finds a system that doesn't change performance significantly and its price is 10% lower than expected,
    #  we also show that system, so user can decide whether or not to go for lower price one
    pc = build_pc(price * 0.9, percentages, "A bit cheaper but almost same performance version", build_type, gpu_brand, cpu_brand, storage_type)
    if(pc["GPU"][get_benchmark_text(build_type)] >= pcs[0]["GPU"][get_benchmark_text(build_type)]*0.9) \
        or (pc["CPU"][get_benchmark_text(build_type)] >= pcs[0]["CPU"][get_benchmark_text(build_type)]*0.9):
            pcs.append(pc)

    # if algorithm finds a system that change performance significantly and its price is 10% higher than expected, we also show that system,
    # so user can decide whether or not to higher price
    pc = build_pc(price * 1.1, percentages, "A bit more expensive but more performent version", build_type, gpu_brand, cpu_brand, storage_type)
    if(pc["GPU"][get_benchmark_text(build_type)] >= pcs[0]["GPU"][get_benchmark_text(build_type)]*1.1) \
        or (pc["CPU"][get_benchmark_text(build_type)] >= pcs[0]["CPU"][get_benchmark_text(build_type)]*1.1):
            pcs.append(pc)
    
    for pc in pcs:
        print(pc)
    
    return pcs

builder(1000, None)
