# Infrastructure

## Kubernetes
Contains basic files describing resources to create a server, running on GCK. It will setup a Storage, MongoDB, Server and HTTPS. Note that, to use it you must change the files and add the correct information.

For example, in the file `Kubernetes/7-certificate.yml`, the value for domains `domain.com` must be replaced with your own domain. This is the domain used to generate the certificate used with https.

```yaml
...
spec:
  domains:
    - domain.com
```

## Scripts
All scripts are developed in python. To use them, it is necessary to install all dependencies listed in `dependencies.txt` file, it can be achieved running

```bash
pip install -r dependencies.txt
```

> We recommend to use a environment, using tools such as [virtualenv](https://virtualenv.pypa.io/en/latest/).