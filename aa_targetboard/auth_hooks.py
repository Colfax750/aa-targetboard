from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls


class PermissionedMenuItem(MenuItemHook):
    """Hide menu item if user lacks the required perm."""
    required_perm = "aa_targetboard.view_target"

    def render(self, request) -> str:
        if not request.user.has_perm(self.required_perm):
            return ""
        return super().render(request)


@hooks.register("menu_item_hook")
def register_menu():
    return PermissionedMenuItem(
        "Target Board",
        "fas fa-bullseye fa-fw",
        "aa_targetboard:list",
        order=150,
        navactive=["aa_targetboard:"],
    )


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "aa_targetboard", r"^targetboard/")
