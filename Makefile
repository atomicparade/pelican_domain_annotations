lint:
	black pelican/plugins/domain_annotations
	mypy --strict pelican/plugins/domain_annotations
	pylint pelican/plugins/domain_annotations

sample:
	cd sample; pelican --debug

.PHONY: lint sample
