![IntegriChain Logo](https://www.integrichain.com/wp-content/uploads/2019/03/integrichain-logo.svg)

# Postman - Newman E2E tests

_In this section we have all the e2e tests for the DoD API_

## Before executing 📋

_Have npm installed_


### Execution 🔧

_Install the newman as follows:_
```
npm install -g newman
```
_run the command_

```
newman run path/dod-api.postman_collection.json -e path/dod-api-{environment}.postman_environment.json
```