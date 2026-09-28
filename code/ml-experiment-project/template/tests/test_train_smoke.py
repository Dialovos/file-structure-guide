from project.config import load
from project.train import run


def test_run_writes_record(tmp_path):
    config = load("configs/experiment/baseline.toml")
    run_dir = run(config, seed=0, name="smoke", runs_dir=tmp_path)
    assert (run_dir / "config.resolved.json").is_file()
    assert (run_dir / "meta.json").is_file()
    assert (run_dir / "metrics.jsonl").read_text().count("\n") == config["optim"]["steps"]
