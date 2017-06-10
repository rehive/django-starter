from invoke import Collection
import local_tasks
import k8s_tasks

ns = Collection()
ns.add_collection(Collection.from_module(local_tasks, name='local'))
ns.add_collection(Collection.from_module(k8s_tasks, name='k8s'))
