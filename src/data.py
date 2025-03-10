import os
from pathlib import Path
from gears import PertData
from gears.utils import dataverse_download
import tarfile
import anndata
import numpy as np

def norman2019(seed, data_dir='data', suffix=''):
    d = f'{data_dir}/norman2019'
    file = f'{d}/norman2019_{seed}.h5ad'
    Path(d).mkdir(parents=True, exist_ok=True)

    # Create split and save data (when GEARS restores saved splits,
    # these are not stored in pert_adata.adata.obs['split'])
    pert_data = PertData(f'{d}{suffix}')
    pert_data.load(data_name='norman', data_path='norman2019')
    pert_data.prepare_split(split='simulation', seed=seed)
    if not os.path.exists(file):
        pert_data.adata.write_h5ad(file)
    else:
        pert_data.adata = anndata.read_h5ad(file)  # Manually setting the data to ensure same split
    return pert_data

def adamson2016(seed, data_dir='data', suffix=''):
    d = f'{data_dir}/adamson2016'
    file = f'{d}/adamson2016_{seed}.h5ad'
    Path(d).mkdir(parents=True, exist_ok=True)

    # Create split and save data (when GEARS restores saved splits,
    # these are not stored in pert_adata.adata.obs['split'])
    pert_data = PertData(f'{d}{suffix}')
    pert_data.load(data_name='adamson', data_path='adamson2016')
    pert_data.prepare_split(split='simulation', seed=seed)
    if not os.path.exists(file):
        pert_data.adata.write_h5ad(file)
    else:
        pert_data.adata = anndata.read_h5ad(file)  # Manually setting the data to ensure same split
    return pert_data

def dixit2016(seed, data_dir='data', suffix=''):
    d = f'{data_dir}/dixit2016'
    file = f'{d}/dixit2016_{seed}.h5ad'
    Path(d).mkdir(parents=True, exist_ok=True)

    # Create split and save data (when GEARS restores saved splits,
    # these are not stored in pert_adata.adata.obs['split'])
    pert_data = PertData(f'{d}{suffix}')
    pert_data.load(data_name='dixit', data_path='dixit2016')
    pert_data.prepare_split(split='simulation', seed=seed)
    if not os.path.exists(file):
        pert_data.adata.write_h5ad(file)
    else:
        pert_data.adata = anndata.read_h5ad(file)  # Manually setting the data to ensure same split
    return pert_data

def replogle_k562_2022(seed, data_dir='data', suffix='', discard_perts_not_in_var=True):
    d = f'{data_dir}/replogle_k562_2022'
    file = f'{d}/replogle_k562_2022_{seed}.h5ad'
    Path(d).mkdir(parents=True, exist_ok=True)

    # Create split and save data (when GEARS restores saved splits,
    # these are not stored in pert_adata.adata.obs['split'])
    pert_data = PertData(f'{d}{suffix}')
    data_name = 'replogle_k562_essential'
    data_path = 'replogle_k562_2022'
    if os.path.exists(file):  # Fixing scGPT compatibility issue
        data_path = f'{d}/{data_name}'
    pert_data.load(data_name=data_name, data_path=data_path)
    pert_data.prepare_split(split='simulation', seed=seed)
    if not os.path.exists(file):
        pert_data.adata.write_h5ad(file)
    else:
        pert_data.adata = anndata.read_h5ad(file)  # Manually setting the data to ensure same split

    # Discard cells of genetic perturbations not in gene panel
    if discard_perts_not_in_var:
        # TODO: Does GEARS processing leads to genetic perturbations not in gene panel?
        perturbations = pert_data.adata.obs['condition'].str.split('+').str[0].values
        unique_perts = set(perturbations).difference(set(['ctrl']))
        discard_perts = [p for p in unique_perts if p not in pert_data.adata.var['gene_name'].values]
        m = np.isin(perturbations, discard_perts)
        print('L', len(pert_data.adata))
        print(f'{100*sum(m) / len(m)}% of cells belong to perturbations not in gene panel... Warning: discarding them')
        pert_data.adata = pert_data.adata[~m]
        print('L', len(pert_data.adata))

    return pert_data

