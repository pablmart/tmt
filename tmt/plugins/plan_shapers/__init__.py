from collections.abc import Iterator
from typing import TYPE_CHECKING, Any, Callable

import tmt.log
import tmt.utils
from tmt.plugins import PluginRegistry

if TYPE_CHECKING:
    from tmt.base import Plan, Test
    from tmt.options import ClickOptionDecoratorType


PlanShaperClass = type['PlanShaper']


_PLAN_SHAPER_PLUGIN_REGISTRY: PluginRegistry[PlanShaperClass] = PluginRegistry()


def provides_plan_shaper(
        package_manager: str) -> Callable[[PlanShaperClass], PlanShaperClass]:
    """
    A decorator for registering package managers.

    Decorate a package manager plugin class to register a package manager.
    """

    def _provides_plan_shaper(package_manager_cls: PlanShaperClass) -> PlanShaperClass:
        _PLAN_SHAPER_PLUGIN_REGISTRY.register_plugin(
            plugin_id=package_manager,
            plugin=package_manager_cls,
            logger=tmt.log.Logger.get_bootstrap_logger())

        return package_manager_cls

    return _provides_plan_shaper


def find_package_manager(name: str) -> 'PlanShaperClass':
    """
    Find a plan shaper by its name.

    :raises GeneralError: when the plugin does not exist.
    """

    plugin = _PLAN_SHAPER_PLUGIN_REGISTRY.get_plugin(name)

    if plugin is None:
        raise tmt.utils.GeneralError(
            f"Package manager '{name}' was not found in package manager registry.")

    return plugin


class PlanShaper(tmt.utils.Common):
    """ A base class for package manager plugins """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def run_options(cls) -> list['ClickOptionDecoratorType']:
        raise NotImplementedError

    @classmethod
    def check(cls, plan: 'Plan', tests: list[tuple[str, 'Test']]) -> bool:
        raise NotImplementedError

    @classmethod
    def apply(
            cls,
            plan: 'Plan',
            tests: list[tuple[str, 'Test']]) -> Iterator['Plan']:
        raise NotImplementedError
