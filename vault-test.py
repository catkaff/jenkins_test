import hvac, sys
mount_point = 'kv'
secret_path = 'message'
#secret_path = 'message2'
roottoken = 'hvs.1XIaQgAlirW9eWVbUvmLzZHb'
usertoken = 'hvs.CAESIC_LsXpP6oBPr6ZS3U8uGWFkVQ7SzB_TsiaGT8aOgX_3Gh4KHGh2cy56QmMwbjFZQ0tvcWZQcTNLTnNveTZ3dmc'

try:
    client = hvac.Client(url='https://vault.wefurries.ru:2083', token=usertoken,)
    print(client.is_authenticated())
    read_secret_result = client.secrets.kv.v1.read_secret(path=secret_path, mount_point=mount_point, )

    for key, value in read_secret_result.items():
        print(key, ': ', value)

    key0 = list(read_secret_result['data'].keys())[0]
    print('\n Password: ' + str(read_secret_result['data'][key0]))

except hvac.exceptions.Forbidden as vault_exception:
    print(vault_exception.errors[0])
    sys.exit(1)