def replogle_k562_2022_v2(seed, data_dir='data'):
    d = f'{data_dir}/replogle_k562_v2_2022'
    file = f'{d}/replogle_k562_v2_2022_{seed}.h5ad'
    Path(d).mkdir(parents=True, exist_ok=True)
    # adata = anndata.read_h5ad(f'{d}/perturb_processed.h5ad')

    # Create split and save data (when GEARS restores saved splits,
    # these are not stored in pert_adata.adata.obs['split'])
    pert_data = PertData(f'{d}')
    # pert_data.new_data_process(dataset_name='replogle_k562_v2_2022', adata=adata, skip_calc_de = False)  # specific dataset name and adata object
    pert_data.load(data_name='replogle_k562_v2_2022', data_path=d)  # load the processed data, the path is saved folder + dataset_name
    pert_data.prepare_split(split='simulation', seed=seed)  # get data split with seed

    if not os.path.exists(file):
        pert_data.adata.write_h5ad(file)
    else:
        pert_data.adata = anndata.read_h5ad(file)

    return pert_data


def replogle_k562_2022_v2_scgptprocessing(seed, data_dir='data'):
    d = f'{data_dir}/replogle_k562_v3_2022'
    file = f'{d}/replogle_k562_v3_2022_{seed}.h5ad'
    Path(d).mkdir(parents=True, exist_ok=True)
    # adata = anndata.read_h5ad(f'{d}/perturb_processed.h5ad')

    # Create split and save data (when GEARS restores saved splits,
    # these are not stored in pert_adata.adata.obs['split'])
    data_name = 'K562_1900_100'
    data_path = f'{d}/{data_name}'
    pert_data = PertData(data_path)
    # pert_data.new_data_process(dataset_name='replogle_k562_v2_2022', adata=adata, skip_calc_de = False)  # specific dataset name and adata object
    pert_data.load(data_name=data_name, data_path=data_path)  # load the processed data, the path is saved folder + dataset_name
    pert_data.prepare_split(split='simulation', seed=seed)  # get data split with seed

    if not os.path.exists(file):
        pert_data.adata.write_h5ad(file)
    else:
        pert_data.adata = anndata.read_h5ad(file)

    return pert_data

def replogle_k562_2022_v3(seed, data_dir='data'):
    d = f'{data_dir}/replogle_k562_v3_2022'
    file = f'{d}/replogle_k562_v3_2022_{seed}.h5ad'
    Path(d).mkdir(parents=True, exist_ok=True)
    # adata = anndata.read_h5ad(f'{d}/perturb_processed.h5ad')

    # Create split and save data (when GEARS restores saved splits,
    # these are not stored in pert_adata.adata.obs['split'])
    data_name = 'k562'
    data_path = f'{d}/{data_name}'
    pert_data = PertData(data_path)
    # pert_data.new_data_process(dataset_name='replogle_k562_v2_2022', adata=adata, skip_calc_de = False)  # specific dataset name and adata object
    pert_data.load(data_name=data_name, data_path=data_path)  # load the processed data, the path is saved folder + dataset_name
    pert_data.prepare_split(split='simulation', seed=seed)  # get data split with seed
    pert_data.dataset_name = ''

    if not os.path.exists(file):
        pert_data.adata.write_h5ad(file)
    else:
        pert_data.adata = anndata.read_h5ad(file)

    return pert_data

