# Python bindings to the DeviceDemo API

这是一个基于DeviceDemo API 构建的客户端库， 其中包括python SDK 和命令行工具2部分
这也是一个Demo, 参考Openstack Magnum规范。

### CLI使用样例

1. 查看列表

```
(.venv)  maojun@maojun-mbp# source tools/admin_openrc
(.venv)  maojun@maojun-mbp# PYTHONPATH=. python3 devicedemoclient/shell.py device-list
+--------------------------------------+------------+-----------+--------+---------+
| uuid                                 | name       | type      | vendor | version |
+--------------------------------------+------------+-----------+--------+---------+
| test_new7                            | test_new7  | test_new7 | test   | 111     |
| faf7404e-1d9a-47d2-bc49-48569ad5ed6e | api_test   | -         | -      | -       |
| e3be6917-9ae8-4818-b5bf-d864631c2318 | cli_test01 | -         | -      | -       |
+--------------------------------------+------------+-----------+--------+---------+
```

2. 查看详情

```
(.venv)  maojun@maojun-mbp# PYTHONPATH=. python3 devicedemoclient/shell.py device-show test_new7
+----------+-----------+
| Property | Value     |
+----------+-----------+
| vendor   | test      |
| name     | test_new7 |
| type     | test_new7 |
| version  | 111       |
| uuid     | test_new7 |
+----------+-----------+
```

3. 添加设备

```
(.venv)  maojun@maojun-mbp# PYTHONPATH=. python3 devicedemoclient/shell.py device-create "cli_test04"
Create device <f7de4ff3-0b25-46b2-88a7-81e1e9535806> successful.
```

4. 删除设备

```
(.venv)  maojun@maojun-mbp# PYTHONPATH=. python3 devicedemoclient/shell.py device-list
+--------------------------------------+------------+-----------+--------+---------+
| uuid                                 | name       | type      | vendor | version |
+--------------------------------------+------------+-----------+--------+---------+
| test_new7                            | test_new7  | test_new7 | test   | 111     |
| faf7404e-1d9a-47d2-bc49-48569ad5ed6e | api_test   | -         | -      | -       |
| e3be6917-9ae8-4818-b5bf-d864631c2318 | cli_test01 | -         | -      | -       |
| f7de4ff3-0b25-46b2-88a7-81e1e9535806 | cli_test04 | -         | -      | -       |
+--------------------------------------+------------+-----------+--------+---------+
(.venv)  maojun@maojun-mbp# PYTHONPATH=. python3 devicedemoclient/shell.py device-delete "f7de4ff3-0b25-46b2-88a7-81e1e9535806"
Request to delete device f7de4ff3-0b25-46b2-88a7-81e1e9535806 successful.
(.venv)  maojun@maojun-mbp# PYTHONPATH=. python3 devicedemoclient/shell.py device-list
+--------------------------------------+------------+-----------+--------+---------+
| uuid                                 | name       | type      | vendor | version |
+--------------------------------------+------------+-----------+--------+---------+
| test_new7                            | test_new7  | test_new7 | test   | 111     |
| faf7404e-1d9a-47d2-bc49-48569ad5ed6e | api_test   | -         | -      | -       |
| e3be6917-9ae8-4818-b5bf-d864631c2318 | cli_test01 | -         | -      | -       |
+--------------------------------------+------------+-----------+--------+---------+
```