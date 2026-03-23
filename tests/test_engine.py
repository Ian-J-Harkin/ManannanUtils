import os
import sys
import json
import pytest

# Ensure ui directory is in path for testing
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui"))
from engine import DigitizationEngine

@pytest.fixture
def engine(tmp_path):
    # Mock some data for the engine
    utils_root = tmp_path / "ManannanUtils"
    utils_root.mkdir()
    (utils_root / "python-utils").mkdir()
    
    # Create engine and point it to tmp_path for config
    os.chdir(tmp_path)
    engine = DigitizationEngine()
    engine.config_file = str(tmp_path / "workspace_config.json")
    return engine

def test_engine_defaults(engine):
    assert engine.old_folder == "old-orthography"
    assert engine.new_folder == "new-orthography"

def test_engine_save_load_config(engine, tmp_path):
    data_root = str(tmp_path / "Data")
    old_f = "source"
    new_f = "output"
    
    engine.save_config(data_root, old_f, new_f)
    
    # Create a fresh engine and check if it loads
    new_engine = DigitizationEngine()
    new_engine.config_file = engine.config_file
    new_engine.load_config()
    
    assert new_engine.data_root == data_root
    assert new_engine.old_folder == old_f
    assert new_engine.new_folder == new_f

def test_engine_path_generation(engine):
    engine.data_root = "/mock/data"
    engine.old_folder = "old"
    
    default_dir = engine.get_default_directory()
    assert "old" in default_dir
    assert "caibidlí" in default_dir
    assert os.path.isabs(default_dir)
