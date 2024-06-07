import os
import sys
import tomllib
from dataclasses import dataclass, field

from icecream import ic

CONFIGURATION_FILENAME = "configuration.toml"
with open(CONFIGURATION_FILENAME, "rb") as f:
    SETTING = tomllib.load(f)

DATASET_PROFILE: str = SETTING.get("dataset")  # "tabler-icons-3.5.0"
DATASET_CONFIG: dict = SETTING["datasets"][SETTING.get("dataset")]
MODEL_CONFIG = SETTING["embedding_model_profile"].get(
    DATASET_CONFIG.get("model_profile")
)


@dataclass
class IconDatabase:
    """
    # Dataset database settings
    Represents the configuration for an icon database.

    ### Arguments:
    - `dataset_profile`: (optional) The name of the dataset profile to use. Defaults to the value in the configuration file.
    - `datasets_directory`: (optional) The directory name relative to main.py containing datasets. Defaults to the value in the configuration file.

    ### Attributes:
    - `dataset_directory`: The sub-directory within datasets_directory containing the specific dataset.
    - `database_filename`: The filename of the database within the dataset_directory.
    - `table_name`: The name of the table within the database to interact with.
    - `database_file`: The full file path to the database file.
    - `database_url`: The URL used to connect to the database.
    """

    dataset_profile: str = SETTING.get("dataset")  # Eit
    datasets_directory: str = SETTING["locations"]["datasets_directory"]
    dataset_directory: str = field(init=False)
    database_filename: str = field(init=False)
    table_name: str = field(init=False)
    database_file: str = field(init=False)
    database_url: str = field(init=False)

    def __post_init__(self):
        profile_data = SETTING["datasets"][self.dataset_profile]
        self.dataset_directory = profile_data["dataset_directory"]
        self.database_filename = profile_data["database_filename"]
        self.table_name = profile_data["table_name"]
        self.database_file = os.path.join(
            sys.path[0],
            self.datasets_directory,
            self.dataset_directory,
            self.database_filename,
        )
        self.database_url = f"sqlite:///./{self.database_file}"


@dataclass
class EmbeddingModel:
    """
    # Embedding model
    Runtime information for using a model with a dataset
    """

    profile_name: str = DATASET_CONFIG["model_profile"]
    model_string: str = field(init=False)
    query_prompt: str = field(init=False)
    encoding_parameters: dict | None = field(init=False)

    def __post_init__(self):
        self.model_string = MODEL_CONFIG["model_string"]
        self.query_prompt = MODEL_CONFIG["query_prompt"]
        self.encoding_parameters = MODEL_CONFIG.get("encoding_parameters")


icon_database = IconDatabase()
embedding_model_config = EmbeddingModel()

ic(icon_database)
ic(embedding_model_config)
