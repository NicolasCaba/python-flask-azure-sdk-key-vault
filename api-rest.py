import os
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import AzureError
from azure.identity import ClientSecretCredential
from flask import Flask, jsonify, request


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/get-secret', methods=['GET'])
def get_secret():
    args = request.args
    secretName = args.get('secretName')
    keyVaultName = args.get('keyVaultName')

    response = {}
    if secretName == None and keyVaultName == None:
        response = {"Error": "Ingrese los parametros \"secretName\" y \"keyVaultName\""}
    elif secretName is None:
        response = {"Error": "Ingrese el parametro \"secretName\""}
    elif keyVaultName is None:
        response = {"Error": "Ingrese el parametro \"keyVaultName\""}
    else:

        try:
            KVUri = f"https://{keyVaultName}.vault.azure.net"

            client_id = os.environ['AZURE_CLIENT_ID']
            client_secret = os.environ['AZURE_CLIENT_SECRET']
            tenant_id = os.environ['AZURE_TENANT_ID']

            credentials = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
            client = SecretClient(vault_url=KVUri, credential=credentials)

            retrieved_secret = client.get_secret(secretName)

        except AzureError as error:
            response = {"Error": "AzureError", "Args": error.args, "Message": "Verifique que los datos ingresados sean correctos"}
        else:
            response = {"secret-name": secretName, "secret-value": retrieved_secret.value}
            
    return jsonify(response)


if __name__=='__main__':
    app.run(debug=True)