def replogle_rpe1_2022(seed, data_dir='data', suffix='', discard_perts_not_in_var=True):
    d = f'{data_dir}/replogle_rpe1_2022'
    file = f'{d}/replogle_rpe1_2022_{seed}.h5ad'
    Path(d).mkdir(parents=True, exist_ok=True)

    # Create split and save data (when GEARS restores saved splits,
    # these are not stored in pert_adata.adata.obs['split'])
    pert_data = PertData(f'{d}{suffix}')
    data_name = 'replogle_rpe1_essential'
    data_path = 'replogle_rpe1_2022'
    if os.path.exists(file):  # Fixing scGPT compatibility issue
        data_path = f'{d}/{data_name}'
    pert_data.load(data_name=data_name, data_path=data_path)
    pert_data.prepare_split(split='simulation', seed=seed)
    if not os.path.exists(file):
        pert_data.adata.write_h5ad(file)
    else:
        pert_data.adata = anndata.read_h5ad(file)  # Manually setting the data to ensure same split

    # Discard cells of genetic perturbations not in gene panel
    if discard_perts_not_in_var:
        # TODO: Does GEARS processing lead to genetic perturbations not in gene panel?
        perturbations = pert_data.adata.obs['condition'].str.split('+').str[0].values
        unique_perts = set(perturbations).difference(set(['ctrl']))
        discard_perts = [p for p in unique_perts if p not in pert_data.adata.var['gene_name'].values]
        m = np.isin(perturbations, discard_perts)
        print(f'{100*sum(m) / len(m)}% of cells belong to perturbations not in gene panel... Warning: discarding them')
        pert_data.adata = pert_data.adata[~m]

    return pert_data

def joung2023(seed, data_dir='data'):
    d = f'{data_dir}/joung2023'
    file = f'{d}/joung2023_{seed}.h5ad'
    Path(d).mkdir(parents=True, exist_ok=True)
    # adata = anndata.read_h5ad(f'{d}/perturb_processed.h5ad')

    # Create split and save data (when GEARS restores saved splits,
    # these are not stored in pert_adata.adata.obs['split'])
    pert_data = PertData(f'{d}')
    # pert_data.new_data_process(dataset_name='joung', adata=adata)  # specific dataset name and adata object
    pert_data.load(data_name='joung', data_path=d)  # load the processed data, the path is saved folder + dataset_name
    pert_data.prepare_split(split='simulation', seed=seed)  # get data split with seed
    if not os.path.exists(file):
        pert_data.adata.write_h5ad(file)
    else:
        pert_data.adata = anndata.read_h5ad(file)

    return pert_data

def joung2023_v2(seed, data_dir='data'):
    d = f'{data_dir}/joung_v2_2023'
    file = f'{d}/joung2023_v2_{seed}.h5ad'
    Path(d).mkdir(parents=True, exist_ok=True)
    adata = anndata.read_h5ad(f'{d}/perturb_processed.h5ad')

    # Create split and save data (when GEARS restores saved splits,
    # these are not stored in pert_adata.adata.obs['split'])
    pert_data = PertData(f'{d}')
    pert_data.new_data_process(dataset_name='joung_v2', adata=adata)  # specific dataset name and adata object
    # pert_data.load(data_name='joung_v2', data_path=d)  # load the processed data, the path is saved folder + dataset_name
    pert_data.prepare_split(split='simulation', seed=seed)  # get data split with seed
    if not os.path.exists(file):
        pert_data.adata.write_h5ad(file)
    else:
        pert_data.adata = anndata.read_h5ad(file)

    return pert_data

def get_pert_data(dataset, seed, **kwargs):
    if dataset == 'Norman2019':
        return norman2019(seed=seed, **kwargs)
    elif dataset == "Adamson2016":
        return adamson2016(seed=seed, **kwargs)
    elif dataset == "Dixit2016":
        return dixit2016(seed=seed, **kwargs)
    elif dataset == "ReplogleK562":
        return replogle_k562_2022(seed=seed, **kwargs)
    elif dataset == "ReplogleK562_v2":
        return replogle_k562_2022_v2(seed=seed, **kwargs)
    elif dataset == "ReplogleK562_v3":
        return replogle_k562_2022_v3(seed=seed, **kwargs)
    elif dataset == "ReplogleRPE1":
        return replogle_rpe1_2022(seed=seed, **kwargs)
    elif dataset == "Joung2023":
        return joung2023(seed=seed, **kwargs)
    elif dataset == "Joung2023_v2":
        return joung2023_v2(seed=seed, **kwargs)
    else:
        raise ValueError(f'Dataset {dataset} not supported')