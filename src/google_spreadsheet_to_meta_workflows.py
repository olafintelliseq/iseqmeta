import gspread
import json
import argparse
from collections import OrderedDict

__version__ = "0.0.3"


def args_parser_init():
    parser = argparse.ArgumentParser(description="""Creates new meta.json with workflows general parameters filled from google spreadsheet.
Further explanation can be found here: 
    https://workflows-dev-documentation.readthedocs.io/en/latest/Developer%20tools.html#parsing-google-spreadsheet-to-meta""")
    parser.add_argument('--input-workflow-name', type=str, required=True,
                        help='Workflow\'s name')
    parser.add_argument('--input-credentials-json', type=str, required=True,
                        help='Credentials.json containing data necessary to get access to google developer\'s privileges')
    parser.add_argument('--input-meta-json', type=str, required=True,
                        help='Meta.json file from selected workflow')
    parser.add_argument('--input-google-spreadsheet-key', type=str, required=True,
                        help='A key to access to the google spreadsheet')
    parser.add_argument('--output-meta-json', type=str, required=True,
                        help='An updated meta.json file')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))

    args = parser.parse_args()
    return args


def save_to_json(output_meta_json, meta_json):
    with open(output_meta_json, "w") as json_file:
        json.dump(meta_json, json_file, indent=3)


def get_json_content(input_meta_json):
    with open(input_meta_json) as json_file:
        return json.load(json_file)


def split_different_workflow_variants(record):
    raw_workflow_variant = record['workflow_variant'].split()
    workflow_variant_no_whitespace = "".join(raw_workflow_variant)
    return workflow_variant_no_whitespace.split(',')


def update_booleans(record):
    for key in record.keys():
        if isinstance(record[key], str):
            if record[key].replace(" ", "").lower() == "true":
                record[key] = True
            elif record[key].replace(" ", "").lower() == "false":
                record[key] = False


def update_workflows_parameters(workflow, variant_name, meta_json):
    workflows_parameters = ['name', 'description', 'price', 'tag', 'longDescription', 'beta']

    for parameter in workflows_parameters:
        if workflow[parameter]:
            meta_json[f'{variant_name}{parameter}'] = workflow[parameter]

    # price always must be string type
    meta_json[f'{variant_name}price'] = str(meta_json[f'{variant_name}price'])

    update_booleans(meta_json)


def update_meta_workflows(workflows, meta_json):
    for workflow in workflows:
        workflow_variant = workflow['workflow_variant'].split('_')
        variant_name = ""

        if len(workflow_variant) > 1:
            variant_name = f"{workflow_variant[1]}_"

        update_workflows_parameters(workflow, variant_name, meta_json)
    return meta_json


def filter_by_workflow(unfiltered, workflow_name):
    filtered = list()
    for index, record in enumerate(unfiltered):
        workflow_variant_list = split_different_workflow_variants(record)

        for workflow_variant in workflow_variant_list:
            workflow = workflow_variant.split('_')[0]
            if workflow == workflow_name:
                record['workflow_variant'] = workflow_variant
                filtered.append(record)

    return filtered


def update_meta(sheets, meta_json, workflow_name):
    workflows_worksheet = sheets.worksheet('Workflows')
    workflows = workflows_worksheet.get_all_records()

    workflows = filter_by_workflow(workflows, workflow_name)
    meta_json = update_meta_workflows(workflows, meta_json)

    return meta_json


def get_workflows(unsorted_keys):
    return sorted([key for key in unsorted_keys
                   if not key.startswith('input_')
                   and not key.startswith('output_')
                   and not key.startswith('variant')])


def get_inputs(unsorted_keys):
    return sorted([key for key in unsorted_keys
                   if key.startswith('input_')])


def get_variants(unsorted_keys):
    return sorted([key for key in unsorted_keys
                   if key.startswith('variant')])


def get_outputs(unsorted_keys):
    return sorted([key for key in unsorted_keys
                   if key.startswith('output_')])


def order_by_parameter(meta_json):
    sorted_meta = OrderedDict()
    unsorted_keys = list(meta_json.keys())

    workflows = get_workflows(unsorted_keys)
    inputs = get_inputs(unsorted_keys)
    variants = get_variants(unsorted_keys)
    outputs = get_outputs(unsorted_keys)

    sorted_keys = workflows + inputs + variants + outputs
    new_len = len(sorted_keys)
    old_len = len(unsorted_keys)

    if new_len != old_len:
        raise ValueError(f'Sorted keys number [{new_len}] does not equal unsorted keys number [{old_len}]')

    for key in sorted_keys:
        sorted_meta[key] = meta_json[key]

    return sorted_meta



if __name__ == '__main__':
    args = args_parser_init()
    gc = gspread.service_account(filename=args.input_credentials_json)
    sheets = gc.open_by_key(args.input_google_spreadsheet_key)

    meta_json = get_json_content(args.input_meta_json)
    meta_json = update_meta(sheets, meta_json, args.input_workflow_name)
    meta_json = order_by_parameter(meta_json)

    save_to_json(args.output_meta_json, meta_json)
