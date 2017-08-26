FROM node:8.1.2
MAINTAINER Jan Borsodi <jb@aplia.no>

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python-dev && \
    curl https://bootstrap.pypa.io/get-pip.py | python && \
    apt-get install -y rsync

# install watchman
# Note: See the README.md to find out how to increase the
# fs.inotify.max_user_watches value so that watchman will
# work better with ember projects.
RUN \
	git clone https://github.com/facebook/watchman.git && \
	cd watchman && \
	git checkout v4.9.0 && \
	./autogen.sh && \
	./configure && \
	make && \
	make install && \
	pip install pywatchman && \
	cd .. && rm -rf watchman/

# Install yarn, replaces npm
RUN curl -o- -L https://yarnpkg.com/install.sh | bash

# Install ember dev dependencies
RUN \
	yarn global add bower@1.8.0 && \
	yarn global add livereload && \
	yarn global add nodemon@1.11.0

COPY ./entrypoint.sh ./watch.sh /
RUN sed -i 's/\r//' /*.sh \
    && chmod +x /*.sh

ENTRYPOINT ["/entrypoint.sh"]
