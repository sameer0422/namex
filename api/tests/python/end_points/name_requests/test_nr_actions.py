"""
Integration tests for Name Request state transitions.
"""
import json

from tests.python.common.test_name_request_utils import \
    assert_field_is_mapped, assert_field_equals_value, assert_field_is_lt_value

from .test_setup_utils.test_helpers import \
    assert_names_are_mapped_correctly, assert_applicant_is_mapped_correctly, \
    create_draft_nr, patch_nr

from namex.models import State
from namex.constants import NameRequestActions

# Define our data
# Check NR number is the same because these are PATCH and call change_nr
draft_input_fields = {
    'additionalInfo': '',
    'consentFlag': None,
    'consent_dt': None,
    'corpNum': '',
    'entity_type_cd': 'CR',
    'expirationDate': None,
    'furnished': 'N',
    'hasBeenReset': False,
    # 'lastUpdate': None,
    'natureBusinessInfo': 'Test',
    # 'nrNum': '',
    # 'nwpta': '',
    # 'previousNr': '',
    # 'previousRequestId': '',
    # 'previousStateCd': '',
    'priorityCd': 'N',
    # 'priorityDate': None,
    'requestTypeCd': 'CR',
    'request_action_cd': 'NEW',
    # 'source': 'NAMEREQUEST',
    'state': 'DRAFT',
    'stateCd': 'DRAFT',
    'submitCount': 1,
    # 'submittedDate': None,
    'submitter_userid': 'name_request_service_account',
    'userId': 'name_request_service_account',
    'xproJurisdiction': ''
}


