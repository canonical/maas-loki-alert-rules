# Copyright 2022 Canonical Ltd.  This software is licensed under the
# Apache License version 2 (see the file LICENSE).

PIP:=pip3

all: groups

bin/cortextool:
	curl -fSL -o $@ "https://github.com/grafana/cortex-tools/releases/download/v0.10.7/cortextool_0.10.7_linux_x86_64"
	chmod a+x $@

.python-deps:
	$(PIP) install pyyaml
	touch $@

groups: rules/bundle.yml

clean:
	rm -f rules/bundle.yml

rules/bundle.yml: .python-deps
	./bin/group.py --rules './rules/*.rule' --out $@

lint: bin/cortextool rules/bundle.yml
	bin/cortextool rules lint --backend=loki --log.level=debug  rules/bundle.yml
