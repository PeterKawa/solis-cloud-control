import logging

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.solis_cloud_control.data import SolisCloudControlConfigEntry
from custom_components.solis_cloud_control.number_utils import safe_get_int_value

from .const import CID_STORAGE_MODE
from .coordinator import SolisCloudControlCoordinator
from .entity import SolisCloudControlEntity

_LOGGER = logging.getLogger(__name__)


_MODE_SELF_USE = "Self-Use"
_MODE_FEED_IN_PRIORITY = "Feed-In Priority"
_MODE_OFF_GRID = "Off-Grid"

_BIT_SELF_USE = 0
_BIT_OFF_GRID = 2
_BIT_BACKUP_MODE = 4
_BIT_GRID_CHARGING = 5
_BIT_FEED_IN_PRIORITY = 6


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SolisCloudControlConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        [
            StorageModeSelect(
                coordinator=coordinator,
                entity_description=SelectEntityDescription(
                    key="storage_mode",
                    name="Storage Mode",
                    icon="mdi:solar-power",
                ),
                cid=CID_STORAGE_MODE,
            ),
        ]
    )


class StorageModeSelect(SolisCloudControlEntity, SelectEntity):
    def __init__(
        self, coordinator: SolisCloudControlCoordinator, entity_description: SelectEntityDescription, cid: int
    ) -> None:
        super().__init__(coordinator, entity_description, cid)
        self._attr_options = [_MODE_SELF_USE, _MODE_FEED_IN_PRIORITY, _MODE_OFF_GRID]

    @property
    def current_option(self) -> str | None:
        value_str = self.coordinator.data.get(self.cid)
        value = safe_get_int_value(value_str)
        if value is None:
            return None

        if value & (1 << _BIT_SELF_USE):
            return _MODE_SELF_USE
        elif value & (1 << _BIT_FEED_IN_PRIORITY):
            return _MODE_FEED_IN_PRIORITY
        elif value & (1 << _BIT_OFF_GRID):
            return _MODE_OFF_GRID

        return None

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        value_str = self.coordinator.data.get(self.cid)
        value = safe_get_int_value(value_str)

        attributes = {}
        if value is not None:
            battery_reserve = "ON" if value & (1 << _BIT_BACKUP_MODE) else "OFF"
            allow_grid_charging = "ON" if value & (1 << _BIT_GRID_CHARGING) else "OFF"

            attributes["battery_reserve"] = battery_reserve
            attributes["allow_grid_charging"] = allow_grid_charging

        return attributes

    async def async_select_option(self, option: str) -> None:
        value_str = self.coordinator.data.get(self.cid)
        value = safe_get_int_value(value_str)
        if value is None:
            return

        value &= ~(1 << _BIT_SELF_USE)
        value &= ~(1 << _BIT_FEED_IN_PRIORITY)
        value &= ~(1 << _BIT_OFF_GRID)

        if option == _MODE_SELF_USE:
            value |= 1 << _BIT_SELF_USE
        elif option == _MODE_FEED_IN_PRIORITY:
            value |= 1 << _BIT_FEED_IN_PRIORITY
        elif option == _MODE_OFF_GRID:
            value |= 1 << _BIT_OFF_GRID

        _LOGGER.info("Setting storage mode to %s (value: %s)", option, value)

        await self.coordinator.control(self.cid, str(value))
