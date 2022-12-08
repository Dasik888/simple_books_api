# Set up python environment for autotests
1. Need to know where Python was installed
- whereis python3
2. Initiate VirtualEnv for project
- virtualenv -p {path to python3}python3.9 env
3. Activate VirtualEnv
- source env/bin/activate
3. Install requirements.txt
- pip install -r requirements.txt
4. Set up PyTets as a default runer
- PyCharm - File - Settings - Tools - Python integrated tools - default test runner: pytest