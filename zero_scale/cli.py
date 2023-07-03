#!/usr/bin/env python3

import click
import click_log
import logging
import time
from zero_scale.app import commands

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-s', '--scale', 'scale',
              default=0,
              help='Sets the scale of a deployment')
@click.option('-p', '--period', 'period',
              default=60,
              help='The time (seconds) between checks')
@click.option('--number', 'number',
              default=5,
              help='Number of positive results before action is taken')
@click.option('-n', '--namespace', 'namespace',
              default='default',
              help='The k8 namespace')
@click.option('-h', '--hpa', 'hpa_name',
              default='default',
              help='The HPA name')
@click.option('-m', '--metric-name', 'metric_name',
              default='default',
              help='The metric name')
@click.option('-d', '--deployment', 'deployment_name',
              default='default',
              help='The deployment to modify')
def run(scale, period, number, namespace, hpa_name, metric_name, deployment_name):

    scaler = commands.ZeroScale()
    positive_results = 0

    while True:
        try:
            time.sleep(period)
            logger.debug(f'positive_results: %s', positive_results)

            # Skip current iteration if scale is already 0
            if  scaler.scale_already_zero(metric_name=metric_name, deployment_name=deployment_name, namespace=namespace):
                logger.info(f'Scale already 0 - skipping')
                continue

            # Scale to 0 if number of positive results are hit
            if positive_results == number:
                logger.info(f'Scaling to 0')
                scaler.scale_deployment(scale,
                                        deployment_name,
                                        namespace)
                positive_results = 0
                continue

            # HPA is disabled when target deployment scale is zero.
            # Force scale to be 1 if metrics > 1
            if  (scaler.current_metric_value(namespace, metric_name) > 1 and
                scaler.current_scale(namespace=namespace, deployment_name=deployment_name) == 0):
                logger.info(f'Scaling to 1')
                scaler.scale_deployment(scale=1,
                                        deployment_name=deployment_name,
                                        namespace=namespace)

            # Keep track of positive results
            if scaler.current_metric_value(namespace, metric_name) == 0:
                positive_results += 1


        except Exception as e:
            logger.info(e)
            exit()

if __name__ == '__main__':
    run()
