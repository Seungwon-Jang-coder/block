import os, shutil, random

def split_data(src_root, dst_root, split=(0.8, 0.1, 0.1)):
    classes = [d for d in os.listdir(src_root) if os.path.isdir(os.path.join(src_root, d))]
    for cls in classes:
        files = [f for f in os.listdir(os.path.join(src_root, cls)) if f.lower().endswith(('.jpg','.jpeg','.png'))]
        random.shuffle(files)
        n_total = len(files)
        n_train = int(n_total * split[0])
        n_val = int(n_total * split[1])
        n_test = n_total - n_train - n_val
        sets = {'train': files[:n_train], 'val': files[n_train:n_train+n_val], 'test': files[n_train+n_val:]}
        for set_name, set_files in sets.items():
            dst_dir = os.path.join(dst_root, set_name, cls)
            os.makedirs(dst_dir, exist_ok=True)
            for fname in set_files:
                shutil.copy2(os.path.join(src_root, cls, fname), os.path.join(dst_dir, fname))

split_data('data', 'data_split', split=(0.8,0.1,0.1))
