---
page_type: sample
languages: 
- python
products: 
- azure
- azure-functions
title: Using Flask Framework with Azure Functions
---

# Using Flask Framework with Azure Functions

Azure Functions supports WSGI and ASGI-compatible frameworks with HTTP-triggered Python functions. This can be helpful if you are familiar with a particular framework, or if you have existing code you would like to reuse to create the Function app. The following is an example of creating an Azure Function app using Flask.
  
## Credit

This repo is forked and modified from [this sample](https://github.com/Azure-Samples/flask-app-on-azure-functions/).

**Install Python**

A [Python version](https://docs.microsoft.com/azure/azure-functions/supported-languages#languages-by-runtime-version) that is supported by Azure Functions is required. Run `python --version` (Linux/MacOS) or `py --version` (Windows) to check your Python version reports to a supported version. For more information on installing Python, see [How to install Python](https://wiki.python.org/moin/BeginnersGuide/Download).

**Install Azure Functions Core Tools**

Azure Functions Core Tools provides commands to create functions, connect to Azure, and deploy function projects. For more information, see [Install Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cwindows%2Ccsharp%2Cportal%2Cbash#install-the-azure-functions-core-tools).

**Create a new Azure Function App in VS Code**

To create an Azure Function app in VSCode, please go through the [Microsoft Docs tutorial on creating your first Azure Function using Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python). In the code snippet along with the sample, we name the two python module 'FlaskApp' and 'HandleApproach' with the HTTP trigger.

## Setup

Clone or download [this sample](https://github.com/Azure-Samples/flask-app-on-azure-functions/) repository, and open the sample folder in Visual Studio Code or your IDE of choice.

## Flask Framework in an Azure Function App

The file requirements.txt is updated to include the following depdendencies.
```python
azure-functions
Flask
```
Note that `azure-functions-worker` should not be included in this file as the Python worker is manager by Azure Functions platform and manually managing it may cause unexpected issues.

The following code shows the use of `WsgiMiddleware`, which redirects the invocations to Flask handler.
```python
import azure.functions as func
from FlaskApp import app

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the WSGI handler.
    """
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)
```

The file function.json is modified to include `route` in the HTTP trigger.
```json
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "authLevel": "anonymous",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": [
        "get",
        "post"
      ],
      "route": "/{*route}"
    },
    {
      "type": "http",
      "direction": "out",
      "name": "$return"
    }
  ]
}
```

The file host.json is updated to include the HTTP `routePrefix`.
```json
{
  "version": "2.0",
  "extensions": {
    "http": {
        "routePrefix": ""
    }
  }
}
```

## Running the sample

### Testing locally

To run Function Apps using Core Tools, see [Run functions locally with Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cwindows%2Cpython%2Cportal%2Cbash#start).

To test locally, run the below to install Flask.

```log
pip install -r requirements.txt
```

Then, start debug mode and test the function using the HTTP endpoint exposed after the host and the worker load up the function.

```log
Http Functions:
HandleApproach: [GET,POST] http://localhost:7071/<route>
```

### Testing in Azure

You can publish the function app directly from VSCode using the “Publish to Azure option” in the Azure extension. For more information, please refer the guide to [publish the project to Azure using Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python#publish-the-project-to-azure).

You can use a tool like Postman to see the API in action locally, and on Azure. Running locally will help you to verify the credentials, configuration and business logic.

### Calling the URL with Path Parameters

When running this sample, you can try a different URL route as well as parameterize it. For instance, `http://<HOST>:7071/joke` to tell the Flask app invoking to reach random joke site and will respond back.

When done locally, please try the following URL in your browser -
```
http://localhost:7071/joke
```

When done in Azure, please try the following URL in your browser -
```
http://<FunctionAppName>.azurewebsites.net/joke
```

## Conclusion and Next Steps
To learn more about altering Python functions to leverage WSGI and ASGI-compatible frameworks, see [Web frameworks](https://docs.microsoft.com/azure/azure-functions/functions-reference-python?tabs=asgi%2Cazurecli-linux%2Capplication-level#web-frameworks).
