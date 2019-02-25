"""
A set of tools for common CIDC tasks.
"""
import json
import attr


@attr.s
class TrialRecord(object):
    """
    Class representing a mongo record for a trial.

    Arguments:
        object {[type]} -- [description]
    """
    trial_name = attr.ib()
    principal_investigator = attr.ib()
    start_date = attr.ib()
    samples = attr.ib(factory=list)
    assays = attr.ib(factory=list)
    collaborators = attr.ib(factory=list)


@attr.s
class AssayRecord(object):
    """
    Class representing a mongo record for an assay.

    Arguments:
        object {[type]} -- [description]
    """
    assay_name = attr.ib()
    wdl_location = attr.ib()
    static_inputs = attr.ib(factory=list)
    non_static_inputs = attr.ib(factory=list)


@attr.s
class DataRecord(object):
    """
    Class representing a mongo record for uploaded data.

    Arguments:
        Object {[type]} -- [description]
    """
    _id = attr.ib()
    assay = attr.ib()
    trial = attr.ib()
    file_name = attr.ib()
    sample_id = attr.ib()
    mapping = attr.ib()
    gs_uri = attr.ib()
    date_created = attr.ib()
    processed = attr.ib()


def convert_input_json(path: str) -> dict:
    """
    Takes an input.json file and coverts into into a dictionary
    object that can be inserted into MongoDB

    Arguments:
        path {str} -- Path to input file.

    Returns:
        dict -- Formatted dictionary in the form of a mongo record.
    """
    with open(path, 'r') as input_json:
        json_str = json.loads(input_json.read())
        return [{"key_name": key, "key_value": value} for key, value in json_str.items()]


def create_record(input_path, wdl_location, non_static_inputs, assay_name):
    """Create sample records for mongo insert

    Arguments:
        input_path {[type]} -- [description]
        wdl_location {[type]} -- [description]
        non_static_inputs {[type]} -- [description]
        assay_name {[type]} -- [description]
    """
    static_inputs = convert_input_json(input_path)
    assay = AssayRecord(
        assay_name=assay_name,
        wdl_location=wdl_location,
        static_inputs=static_inputs,
        non_static_inputs=non_static_inputs
    )
    print(assay)
