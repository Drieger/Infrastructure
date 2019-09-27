dockerfile='dockerfile'
basedir='.'
tag='CustomImage:lastest'
build:
	@echo "#########################"
	@echo "# Building docker image #"
	@echo "#########################"
	docker build -t $(tag) -f $(dockerfile) $(basedir)

message='make echo message="Your message here"'
echo:
	@echo "################"
	@echo "# Echo command #"
	@echo "################"
	@echo $(message)

.PHONY: all
