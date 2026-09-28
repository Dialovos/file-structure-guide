from acme_cli import main


def test_main_prints_greeting(capsys):
    main()
    assert "hello" in capsys.readouterr().out
