import os
import openshift as oc

from labs.activities import GuidedExercise


class BaseLab(GuidedExercise):
    def __init__(self):
        lab_exec_kubeconfig = os.environ.get(
            "LAB_KUBECONFIG", "~/.auth/ocp4-kubeconfig"
        )
        expanded = os.path.expanduser(lab_exec_kubeconfig)
        oc.set_default_kubeconfig_path(expanded)
