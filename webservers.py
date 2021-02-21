"""webservers.

Usage:
    webservers create <cfgfile>
    webservers destroy <cfgfile>

Arguments:
    create
    destroy

Options:
"""

import sys
from docopt import docopt
import yaml
import simplejson as json
from awshelper import Ec2Client, Ec2Resource, AwsHelperError


def main():
    """Startup or shutdown aws(addr2data) environment."""
    args = docopt(__doc__)
    with open(args['<cfgfile>']) as fin:
        cfg = yaml.safe_load(fin)

    ec2_client = Ec2Client()
    ec2_resource = Ec2Resource()

    if args['create']:
        print("Deploying web servers to private subnets")

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
            with open('results.json', 'w') as fout:
                fout.write(json.dumps(instances, indent=4, sort_keys=False))
        except AwsHelperError as err:
            sys.exit(err)

    elif args['destroy']:
        with open(args['<cfgfile>'], 'r') as fin:
            cfg = json.load(fin)

        print("Destroying web servers.")
        try:
            ec2_client.term_instances(cfg['instances'])
        except AwsHelperError as err:
            sys.exit(err)

        print("Removing security group.")
        try:
            ec2_client.delete_security_group(cfg['sgId'])
        except AwsHelperError as err:
            sys.exit(err)


if __name__ == "__main__":
    main()
