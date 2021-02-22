"""webservers.

Usage:
    webservers create <cfgfile>
    webservers destroy <results_file>
    webservers connect <results_file> [--browser]

Arguments:
    create
    destroy

Options:
"""

import sys
import time
from docopt import docopt
import yaml
import simplejson as json
import subprocess
from awshelper import Ec2Client, Ec2Resource, AwsHelperError


def main():
    """Startup or shutdown aws(addr2data) environment."""
    args = docopt(__doc__)

    ec2_client = Ec2Client()
    ec2_resource = Ec2Resource()

    if args['create']:
        with open(args['<cfgfile>']) as fin:
            cfg = yaml.safe_load(fin)
        print("Deploying web servers to public subnets")

        try:
            ec2_client.find_vpc(cfg['base']['vpc_name'])
        except AwsHelperError as err:
            sys.exit(err)

        try:
            ec2_client.find_subnet_ids(cfg['base']['priv_subnets'])
        except AwsHelperError as err:
            sys.exit(err)

        try:
            ec2_client.create_webserver_sg(cfg['security_group'])
        except AwsHelperError as err:
            sys.exit(err)

        try:
            instances = ec2_client.run_instances(cfg['webservers'])
        except AwsHelperError as err:
            sys.exit(err)

        instance_ids = [x[0] for x in instances['instances']]
        while True:
            print("Waiting instances to reach 'running' state")
            time.sleep(3)
            try:
                status = ec2_client.get_instance_state(instance_ids)
            except AwsHelperError as err:
                sys.exit(err)

            status = list(set(status))
            if len(status) == 1 and status[0] == "running":
                break

        with open(cfg['base']['output_file'], 'w') as fout:
            fout.write(json.dumps(instances, indent=4, sort_keys=False))

    elif args['destroy']:
        with open(args['<results_file>'], 'r') as fin:
            cfg = json.load(fin)

        print("Destroying web servers.")
        instance_ids = [x[0] for x in cfg['instances']]

        try:
            ec2_client.term_instances(instance_ids)
        except AwsHelperError as err:
            sys.exit(err)

        while True:
            print("Waiting instances to terminate")
            time.sleep(3)
            try:
                status = ec2_client.get_instance_state(instance_ids)
            except AwsHelperError as err:
                sys.exit(err)

            status = list(set(status))
            if len(status) == 1 and status[0] == "terminated":
                break

        print("Removing security group.")
        try:
            ec2_client.delete_security_group(cfg['sgId'])
        except AwsHelperError as err:
            sys.exit(err)

    elif args['connect']:
        with open(args['<results_file>'], 'r') as fin:
            cfg = json.load(fin)

        for instance in cfg['instances']:
            if args['--browser']:
                subprocess.Popen(f"start firefox http://{instance[1]}:5000", shell=True)
            else:
                subprocess.Popen(
                    ["putty", "-ssh", f"ubuntu@{instance[1]}", "-i", "C:\\Users\\Administrator\\.ssh\\webinar.ppk"])

if __name__ == "__main__":
    main()
