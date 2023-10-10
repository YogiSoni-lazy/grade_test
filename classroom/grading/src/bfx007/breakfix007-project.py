# import openshift as oc

# import time
from ocpcli.manifests import create_manifest_step, apply_manifest_step
from bfx007.common import BaseLab
from ocpcli.health import wait_cluster_step
from bfx007.common.constants import MATERIALS_PATH

# from bfx007.common.constants import WORKDIR
from ocpcli.projects import delete_project_step, project_exists
from ocpcli.apps import create_app_step
from labs.ui import GradingStep

# from labs.common.steps import copy_materials_step


class Breakfix007(BaseLab):
    __LAB__ = "breakfix007-project"
    mpath = MATERIALS_PATH / "labs" / __LAB__
    NameSpace = "foo"

    def start(self):
        wait_cluster_step()
        if project_exists(self.NameSpace)[0]:
            print(f"'{self.NameSpace}' project exists, do not run start multiple times")
        # copy_materials_step(MATERIALS_PATH, self.__LAB__, WORKDIR)
        else:
            create_manifest_step(self.mpath / "project.yaml")
            create_app_step(
                "https://github.com/openshift-instruqt/blog-django-py",
                self.NameSpace,
                ["--strategy=source"],
            )
            apply_manifest_step(self.mpath / "service.yaml")
            apply_manifest_step(self.mpath / "foo-crd.yaml")
            apply_manifest_step(self.mpath / "foo.yaml")

    def grade(self):
        with GradingStep("Project status check") as step:
            if project_exists(self.NameSpace)[0]:
                step.add_error("Ensure " + f"'{self.NameSpace}' project is removed")
                step.add_error("Sorry. There still seems to be a problem.")
                step.fail()
            else:
                step.add_message("Project " + f"'{self.NameSpace}' is removed")
                step.add_message("COMPLETION CODE: PROJRMFOO")
                step.success()

    def finish(self):
        if project_exists(self.NameSpace)[0]:
            print(
                f"'{self.NameSpace}' project is exists, remove the project and then run finish"
            )
        else:
            delete_project_step(self.NameSpace)
            print(f"'{self.NameSpace}' project does not exist")
