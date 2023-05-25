#
# Author: Jake Zimmerman <jake@zimmerman.io>
#
# ===== Usage ================================================================
#
# make                  Prepare docs/ folder (all markdown & assets)
# make docs/index.html  Recompile just docs/index.html
#
# make watch            Start a local HTTP server and rebuild on changes
# PORT=4242 make watch  Like above, but use port 4242
#
# make clean            Delete all generated files
#
# ============================================================================

SOURCES := $(shell find src -type f -name '*.md')
TARGETS := $(patsubst src/%.md,docs/%.html,$(SOURCES))

IMAGES := $(shell find public/img -type f -name '*.jpg')
THUMBS := $(patsubst public/img/%.jpg,docs/img/thumb/%.jpg,$(IMAGES))

.PHONY: all
all: docs/.nojekyll docs/img/thumb $(TARGETS) $(THUMBS)
	rm -rf ../georgia
	cp -r docs ../georgia

.PHONY: clean
clean:
	rm -rf docs

.PHONY: watch
watch:
	./tools/serve.sh --watch

docs/.nojekyll: $(wildcard public/*) public/.nojekyll
	rm -vrf docs && mkdir -p docs && cp -vr public/.nojekyll public/* docs

.PHONY: docs
docs: docs/.nojekyll

# Generalized rule: how to build a .html file from each .md
# Note: you will need pandoc 2 or greater for this to work
docs/%.html: src/%.md template.html5 Makefile tools/build.sh
	tools/build.sh "$<" "$@"

docs/img/thumb:
	mkdir docs/img/thumb

docs/img/thumb/%.jpg: public/img/%.jpg
	cp "$<" "$@"
	sips -Z 1000 "$@"

