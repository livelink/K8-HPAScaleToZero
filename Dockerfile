FROM python:3.9
ADD . /tmp/zero-scale/
RUN pip install /tmp/zero-scale && rm -rf /tmp/zero-scale

ENTRYPOINT ["/usr/local/bin/zero-scale"]
