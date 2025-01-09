# Copyright 2025 yu-iskw
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Set up an environment
.PHONY: setup
setup: setup-python

# Set up the python environment.
.PHONY: setup-python
setup-python:
	bash ./dev/setup.sh --deps "development"

# Check all the coding style.
.PHONY: lint
lint:
	trunk check -a

# Format source codes
.PHONY: format
format:
	trunk fmt -a

# Run the unit tests.
.PHONY: test
test:
	uv run bash ./dev/test_python.sh

# Build the package
.PHONY: build
build:
	uv run bash ./dev/build.sh

# Clean the environment
.PHONY: clean
clean:
	uv run bash ./dev/clean.sh

all: clean lint test build

# Publish to pypi
.PHONY: publish
publish:
	uv run bash ./dev/publish.sh "pypi"

# Publish to testpypi
.PHONY: test-publish
test-publish:
	uv run bash ./dev/publish.sh "testpypi"


download-lightdash-json-schema:
	curl -o ./dev/resources/lightdash-dbt-2.0.json \
		https://raw.githubusercontent.com/lightdash/lightdash/main/packages/common/src/schemas/json/lightdash-dbt-2.0.json
