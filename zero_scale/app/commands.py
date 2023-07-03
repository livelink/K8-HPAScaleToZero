import click
import click_log
import logging
import json
import os
from kubernetes import client, config
from kubernetes.client.rest import ApiException


class ZeroScale:

    def __init__(self):

        self.logger = logging.getLogger('zero_scale.cli')
        if os.getenv('KUBERNETES_SERVICE_HOST'):
            self.logger.info("Using in cluster config")
            config.load_incluster_config()
        else:
            self.logger.info("Not in cluster - loading kube config")
            config.load_kube_config()

    def current_metric_value(self, namespace, metric_name):

        self.logger.debug(namespace)
        self.logger.debug(metric_name)

        client_api = client.ApiClient()
        metrics_url='/apis/custom.metrics.k8s.io/v1beta1/namespaces/{}/pods/*/{}'.format(namespace, metric_name)

        try:
            res = json.loads(client_api.call_api(metrics_url, 'GET', auth_settings=['BearerToken'], _preload_content=False)[0].data.decode('utf-8'))
            value = [element for element in res['items'] if element["metricName"] == metric_name][0]['value']
            return int(value)

        except ApiException as e:
                print(f'Exception when calling ApiClient: %s\n', e)

    def scale_deployment(self, scale, deployment_name, namespace):

        self.logger.info(f'Scaling %s:%s to %s', namespace, deployment_name, scale)
        apps_api = client.AppsV1Api()
        try:
            api_response = apps_api.patch_namespaced_deployment_scale(name=deployment_name,
                                                                         namespace=namespace,
                                                                         body={'spec': {'replicas': scale}})
            # self.logger.debug(api_response)

        except ApiException as e:
                print(f'Exception when calling AppsV1Api->: %s\n', e)

    def current_scale(self, deployment_name, namespace):

        apps_api = client.AppsV1Api()
        try:
            res = apps_api.read_namespaced_deployment(name=deployment_name, namespace=namespace)
            # self.logger.debug(api_response)
            value = res.status.replicas
            if value == None:
                return 0
            else:
                return value

        except ApiException as e:
                print(f'Exception when calling AppsV1Api->: %s\n', e)

    def scale_already_zero(self, namespace, metric_name, deployment_name):

        if  (self.current_metric_value(namespace, metric_name) == 0 and
            self.current_scale(namespace=namespace, deployment_name=deployment_name) == 0):
            return True
        else:
            return False

