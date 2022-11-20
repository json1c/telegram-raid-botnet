import random

from .application import Application


class LinuxAPI(Application):
    enviroments = ["GNOME", "MATE", "XFCE", "Cinnamon", "Unity", "ubuntu", "LXDE", "i3", "Openbox", "bspwm", "dwm", "KDE"]
    compositors = ["Wayland", "XWayland", "X11"]
    glibc_versions = ["2.32", "2.33", "2.34", "2.35"]
    app_versions = ["4.0.2 x64", "4.0.2", "3.7.3 x64", "3.6.1", "3.1.1 x64", "3.1.1"]

    lang_pack = "tdesktop"

    api_id = 2040
    api_hash = "b18441a1ff607e10a989891a5462e627"

    @staticmethod
    def app_version() -> str:
        return random.choice(LinuxAPI.app_versions)

    @staticmethod
    def device() -> str:
        return "PC 64bit"

    @staticmethod
    def sdk() -> str:
        enviroment = random.choice(LinuxAPI.enviroments)
        compositor = random.choice(LinuxAPI.compositors)
        glibc_version = random.choice(LinuxAPI.glibc_versions)

        return f"Linux {enviroment} {compositor} glibc {glibc_version}"
