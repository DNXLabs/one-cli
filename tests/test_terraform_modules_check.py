from one.utils.terraform_modules import terraform_modules_check
from click.testing import CliRunner

runner = CliRunner()


def test_terraform_module_same_version():
    api_mock_data = """{
        "Modules":[
            {
                "Key": "terraform-aws-test",
                "Source": "git::https://github.com/DNXLabs/terraform-aws-test.git?ref=1.0.0"
            }
        ]
    }"""

    terraform_mock_data = {
        "modules": {
            "terraform-aws-test": {
                "html_url": "https://github.com/DNXLabs/terraform-aws-test/releases/tag/1.0.0",
                "tag_name": "1.0.0"
            }
        }
    }

    with runner.isolated_filesystem():
        with open('modules.json', 'w') as f:
            f.write(api_mock_data)
        results = terraform_modules_check(file_path='modules.json', api=terraform_mock_data)
        print(results)
    assert results == {'terraform-aws-test': {'key': 'terraform-aws-test', 'version': '1.0.0'}}


def test_terraform_module_new_version():
    api_mock_data = """{
        "Modules":[
            {
                "Key":"terraform-aws-test",
                "Source":"git::https://github.com/DNXLabs/terraform-aws-test.git?ref=1.0.0"
            }
        ]
    }"""

    terraform_mock_data = {
        "modules": {
            "terraform-aws-test": {
                "html_url": "https://github.com/DNXLabs/terraform-aws-test/releases/tag/1.0.0",
                "tag_name": "1.0.1"
            }
        }
    }

    with runner.isolated_filesystem():
        with open('modules.json', 'w') as f:
            f.write(api_mock_data)
        results = terraform_modules_check(file_path='modules.json', api=terraform_mock_data)
        print(results)
    assert results == {'terraform-aws-test': {'key': 'terraform-aws-test', 'version': '1.0.0', 'api_version': '1.0.1'}}


def test_empty_modules_list():
    api_mock_data = """{
        "Modules":[]
    }"""

    terraform_mock_data = {}

    with runner.isolated_filesystem():
        with open('modules.json', 'w') as f:
            f.write(api_mock_data)
        results = terraform_modules_check(file_path='modules.json', api=terraform_mock_data)
        print(results)
    assert results == {}


def test_terraform_module_local_dir_pointer():
    api_mock_data = """{
        "Modules":[
            {
                "Key":"",
                "Source":"",
                "Dir":"."
            }
        ]
    }"""

    terraform_mock_data = {}

    with runner.isolated_filesystem():
        with open('modules.json', 'w') as f:
            f.write(api_mock_data)
        results = terraform_modules_check(file_path='modules.json', api=terraform_mock_data)
        print(results)
    assert results == {}


def test_empty_missing_module_source():
    api_mock_data = """{
        "Modules":[
            {
                "Key":"terraform-aws-test"
            }
        ]
    }"""

    terraform_mock_data = {}

    with runner.isolated_filesystem():
        with open('modules.json', 'w') as f:
            f.write(api_mock_data)
        results = terraform_modules_check(file_path='modules.json', api=terraform_mock_data)
        print(results)
    assert results == {}
