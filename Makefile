.PHONY: build-frontend package clean

# Build the frontend and copy dist into the Python package tree
build-frontend:
	cd frontend && npm ci && npm run build
	rm -rf backend/app/frontend_dist
	cp -r frontend/dist backend/app/frontend_dist

# Build the pip-installable package (wheel + sdist)
package: build-frontend
	python3 -m build

# Clean build artifacts
clean:
	rm -rf backend/app/frontend_dist
	rm -rf dist/ build/ *.egg-info backend/*.egg-info
