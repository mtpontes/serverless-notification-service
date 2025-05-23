import json

from boto3.session import Session

from src.main.infra.utils.log_utils import log
from src.main.infra.config.app_config import AppConfig
from src.main.infra.security.credentials_consts import SecretManagerConsts


class SecretManagerService():

    def __init__(self):
        log.info('%s - [constructor] - Start', self.__class__.__name__)
        
        self.client = Session().client(
            service_name=SecretManagerConsts.SERVICE_NAME, 
            region_name=AppConfig.secret_manager.region
        )
        
        log.info('%s - [constructor] - End - Self: %s', self.__class__.__name__, self)

    def get_secret(self, secret_name: str) -> dict:
        log.info('%s - catching secret', self.__class__.__name__)
        
        result: dict[str, any] = self.client.get_secret_value(SecretId=secret_name)
        secrets: str | None = result.get(SecretManagerConsts.SECRET_STRING)
        if secrets is not None:
            log.info('%s - secret loaded: %s', self.__class__.__name__, secrets)
            return json.loads(secrets)
        raise EmptySecretException("Secret not found")
        
    def update_secret(self, secret_name: str, secrets_key_value: dict) -> None:
        try:
            self.client.put_secret_value(
                SecretId=secret_name,
                SecretString=json.dumps(secrets_key_value), # Deve ser um json
            )
        except Exception: # TODO: Tratar possível erro ao atualizar
            pass
        
class EmptySecretException(Exception):
    def __init__(self, message: str = "Secret error"):
        super().__init__(message)