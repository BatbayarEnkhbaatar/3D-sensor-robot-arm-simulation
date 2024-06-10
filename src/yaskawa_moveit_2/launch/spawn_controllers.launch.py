from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_spawn_controllers_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("yaskawa_mh5lf", package_name="yaskawa_moveit_2").to_moveit_configs()
    return generate_spawn_controllers_launch(moveit_config)