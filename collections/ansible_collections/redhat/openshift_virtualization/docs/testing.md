# Testing

## Sanity and unit tests

Sanity and unit tests can be run with `ansible-test`.

### Running tests with ansible-test

Run sanity tests with `ansible-test` like so:

```
ANSIBLE_TEST_PREFER_PODMAN=1 ansible-test sanity --docker
```

Run unit tests with `ansible-test` like so:

```
ANSIBLE_TEST_PREFER_PODMAN=1 ansible-test units --docker
```

## Integration tests

Integration tests require a working cluster and can be run with
`ansible-test`.

### Running integration tests with ansible-test

Run integration tests with `ansible-test` like so:

```
ansible-test integration
```