def test_draft_patch_edit_data(client, jwt, app):
    """
    Test the Name Request's data fields. Excludes associations 'names' and 'applicant' - we have other tests for those.
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    # Add another name to the mix
    nr_data = {
        'names': draft_nr.get('names'),
        'applicants': draft_nr.get('applicants'),
        'entity_type_cd': 'FR',
        'corpNum': 'TESTCORP123',
        # 'homeJurisNum': 'TESTHOME123',
        'additionalInfo': 'Testing additional info',
        'natureBusinessInfo': 'Testing nature of business info',
        'priorityCd': 'Y',
        'requestTypeCd': 'CR'
    }

    added_names = [
        {
            'name': 'BLUE HERON ADVENTURE TOURS LTD.',
            'choice': 2,
            'designation': 'LTD.',
            'name_type_cd': 'CO',
            'consent_words': '',
            'conflict1': 'BLUE HERON TOURS LTD.',
            'conflict1_num': '0515211'
        },
        {
            'name': 'BLUE HERON ISLAND TOURS LTD.',
            'choice': 3,
            'designation': 'LTD.',
            'name_type_cd': 'CO',
            'consent_words': '',
            'conflict1': 'BLUE HERON TOURS LTD.',
            'conflict1_num': '0515211'
        }
    ]

    nr_data['names'].extend(added_names)

    # Change the designation, we'll check to make sure it's mapped in the response
    nr_data['names'][0]['designation'] = 'INC.'

    # TODO: More applicant testing
    # updated_applicant = {}
    # nr_data['applicant'] = updated_applicant

    patch_response = patch_nr(client, NameRequestActions.EDIT.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == 'DRAFT'

    # Check names
    assert_names_are_mapped_correctly(nr_data.get('names'), patched_nr.get('names'))

    # Check applicant
    assert_applicant_is_mapped_correctly(nr_data.get('applicants'), patched_nr.get('applicants'))

    # Check data
    expected_field_values = {
        'additionalInfo': 'Testing additional info',
        'consentFlag': None,
        'consent_dt': None,
        'corpNum': 'TESTCORP123',
        # 'homeJurisNum': 'TESTHOME123',
        'entity_type_cd': 'FR',
        'expirationDate': None,
        'furnished': 'N',
        'hasBeenReset': False,
        # 'lastUpdate': None,
        'natureBusinessInfo': 'Testing nature of business info',
        # 'nrNum': '',
        # 'nwpta': '',
        # 'previousNr': '',
        # 'previousRequestId': '',
        # 'previousStateCd': '',
        'priorityCd': 'Y',
        # 'priorityDate': None,
        'requestTypeCd': 'CR',
        'request_action_cd': 'NEW',
        'source': 'NAMEREQUEST',
        'state': 'DRAFT',
        'stateCd': 'DRAFT',
        'submitCount': 1,
        # 'submittedDate': None,
        'submitter_userid': 'name_request_service_account',
        'userId': 'name_request_service_account',
        'xproJurisdiction': ''
    }

    for key, value in expected_field_values.items():
        assert_field_equals_value(patched_nr, key, value)


def test_draft_patch_edit_and_repatch(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    # Add another name to the mix
    nr_data = {
        'names': draft_nr.get('names'),
        'applicants': draft_nr.get('applicants')
    }

    added_names = [
        {
            'name': 'BLUE HERON ADVENTURE TOURS LTD.',
            'choice': 2,
            'designation': 'LTD.',
            'name_type_cd': 'CO',
            'consent_words': '',
            'conflict1': 'BLUE HERON TOURS LTD.',
            'conflict1_num': '0515211'
        },
        {
            'name': 'BLUE HERON ISLAND TOURS LTD.',
            'choice': 3,
            'designation': 'LTD.',
            'name_type_cd': 'CO',
            'consent_words': '',
            'conflict1': 'BLUE HERON TOURS LTD.',
            'conflict1_num': '0515211'
        }
    ]

    nr_data['names'].extend(added_names)

    # updated_applicant = {}

    # nr_data['applicant'] = updated_applicant

    patch_response = patch_nr(client, NameRequestActions.EDIT.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response #1: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == 'DRAFT'

    # TODO: Check applicant(s)

    # Check names
    assert_names_are_mapped_correctly(nr_data.get('names'), patched_nr.get('names'))

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    # Check actions (write a util for this)

    """
    Patch the NR again with the response to make sure everything runs as expected
    """

    patch_response = patch_nr(client, NameRequestActions.EDIT.value, patched_nr.get('nrNum'), patched_nr)
    patched_nr = json.loads(patch_response.data)

    re_patched_nr = json.loads(patch_response.data)
    assert re_patched_nr is not None

    print('PATCH Response #2: \n' + json.dumps(re_patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(re_patched_nr.get('stateCd') == 'DRAFT')))
    assert re_patched_nr.get('stateCd') == 'DRAFT'

    # TODO: Check applicant(s)

    # Check names
    assert_names_are_mapped_correctly(patched_nr.get('names'), re_patched_nr.get('names'))

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')


def test_draft_patch_upgrade(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None
    assert_field_equals_value(draft_nr, 'priorityCd', 'N')

    # Take the response and edit it
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.UPGRADE.value, draft_nr.get('nrNum'), nr_data)

    assert patch_response.status_code == 200
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    # Check actions (write a util for this)

    # assert_field_equals_value(patched_nr, 'payment_token', '')
    assert_field_equals_value(patched_nr, 'priorityCd', 'Y')
    # assert_field_equals_value(patched_nr, 'priorityDate', '')


def test_draft_patch_cancel(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.CANCEL.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == CANCELLED: ' + str(bool(patched_nr.get('stateCd') == 'CANCELLED')))
    assert patched_nr.get('stateCd') == State.CANCELLED

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    # Check actions (write a util for this)


def test_draft_patch_refund(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.REFUND.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')


def test_draft_patch_reapply(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    def do_reapply():
        # Take the response and edit it
        nr_data = {}
        patch_response = patch_nr(client, NameRequestActions.REAPPLY.value, draft_nr.get('nrNum'), nr_data)

        updated_nr = None
        if patch_response.status_code == 200:
            updated_nr = json.loads(patch_response.data)
            assert updated_nr is not None

            print('PATCH Response: \n' + json.dumps(updated_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

        return updated_nr, patch_response.status_code

    # Re-apply
    patched_nr, status_code = do_reapply()

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    assert_field_equals_value(patched_nr, 'submitCount', 2)
    # assert_field_equals_value(patched_nr, 'expirationDate', '')

    # Re-apply
    patched_nr, status_code = do_reapply()

    assert_field_equals_value(patched_nr, 'submitCount', 3)

    # Re-apply
    patched_nr, status_code = do_reapply()
    # The submitCount should never be greater than 3, this should now fail with a 500
    assert status_code == 500


def test_draft_patch_reapply_historical(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {
        'request_action_cd': 'REH'
    }

    patch_response = patch_nr(client, NameRequestActions.REAPPLY.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    assert_field_is_lt_value(patched_nr, 'submitCount', 4)
    # assert_field_equals_value(patched_nr, 'expirationDate', '')

    # Take the response and edit it
    nr_data = {
        'request_action_cd': 'REST'
    }

    patch_response = patch_nr(client, NameRequestActions.REAPPLY.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    assert_field_is_lt_value(patched_nr, 'submitCount', 4)
    # assert_field_equals_value(patched_nr, 'expirationDate', '')


def test_draft_patch_resend(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.RESEND.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')